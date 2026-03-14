"""Location search endpoints backed by PostgreSQL."""

import time
from flask import Blueprint, jsonify, request

from database.db import get_connection


location_bp = Blueprint("location_bp", __name__)
SEARCH_CACHE = {}
SEARCH_CACHE_TTL_SECONDS = 120  # 2 minutes


def _get_cached_search(query: str):
    """Return cached location search results for query if fresh."""
    entry = SEARCH_CACHE.get(query)
    if not entry:
        return None
    ts = entry.get("timestamp")
    results = entry.get("results")
    if ts is None or results is None or time.time() - ts > SEARCH_CACHE_TTL_SECONDS:
        SEARCH_CACHE.pop(query, None)
        return None
    return results


def _set_cached_search(query: str, results):
    """Store location search results in cache."""
    SEARCH_CACHE[query] = {
        "timestamp": time.time(),
        "results": results,
    }


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
    if not query:
        return jsonify({"error": "q query parameter is required"}), 400

    # Single-character fuzzy search causes expensive scans and poor UX latency.
    if len(query) < 2:
        return jsonify([]), 200

    query_lower = query.lower()
    cached = _get_cached_search(query_lower)
    if cached is not None:
        return jsonify(cached), 200

    q_like = f"%{query.lower()}%"
    q_prefix = f"{query.lower()}%"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT postcode, suburb, state, latitude, longitude
                    FROM location
                    WHERE LOWER(suburb) LIKE %s
                       OR LOWER(suburb) LIKE %s
                       OR postcode = %s
                    ORDER BY
                        CASE
                            WHEN postcode = %s THEN 0
                            WHEN LOWER(suburb) = %s THEN 1
                            WHEN LOWER(suburb) LIKE %s THEN 2
                            ELSE 3
                        END,
                        suburb ASC,
                        postcode ASC
                    LIMIT 20;
                    """,
                    (q_prefix, q_like, query, query, query_lower, q_prefix),
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
        return jsonify({"error": f"Database error while searching locations: {exc}"}), 500

    _set_cached_search(query_lower, results)
    return jsonify(results), 200
