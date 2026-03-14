"""Initialise the PostgreSQL schema for UVibe.

Usage (from the backend directory):

    python -m database.init_db

This script reads `database/schema.sql` and applies it to the database
configured via the DB_* environment variables.
"""

from pathlib import Path

from database.db import get_connection


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def init_schema() -> None:
    if not SCHEMA_PATH.exists():
        raise SystemExit(f"schema file not found: {SCHEMA_PATH}")

    sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print("Database schema initialised successfully.")


if __name__ == "__main__":
    try:
        init_schema()
    except Exception as exc:  # pragma: no cover - CLI safety
        raise SystemExit(f"Failed to initialise database: {exc}")
