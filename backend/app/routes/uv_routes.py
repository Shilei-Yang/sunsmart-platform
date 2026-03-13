"""
UV routes: fetch UV index from Open-Meteo (no API key) and return risk level and message.
Includes a simple in-memory cache and basic rate-limit handling for robustness.
"""
import time
import requests
from datetime import date, timedelta
from flask import Blueprint, jsonify, request

uv_bp = Blueprint("uv_bp", __name__)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&daily=uv_index_max,uv_index_clear_sky_max&timezone=auto"
)

OPEN_METEO_ARCHIVE_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}"
    "&daily=uv_index_max&timezone=auto"
    "&start_date={start_date}&end_date={end_date}"
)

# Simple in-memory cache for UV responses.
# Key: (rounded_lat, rounded_lon)
# Value: {"timestamp": float, "payload": dict}
UV_CACHE = {}
CACHE_TTL_SECONDS = 600  # 10 minutes


def _make_cache_key(lat: float, lon: float, places: int = 2):
    """Build a cache key from rounded latitude/longitude."""
    return (round(float(lat), places), round(float(lon), places))


def _get_cached_uv(lat: float, lon: float):
    """Return cached UV payload for location if still fresh, otherwise None."""
    key = _make_cache_key(lat, lon)
    entry = UV_CACHE.get(key)
    if not entry:
        return None
    ts = entry.get("timestamp")
    payload = entry.get("payload")
    if ts is None or payload is None:
        return None
    if time.time() - ts > CACHE_TTL_SECONDS:
        # Expired entry; remove and treat as cache miss.
        UV_CACHE.pop(key, None)
        return None
    return payload


def _set_cached_uv(lat: float, lon: float, payload: dict):
    """Store UV payload in cache for the given location."""
    key = _make_cache_key(lat, lon)
    UV_CACHE[key] = {"timestamp": time.time(), "payload": payload}

def uv_index_to_risk(uv_index):
    """Map UV index to risk_level, color, and message for frontend display."""
    uv = float(uv_index)
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

    # If we have a fresh cached payload for this location, return it directly.
    cached_payload = _get_cached_uv(lat_f, lon_f)
    if cached_payload is not None:
        return jsonify(cached_payload), 200

    url = OPEN_METEO_URL.format(lat=lat_f, lon=lon_f)

    try:
        response = requests.get(url, timeout=10)

        # If Open-Meteo rate limits us (HTTP 429), try to fall back to cached data.
        if response.status_code == 429:
            cached_payload = _get_cached_uv(lat_f, lon_f)
            if cached_payload is not None:
                return jsonify(cached_payload), 200
            return jsonify({
                "error": "UV service is temporarily busy. Please try again in a few minutes."
            }), 503

        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Unable to fetch UV data from Open-Meteo: {str(e)}"}), 500
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid response from UV service"}), 500

    daily = data.get("daily") or {}
    times = daily.get("time") or []
    uv_max = daily.get("uv_index_max") or []
    uv_clear = daily.get("uv_index_clear_sky_max") or []

    if not times or not uv_max:
        return jsonify({"error": "No daily UV data available for this location"}), 500

    date_str = times[0]
    uv_index_val = float(uv_max[0]) if uv_max[0] is not None else 0.0
    uv_clear_val = float(uv_clear[0]) if (uv_clear and uv_clear[0] is not None) else uv_index_val

    risk = uv_index_to_risk(uv_index_val)

    # Build 7-day daily max UV for frontend max UV graph (bar chart)
    daily_max_list = []
    for i in range(min(7, len(times))):
        val = uv_max[i] if i < len(uv_max) and uv_max[i] is not None else 0.0
        daily_max_list.append({"date": times[i], "uv_index_max": float(val)})

    # Past 7 days history (for "Past" tab). Best-effort: if archive fails, return empty history.
    history_list = []
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=6)
        archive_url = OPEN_METEO_ARCHIVE_URL.format(
            lat=lat_f,
            lon=lon_f,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        archive_res = requests.get(archive_url, timeout=10)
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

    # Build final response payload (structure unchanged from previous implementation).
    payload = {
        "status": "success",
        "date": date_str,
        "latitude": lat_f,
        "longitude": lon_f,
        "uv_index": uv_index_val,
        "uv_index_clear_sky": uv_clear_val,
        "risk_level": risk["risk_level"],
        "color": risk["color"],
        "message": risk["message"],
        "daily": daily_max_list,
        "history": history_list,
    }

    # Store successful response in cache for this location.
    _set_cached_uv(lat_f, lon_f, payload)

    return jsonify(payload), 200
