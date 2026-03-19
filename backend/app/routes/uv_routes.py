"""
UV routes: fetch UV index from Open-Meteo (no API key) and return risk level and message.
Includes a simple in-memory cache and basic rate-limit handling for robustness.
"""
import time
import os
import copy
import threading
import requests
from datetime import date, datetime, timedelta
from flask import Blueprint, current_app, jsonify, request

from database.db import get_connection

uv_bp = Blueprint("uv_bp", __name__)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&daily=uv_index_max,uv_index_clear_sky_max"
    "&current=uv_index"
    "&hourly=uv_index"
    "&timezone=auto"
)

OPEN_METEO_ARCHIVE_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}"
    "&daily=uv_index_max&timezone=auto"
    "&start_date={start_date}&end_date={end_date}"
)

MAINTAINED_LOCATIONS = [
    {"id": "melbourne", "name": "Melbourne", "state": "VIC", "latitude": -37.8136, "longitude": 144.9631},
    {"id": "sydney", "name": "Sydney", "state": "NSW", "latitude": -33.8688, "longitude": 151.2093},
    {"id": "brisbane", "name": "Brisbane", "state": "QLD", "latitude": -27.4698, "longitude": 153.0251},
]

# Simple in-memory cache for UV responses.
# Key: (rounded_lat, rounded_lon)
# Value: {"timestamp": float, "payload": dict}
UV_CACHE = {}
CACHE_TTL_SECONDS = 600  # 10 minutes
LOCATION_CACHE = {}
LOCATION_CACHE_TTL_SECONDS = 1800  # 30 minutes
FORECAST_TIMEOUT_SECONDS = 5
ARCHIVE_TIMEOUT_SECONDS = 4
STALE_CACHE_MAX_AGE_SECONDS = 3600
UV_CACHE_ROUND_PLACES = 1
LOCATION_CACHE_ROUND_PLACES = 2
LOG_RESPONSE_PREVIEW_CHARS = 220
OPEN_METEO_429_BACKOFF_SECONDS = int(os.getenv("UV_OPEN_METEO_429_BACKOFF_SECONDS", "45"))
UV_PROVIDER_BACKOFF_UNTIL = {}
MAINTAINED_UV_CACHE = {}
MAINTAINED_REFRESH_INTERVAL_SECONDS = int(os.getenv("UV_MAINTAINED_REFRESH_INTERVAL_SECONDS", "420"))
MAINTAINED_MAX_SERVE_AGE_SECONDS = int(os.getenv("UV_MAINTAINED_MAX_SERVE_AGE_SECONDS", "1800"))
_UV_MAINTAINER_THREAD = None
_UV_MAINTAINER_LOCK = threading.Lock()
_UV_MAINTAINER_HOOK_LOCK = threading.Lock()


def _make_cache_key(lat: float, lon: float, places: int = 2, include_history=None):
    """Build a cache key from rounded latitude/longitude and request shape."""
    base = (round(float(lat), places), round(float(lon), places))
    if include_history is None:
        return base
    return (base[0], base[1], 1 if include_history else 0)


def _log_uv_debug(message: str, **fields):
    """Best-effort structured debug logging for /api/uv flow."""
    try:
        if fields:
            parts = [f"{k}={v}" for k, v in sorted(fields.items())]
            current_app.logger.info("[uv] %s | %s", message, " ".join(parts))
        else:
            current_app.logger.info("[uv] %s", message)
    except Exception:
        # Logging must never impact endpoint behavior.
        return


def _safe_preview(text, max_chars: int = LOG_RESPONSE_PREVIEW_CHARS):
    if text is None:
        return ""
    compact = str(text).replace("\n", " ").replace("\r", " ").strip()
    if len(compact) <= max_chars:
        return compact
    return compact[:max_chars] + "..."


def _format_cache_key_for_log(key) -> str:
    if isinstance(key, tuple):
        return ",".join(str(part) for part in key)
    return str(key)


def _return_503_with_log(reason: str, user_error: str, **fields):
    """Return a 503 response with a precise diagnostic log reason."""
    _log_uv_debug(f"returning 503 because {reason}", **fields)
    return jsonify({"error": user_error}), 503


