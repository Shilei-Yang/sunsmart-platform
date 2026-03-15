"""Import prepared CSV datasets into PostgreSQL.

Usage (from the backend directory):

    python -m database.import_datasets

Imports:
- `database/australian_postcodes_cleaned.csv` -> location table
- `database/uv_risk_levels.csv` -> uv_risk_level table

Safe to re-run: rows are upserted using ON CONFLICT.
"""

import csv
from pathlib import Path

from database.db import get_connection
from psycopg2.extras import execute_values

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "database"

POSTCODES_CSV = DATA_DIR / "australian_postcodes_cleaned.csv"
UV_RISK_CSV = DATA_DIR / "uv_risk_levels.csv"
LOCATION_BATCH_SIZE = 1000


def _chunked(items, size):
    """Yield fixed-size chunks from a list."""
    for idx in range(0, len(items), size):
        yield items[idx : idx + size]


def import_locations() -> None:
    print("[location] Import started.")
    print(f"[location] Source file: {POSTCODES_CSV}")

    if not POSTCODES_CSV.exists():
        print(f"[location] Skipped – CSV not found: {POSTCODES_CSV}")
        return

    rows_to_import = []
    seen_keys = set()
    skipped = 0
    duplicates_removed = 0

    with POSTCODES_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            postcode = row.get("postcode")
            suburb = row.get("suburb")
            state = row.get("state")
            lat = row.get("lat")
            lon = row.get("lon")

            if not (postcode and suburb and state and lat and lon):
                skipped += 1
                continue

            dedupe_key = (postcode.strip(), suburb.strip().lower())
            if dedupe_key in seen_keys:
                duplicates_removed += 1
                continue

            try:
                rows_to_import.append((postcode, suburb, state, float(lat), float(lon)))
                seen_keys.add(dedupe_key)
            except ValueError:
                skipped += 1

    total_rows = len(rows_to_import)
    print(f"[location] Total valid rows loaded: {total_rows}")
    print(f"[location] Total skipped rows: {skipped}")
    print(f"[location] Total duplicate rows removed: {duplicates_removed}")

    if total_rows == 0:
        print("[location] No valid rows to import.")
        return

    upsert_sql = """
        INSERT INTO location (postcode, suburb, state, latitude, longitude)
        VALUES %s
        ON CONFLICT (postcode, suburb, state)
        DO UPDATE SET latitude = EXCLUDED.latitude,
                      longitude = EXCLUDED.longitude;
    """

    imported = 0
    with get_connection() as conn:
        with conn.cursor() as cur:
            for batch in _chunked(rows_to_import, LOCATION_BATCH_SIZE):
                execute_values(
                    cur,
                    upsert_sql,
                    batch,
                    page_size=LOCATION_BATCH_SIZE,
                )
                imported += len(batch)
                print(f"[location] Batch progress: {imported}/{total_rows}")
        conn.commit()

    print(f"[location] Imported/updated {imported} rows from {POSTCODES_CSV.name}")
    print("[location] Import finished.")


def import_uv_risk_levels() -> None:
    if not UV_RISK_CSV.exists():
        print(f"[uv_risk_level] Skipped – CSV not found: {UV_RISK_CSV}")
        return

    count = 0
    with get_connection() as conn:
        with conn.cursor() as cur:
            with UV_RISK_CSV.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category = row.get("category")
                    min_uv = row.get("min_uv")
                    max_uv = row.get("max_uv")

                    if not (category and min_uv and max_uv):
                        continue

                    # Map CSV category to display fields.
                    risk_level = category
                    color = {
                        "Low": "green",
                        "Moderate": "yellow",
                        "High": "orange",
                        "Very High": "red",
                        "Extreme": "purple",
                    }.get(category, "yellow")

                    # Basic messages aligned with existing uv_index_to_risk logic.
                    default_messages = {
                        "Low": "UV levels are low. Minimal sun protection is required. You can stay outdoors safely, but sunglasses are recommended.",
                        "Moderate": "Moderate UV levels. Consider wearing sunscreen, sunglasses, and a hat if you are outside for an extended period.",
                        "High": "High UV levels. Your skin may begin to burn within 20 to 30 minutes. Apply SPF 30+ sunscreen and seek shade.",
                        "Very High": "Very high UV levels. Your skin may burn within 10 to 20 minutes. Use SPF 50+ sunscreen, wear protective clothing, and limit sun exposure.",
                        "Extreme": "Extreme UV levels. Skin damage can occur in less than 10 minutes. Avoid direct sun exposure and stay in shade whenever possible.",
                    }

                    message = default_messages.get(category, "Check local UV guidance for protection recommendations.")

                    cur.execute(
                        """
                        INSERT INTO uv_risk_level (min_uv, max_uv, risk_level, message, color)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (min_uv, max_uv)
                        DO UPDATE SET risk_level = EXCLUDED.risk_level,
                                      message    = EXCLUDED.message,
                                      color      = EXCLUDED.color;
                        """,
                        (float(min_uv), float(max_uv), risk_level, message, color),
                    )
                    count += 1
        conn.commit()

    print(f"[uv_risk_level] Imported/updated {count} rows from {UV_RISK_CSV.name}")


def main() -> None:
    import_locations()
    import_uv_risk_levels()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI safety
        raise SystemExit(f"Dataset import failed: {exc}")
