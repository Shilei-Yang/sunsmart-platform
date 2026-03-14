"""Location search endpoints backed by PostgreSQL.

Provides a simple search API used by the UV dashboard to look up
suburbs / postcodes and resolve them to coordinates.
"""

import json
import time
from flask import Blueprint, jsonify, request

from database.db import get_connection


location_bp = Blueprint("location_bp", __name__)

# #region agent log
DEBUG_LOG_PATH = "/Users/sidharthsudhi/Documents/FIT5120 -IE/Onboarding project/UVibe/sunsmart-platform/.cursor/debug-a9408d.log"
def _debug_log(hypothesis_id, location, message, data):
    try:
        with open(DEBUG_LOG_PATH, "a") as f:
            f.write(json.dumps({"sessionId": "a9408d", "hypothesisId": hypothesis_id, "location": location, "message": message, "data": data, "timestamp": int(time.time() * 1000)}) + "\n")
    except Exception:
        pass
# #endregion


@location_bp.route("/api/location-search", methods=["GET"])
def location_search():
    """Search for locations by suburb name or postcode.

    Query parameters:
    - q: free-text query (required). Matches against suburb (ILIKE) or postcode.

    Response JSON is a list of locations:
    [
      {
        "name": "Melbourne",
        "state": "VIC",
        "country": "Australia",
        "latitude": -37.814,
        "longitude": 144.9633,
        "postcode": "3000"
      },
      ...
    ]
    """

    query = request.args.get("q", "").strip()
    # #region agent log
    _debug_log("H0", "location_routes.py:entry", "route entered", {"q": query})
    # #endregion
    if not query:
        return jsonify({"error": "q query parameter is required"}), 400

    q_like = f"%{query.lower()}%"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT postcode, suburb, state, latitude, longitude
                    FROM location
                    WHERE LOWER(suburb) LIKE %s
                       OR postcode = %s
                    ORDER BY
                        CASE WHEN LOWER(suburb) = %s THEN 0 ELSE 1 END,
                        suburb ASC,
                        postcode ASC
                    LIMIT 20;
                    """,
                    (q_like, query, query.lower()),
                )
                rows = cur.fetchall()
        results = [
            {
                "name": row["suburb"],
                "state": row["state"],
                "country": "Australia",
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "postcode": str(row["postcode"]),
            }
            for row in rows
        ]
    except Exception as exc:  # pragma: no cover - defensive
        # #region agent log
        _debug_log("H1-H5", "location_routes.py:except", "location_search_exception", {"exc_type": type(exc).__name__, "exc_message": str(exc)})
        # #endregion
        return jsonify({"error": f"Database error while searching locations: {exc}"}), 500

    return jsonify(results), 200