def _is_provider_backoff_active(normalized_key: str):
    """Return True when we should avoid hammering Open-Meteo after recent 429."""
    until_ts = UV_PROVIDER_BACKOFF_UNTIL.get(normalized_key)
    if not until_ts:
        return False
    if time.time() >= until_ts:
        UV_PROVIDER_BACKOFF_UNTIL.pop(normalized_key, None)
        return False
    return True


def _iso_utc_now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _nearest_maintained_location(lat: float, lon: float):
    nearest = None
    nearest_dist = None
    for loc in MAINTAINED_LOCATIONS:
        dist = (loc["latitude"] - lat) ** 2 + (loc["longitude"] - lon) ** 2
        if nearest_dist is None or dist < nearest_dist:
            nearest_dist = dist
            nearest = loc
    return nearest, nearest_dist


def _get_maintained_entry(loc_id: str):
    return MAINTAINED_UV_CACHE.get(loc_id)


def _get_maintained_payload_for_request(lat: float, lon: float, include_history: bool):
    """
    Return maintained UV payload for nearest supported city when fresh enough.
    For include_history=1, skip maintained cache and keep existing live behavior.
    """
    if include_history:
        return None
    nearest, nearest_dist = _nearest_maintained_location(lat, lon)
    if not nearest:
        return None
    entry = _get_maintained_entry(nearest["id"])
    if not entry:
        return None
    ts = entry.get("timestamp")
    payload = entry.get("payload")
    if ts is None or payload is None:
        MAINTAINED_UV_CACHE.pop(nearest["id"], None)
        return None
    age = time.time() - ts
    if age > MAINTAINED_MAX_SERVE_AGE_SECONDS:
        return None
    out = copy.deepcopy(payload)
    out["last_updated"] = out.get("last_updated") or _iso_utc_now()
    out["data_source"] = "maintained_cache"
    out["maintained_location_id"] = nearest["id"]
    out["maintained_distance_sq"] = round(float(nearest_dist), 6)
    return out


def _get_cached_uv_with_meta(lat: float, lon: float, include_history: bool):
    """
    Return (payload, state, age_seconds) where state is one of:
    - hit
    - miss
    - invalid
    - expired
    """
    key = _make_cache_key(
        lat,
        lon,
        places=UV_CACHE_ROUND_PLACES,
        include_history=include_history,
    )
    entry = UV_CACHE.get(key)
    if not entry:
        return None, "miss", None

    ts = entry.get("timestamp")
    payload = entry.get("payload")
    if ts is None or payload is None:
        UV_CACHE.pop(key, None)
        return None, "invalid", None

    age_seconds = time.time() - ts
    if age_seconds > CACHE_TTL_SECONDS:
        UV_CACHE.pop(key, None)
        return None, "expired", round(age_seconds, 3)

    return payload, "hit", round(age_seconds, 3)


def _get_cached_uv(lat: float, lon: float, include_history: bool):
    """Return cached UV payload for location if still fresh, otherwise None."""
    payload, _, _ = _get_cached_uv_with_meta(
        lat,
        lon,
        include_history=include_history,
    )
    return payload


def _set_cached_uv(lat: float, lon: float, payload: dict, include_history: bool):
    """Store UV payload in cache for the given location."""
    key = _make_cache_key(
        lat,
        lon,
        places=UV_CACHE_ROUND_PLACES,
        include_history=include_history,
    )
    UV_CACHE[key] = {"timestamp": time.time(), "payload": payload}


def _get_stale_cached_uv(lat: float, lon: float, include_history: bool, max_age_seconds: int):
    """Return cached UV payload even if expired, up to max_age_seconds."""
    key = _make_cache_key(
        lat,
        lon,
        places=UV_CACHE_ROUND_PLACES,
        include_history=include_history,
    )
    entry = UV_CACHE.get(key)
    if not entry:
        return None
    ts = entry.get("timestamp")
    payload = entry.get("payload")
    if ts is None or payload is None:
        return None
    age = time.time() - ts
    if age <= max_age_seconds:
        return payload
    return None


