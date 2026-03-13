"""
UV routes: fetch UV index from Open-Meteo and return risk level and message.
"""
import requests
from flask import Blueprint, jsonify, request

uv_bp = Blueprint("uv_bp", __name__)

# Open-Meteo forecast API (no API key required)
OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&daily=uv_index_max,uv_index_clear_sky_max&timezone=auto"
)


def uv_index_to_risk(uv_index):
    """
    Map UV index value to risk_level, color, and human-readable message.
    Uses the exact Epic 1 mapping for consistency with frontend display.
    """
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
    # 11 or above
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
    """
    GET /api/uv?lat=<latitude>&lon=<longitude>
    Fetches UV data from Open-Meteo for the given coordinates, maps to risk level,
    and returns a JSON payload for the frontend.
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat is None or lat == "" or lon is None or lon == "":
        return jsonify({"error": "lat and lon are required"}), 400

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        return jsonify({"error": "lat and lon must be valid numbers"}), 400

    url = OPEN_METEO_URL.format(lat=lat_f, lon=lon_f)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Unable to fetch UV data from Open-Meteo"}), 500
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

    return jsonify({
        "status": "success",
        "date": date_str,
        "latitude": lat_f,
        "longitude": lon_f,
        "uv_index": uv_index_val,
        "uv_index_clear_sky": uv_clear_val,
        "risk_level": risk["risk_level"],
        "color": risk["color"],
        "message": risk["message"],
    }), 200