def _get_cached_location(lat: float, lon: float):
    """Return cached nearest-location tuple (name, state) if fresh."""
    key = _make_cache_key(lat, lon, places=LOCATION_CACHE_ROUND_PLACES)
    entry = LOCATION_CACHE.get(key)
    if not entry:
        return None
    ts = entry.get("timestamp")
    if ts is None or time.time() - ts > LOCATION_CACHE_TTL_SECONDS:
        LOCATION_CACHE.pop(key, None)
        return None
    return entry.get("value")


def _set_cached_location(lat: float, lon: float, name, state):
    """Store nearest-location tuple (name, state) in cache."""
    key = _make_cache_key(lat, lon, places=LOCATION_CACHE_ROUND_PLACES)
    LOCATION_CACHE[key] = {
        "timestamp": time.time(),
        "value": (name, state),
    }


def _get_nearest_location_name(lat: float, lon: float):
    """Look up the nearest location from the database for display (suburb, state). Returns (name, region) or (None, None)."""
    cached = _get_cached_location(lat, lon)
    if cached is not None:
        return cached

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Prevent slow DB lookup from delaying UV API response too long.
                cur.execute("SET LOCAL statement_timeout = %s;", (1500,))
                cur.execute(
                    """
                    SELECT suburb, state
                    FROM location
                    ORDER BY (latitude - %s) * (latitude - %s) + (longitude - %s) * (longitude - %s)
                    LIMIT 1;
                    """,
                    (lat, lat, lon, lon),
                )
                row = cur.fetchone()
    except Exception:
        _set_cached_location(lat, lon, None, None)
        return None, None
    if not row:
        _set_cached_location(lat, lon, None, None)
        return None, None
    name_state = (row["suburb"], row["state"])
    _set_cached_location(lat, lon, name_state[0], name_state[1])
    return name_state


def _parse_bool(value: str, default: bool = False) -> bool:
    """Parse common truthy query parameter values."""
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _extract_current_uv(data: dict):
    """
    Extract current UV from Open-Meteo payload.

    Priority:
    1) data["current"]["uv_index"] when present
    2) nearest hour from data["hourly"] fallback
    """
    current = data.get("current") or {}
    current_uv = current.get("uv_index")
    if current_uv is not None:
        try:
            return float(current_uv)
        except (TypeError, ValueError):
            pass

    hourly = data.get("hourly") or {}
    hourly_times = hourly.get("time") or []
    hourly_uv = hourly.get("uv_index") or []
    if not hourly_times or not hourly_uv:
        return None

    limit = min(len(hourly_times), len(hourly_uv))
    now_local = datetime.now()
    nearest_idx = None
    nearest_delta = None

    for i in range(limit):
        uv_val = hourly_uv[i]
        t_str = hourly_times[i]
        if uv_val is None or not t_str:
            continue
        try:
            hour_dt = datetime.fromisoformat(t_str)
        except ValueError:
            continue
        delta = abs((hour_dt - now_local).total_seconds())
        if nearest_delta is None or delta < nearest_delta:
            nearest_delta = delta
            nearest_idx = i

    if nearest_idx is None:
        return None

    try:
        return float(hourly_uv[nearest_idx])
    except (TypeError, ValueError):
        return None


def uv_index_to_risk(uv_index):
    """Look up UV risk data from the database.

    Falls back to the previous hard-coded mapping if the database is
    unavailable or no matching range exists. This keeps the endpoint
    backwards compatible while allowing Epic 1 to use the UVRiskLevel
    table when it is populated.
    """

    uv = float(uv_index)

    # Try to use the database table first.
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT risk_level, message, color
                    FROM uv_risk_level
                    WHERE %s BETWEEN min_uv AND max_uv
                    ORDER BY max_uv - min_uv ASC
                    LIMIT 1;
                    """,
                    (uv,),
                )
                row = cur.fetchone()
    except Exception:
        row = None

    if row:
        return {
            "risk_level": row["risk_level"],
            "color": row["color"],
            "message": row["message"],
        }

    # Fallback: WHO/Australian UV range mapping (Epic 1). 0-2 Low, 3-5 Moderate, 6-7 High, 8-10 Very High, 11+ Extreme.
    if uv <= 2:
        return {
            "risk_level": "Low",
            "color": "green",
            "message": (
                "UV levels are low. Minimal sun protection is required. "
                "You can stay outdoors safely, but sunglasses are recommended."
            ),
        }
    if uv <= 5:
        return {
            "risk_level": "Moderate",
            "color": "yellow",
            "message": (
                "Moderate UV levels. Consider wearing sunscreen, sunglasses, and a hat "
                "if you are outside for an extended period."
            ),
        }
    if uv <= 7:
        return {
            "risk_level": "High",
            "color": "orange",
            "message": (
                "High UV levels. Your skin may begin to burn within 20 to 30 minutes. "
                "Apply SPF 30+ sunscreen and seek shade."
            ),
        }
    if uv <= 10:
        return {
            "risk_level": "Very High",
            "color": "red",
            "message": (
                "Very high UV levels. Your skin may burn within 10 to 20 minutes. "
                "Use SPF 50+ sunscreen, wear protective clothing, and limit sun exposure."
            ),
        }
    return {
        "risk_level": "Extreme",
        "color": "purple",
        "message": (
            "Extreme UV levels. Skin damage can occur in less than 10 minutes. "
            "Avoid direct sun exposure and stay in shade whenever possible."
        ),
    }


def _build_uv_payload_from_forecast(
    lat_f: float,
    lon_f: float,
    data: dict,
    include_history: bool,
    location_hint=None,
    state_hint=None,
):
    daily = data.get("daily") or {}
    times = daily.get("time") or []
    uv_max = daily.get("uv_index_max") or []
    uv_clear = daily.get("uv_index_clear_sky_max") or []

    if not times or not uv_max:
        raise ValueError("No daily UV data available for this location")

    date_str = times[0]
    uv_index_val = float(uv_max[0]) if uv_max[0] is not None else 0.0
    uv_clear_val = float(uv_clear[0]) if (uv_clear and uv_clear[0] is not None) else uv_index_val
    current_uv_val = _extract_current_uv(data)

    risk = uv_index_to_risk(uv_index_val)
    current_risk = uv_index_to_risk(current_uv_val) if current_uv_val is not None else None

    daily_max_list = []
    for i in range(min(7, len(times))):
        val = uv_max[i] if i < len(uv_max) and uv_max[i] is not None else 0.0
        daily_max_list.append({"date": times[i], "uv_index_max": float(val)})

    history_list = []
    if include_history:
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=6)
            archive_url = OPEN_METEO_ARCHIVE_URL.format(
                lat=lat_f,
                lon=lon_f,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
            archive_res = requests.get(archive_url, timeout=ARCHIVE_TIMEOUT_SECONDS)
            archive_res.raise_for_status()
            archive_data = archive_res.json() or {}
            archive_daily = archive_data.get("daily") or {}
            archive_times = archive_daily.get("time") or []
            archive_uv = archive_daily.get("uv_index_max") or []
            for i in range(min(7, len(archive_times), len(archive_uv))):
                uv_val = float(archive_uv[i]) if archive_uv[i] is not None else 0.0
                d = date.fromisoformat(archive_times[i])
                history_list.append({
                    "date": archive_times[i],
                    "label": d.strftime("%a"),
                    "uv_index": uv_val,
                })
        except Exception:
            history_list = []

    if location_hint is not None or state_hint is not None:
        location_name = location_hint
        state = state_hint
    else:
        location_name, state = _get_nearest_location_name(lat_f, lon_f)
    region = f"{state} / Australia" if state else None

    payload = {
        "status": "success",
        "date": date_str,
        "latitude": lat_f,
        "longitude": lon_f,
        "current_uv": current_uv_val,
        "current_risk_level": current_risk["risk_level"] if current_risk else None,
        "current_color": current_risk["color"] if current_risk else None,
        "current_message": current_risk["message"] if current_risk else None,
        "uv_index": uv_index_val,
        "uv_index_clear_sky": uv_clear_val,
        "risk_level": risk["risk_level"],
        "color": risk["color"],
        "message": risk["message"],
        "daily": daily_max_list,
        "history": history_list,
        "last_updated": _iso_utc_now(),
    }
    if location_name is not None:
        payload["location_name"] = location_name
    if region is not None:
        payload["region"] = region
    return payload


def _refresh_maintained_location(location_cfg: dict):
    loc_id = location_cfg["id"]
    lat_f = float(location_cfg["latitude"])
    lon_f = float(location_cfg["longitude"])
    normalized_key = _format_cache_key_for_log(
        _make_cache_key(lat_f, lon_f, places=UV_CACHE_ROUND_PLACES, include_history=False)
    )
    if _is_provider_backoff_active(normalized_key):
        _log_uv_debug(
            "maintainer skipped due to provider backoff",
            maintained_location_id=loc_id,
            normalized_key=normalized_key,
        )
        return

    url = OPEN_METEO_URL.format(lat=lat_f, lon=lon_f)
    started_at = time.time()
    try:
        response = requests.get(url, timeout=(2.5, FORECAST_TIMEOUT_SECONDS))
        elapsed_ms = int((time.time() - started_at) * 1000)
        if response.status_code == 429:
            UV_PROVIDER_BACKOFF_UNTIL[normalized_key] = time.time() + OPEN_METEO_429_BACKOFF_SECONDS
            _log_uv_debug(
                "maintainer got 429 from provider",
                maintained_location_id=loc_id,
                normalized_key=normalized_key,
                elapsed_ms=elapsed_ms,
                backoff_seconds=OPEN_METEO_429_BACKOFF_SECONDS,
            )
            return
        response.raise_for_status()
        data = response.json()
        payload = _build_uv_payload_from_forecast(
            lat_f=lat_f,
            lon_f=lon_f,
            data=data,
            include_history=False,
            location_hint=location_cfg["name"],
            state_hint=location_cfg["state"],
        )
        payload["data_source"] = "maintained_refresh"
        payload["maintained_location_id"] = loc_id
        MAINTAINED_UV_CACHE[loc_id] = {"timestamp": time.time(), "payload": payload}
        _set_cached_uv(lat_f, lon_f, payload, include_history=False)
        UV_PROVIDER_BACKOFF_UNTIL.pop(normalized_key, None)
        _log_uv_debug(
            "maintainer refreshed location successfully",
            maintained_location_id=loc_id,
            normalized_key=normalized_key,
            elapsed_ms=elapsed_ms,
        )
    except Exception as exc:
        _log_uv_debug(
            "maintainer refresh failed",
            maintained_location_id=loc_id,
            normalized_key=normalized_key,
            error_type=type(exc).__name__,
            error=_safe_preview(str(exc)),
        )


def _refresh_maintained_uv_once():
    for location_cfg in MAINTAINED_LOCATIONS:
        _refresh_maintained_location(location_cfg)


def start_uv_maintainer(app):
    """Start one background thread per process to refresh maintained UV cache."""
    global _UV_MAINTAINER_THREAD
    with _UV_MAINTAINER_LOCK:
        if _UV_MAINTAINER_THREAD is not None and _UV_MAINTAINER_THREAD.is_alive():
            return

        def _runner():
            while True:
                try:
                    with app.app_context():
                        _log_uv_debug(
                            "maintainer loop tick",
                            refresh_interval_seconds=MAINTAINED_REFRESH_INTERVAL_SECONDS,
                            maintained_locations=",".join(loc["id"] for loc in MAINTAINED_LOCATIONS),
                        )
                        _refresh_maintained_uv_once()
                except Exception as exc:
                    with app.app_context():
                        _log_uv_debug(
                            "maintainer loop error",
                            error_type=type(exc).__name__,
                            error=_safe_preview(str(exc)),
                        )
                time.sleep(max(30, MAINTAINED_REFRESH_INTERVAL_SECONDS))

        _UV_MAINTAINER_THREAD = threading.Thread(
            target=_runner,
            name="uv-maintainer",
            daemon=True,
        )
        _UV_MAINTAINER_THREAD.start()
        with app.app_context():
            _log_uv_debug(
                "maintainer thread started",
                refresh_interval_seconds=MAINTAINED_REFRESH_INTERVAL_SECONDS,
                maintained_locations=",".join(loc["id"] for loc in MAINTAINED_LOCATIONS),
            )


def register_uv_maintainer_startup(app):
    """
    Register a per-worker startup hook so maintainer starts from request-serving context.
    This is safer under Gunicorn/Render than running thread startup directly in create_app().
    """
    with _UV_MAINTAINER_HOOK_LOCK:
        if app.config.get("_UV_MAINTAINER_STARTUP_HOOK_REGISTERED"):
            return

        @app.before_request
        def _ensure_uv_maintainer_running():
            start_uv_maintainer(app)

        app.config["_UV_MAINTAINER_STARTUP_HOOK_REGISTERED"] = True


@uv_bp.route("/api/uv", methods=["GET"])
def get_uv():
    """GET /api/uv?lat=&lon= — Fetch UV from Open-Meteo, return risk and message."""
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat is None or lat == "" or lon is None or lon == "":
        return jsonify({"error": "lat and lon are required"}), 400

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        return jsonify({"error": "lat and lon must be valid numbers"}), 400

    include_history = _parse_bool(request.args.get("include_history"), default=False)
    normalized_uv_key = _make_cache_key(
        lat_f,
        lon_f,
        places=UV_CACHE_ROUND_PLACES,
        include_history=include_history,
    )
    _log_uv_debug(
        "incoming uv request",
        raw_lat=lat,
        raw_lon=lon,
        normalized_key=_format_cache_key_for_log(normalized_uv_key),
        include_history=int(include_history),
        pid=os.getpid(),
        uv_cache_entries=len(UV_CACHE),
    )

    # If we have a fresh cached payload for this location, return it directly.
    cached_payload, cache_state, cache_age = _get_cached_uv_with_meta(
        lat_f,
        lon_f,
        include_history=include_history,
    )
    _log_uv_debug(
        "cache check before external call",
        cache_state=cache_state,
        cache_age_seconds=cache_age,
        include_history=int(include_history),
        lat=round(lat_f, 4),
        lon=round(lon_f, 4),
    )
    if cached_payload is not None:
        _log_uv_debug(
            "cache hit served response",
            include_history=int(include_history),
            lat=round(lat_f, 4),
            lon=round(lon_f, 4),
        )
        return jsonify(cached_payload), 200

    maintained_payload = _get_maintained_payload_for_request(
        lat=lat_f,
        lon=lon_f,
        include_history=include_history,
    )
    if maintained_payload is not None:
        _log_uv_debug(
            "served maintained uv payload",
            include_history=int(include_history),
            requested_lat=round(lat_f, 4),
            requested_lon=round(lon_f, 4),
            maintained_location_id=maintained_payload.get("maintained_location_id"),
            last_updated=maintained_payload.get("last_updated"),
        )
        return jsonify(maintained_payload), 200

    # If this key was recently rate-limited, avoid repeatedly calling Open-Meteo.
    if _is_provider_backoff_active(_format_cache_key_for_log(normalized_uv_key)):
        stale_payload = _get_stale_cached_uv(
            lat_f,
            lon_f,
            include_history=include_history,
            max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
        )
        if stale_payload is not None:
            _log_uv_debug(
                "served stale cache during provider backoff window",
                normalized_key=_format_cache_key_for_log(normalized_uv_key),
                stale_max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
            )
            return jsonify(stale_payload), 200
        return _return_503_with_log(
            reason="provider_backoff_active_and_no_stale_cache",
            user_error="UV service is temporarily busy. Please try again in a few minutes.",
            normalized_key=_format_cache_key_for_log(normalized_uv_key),
            include_history=int(include_history),
        )

    url = OPEN_METEO_URL.format(lat=lat_f, lon=lon_f)

    try:
        # Separate connect/read timeout to fail fast on network stalls while
        # still allowing moderate response time from Open-Meteo.
        started_at = time.time()
        response = requests.get(url, timeout=(2.5, FORECAST_TIMEOUT_SECONDS))
        elapsed_ms = int((time.time() - started_at) * 1000)
        _log_uv_debug(
            "external forecast response received",
            status_code=response.status_code,
            elapsed_ms=elapsed_ms,
            include_history=int(include_history),
            lat=round(lat_f, 4),
            lon=round(lon_f, 4),
            normalized_key=_format_cache_key_for_log(normalized_uv_key),
        )

        # If Open-Meteo rate limits us (HTTP 429), try to fall back to cached data.
        if response.status_code == 429:
            UV_PROVIDER_BACKOFF_UNTIL[_format_cache_key_for_log(normalized_uv_key)] = (
                time.time() + OPEN_METEO_429_BACKOFF_SECONDS
            )
            _log_uv_debug(
                "external rate-limited (429)",
                response_preview=_safe_preview(response.text),
                include_history=int(include_history),
                backoff_seconds=OPEN_METEO_429_BACKOFF_SECONDS,
            )
            # Fresh cache fallback.
            cached_payload, cache_state, cache_age = _get_cached_uv_with_meta(
                lat_f,
                lon_f,
                include_history=include_history,
            )
            if cached_payload is not None:
                _log_uv_debug(
                    "served fresh cache after 429",
                    cache_state=cache_state,
                    cache_age_seconds=cache_age,
                )
                return jsonify(cached_payload), 200
            # Stale cache fallback to keep endpoint stable during temporary rate limits.
            stale_payload = _get_stale_cached_uv(
                lat_f,
                lon_f,
                include_history=include_history,
                max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
            )
            if stale_payload is not None:
                _log_uv_debug(
                    "served stale cache after 429",
                    stale_max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
                )
                return jsonify(stale_payload), 200
            return _return_503_with_log(
                reason="429_and_no_fresh_or_stale_cache",
                user_error="UV service is temporarily busy. Please try again in a few minutes.",
                normalized_key=_format_cache_key_for_log(normalized_uv_key),
                include_history=int(include_history),
            )

        if response.status_code >= 400:
            _log_uv_debug(
                "external non-429 http error",
                status_code=response.status_code,
                response_preview=_safe_preview(response.text),
                normalized_key=_format_cache_key_for_log(normalized_uv_key),
            )

        response.raise_for_status()
        data = response.json()
        UV_PROVIDER_BACKOFF_UNTIL.pop(_format_cache_key_for_log(normalized_uv_key), None)
    except requests.exceptions.RequestException as e:
        _log_uv_debug(
            "external forecast request exception",
            error_type=type(e).__name__,
            error=_safe_preview(str(e)),
            include_history=int(include_history),
        )
        stale_payload = _get_stale_cached_uv(
            lat_f,
            lon_f,
            include_history=include_history,
            max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
        )
        if stale_payload is not None:
            _log_uv_debug(
                "served stale cache after request exception",
                stale_max_age_seconds=STALE_CACHE_MAX_AGE_SECONDS,
            )
            return jsonify(stale_payload), 200
        return jsonify({"error": f"Unable to fetch UV data from Open-Meteo: {str(e)}"}), 500
    except (ValueError, KeyError):
        _log_uv_debug("invalid external forecast payload")
        return jsonify({"error": "Invalid response from UV service"}), 500

    try:
        payload = _build_uv_payload_from_forecast(
            lat_f=lat_f,
            lon_f=lon_f,
            data=data,
            include_history=include_history,
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500

    # Store successful response in cache for this location.
    _set_cached_uv(lat_f, lon_f, payload, include_history=include_history)
    _log_uv_debug(
        "stored successful response in cache",
        include_history=int(include_history),
        cache_ttl_seconds=CACHE_TTL_SECONDS,
        rounded_key_lat=round(lat_f, UV_CACHE_ROUND_PLACES),
        rounded_key_lon=round(lon_f, UV_CACHE_ROUND_PLACES),
    )

    return jsonify(payload), 200
