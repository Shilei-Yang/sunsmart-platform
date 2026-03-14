"""Database helper for PostgreSQL connections.

Uses environment variables for configuration so the same code works locally,
for tests, and in deployment:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD

This module exposes a small helper `get_connection()` that opens a new
psycopg2 connection. Callers should use it in a context manager and close
cursors / connections promptly.
"""

import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def _get_db_config():
    """Read database settings from the environment.

    Raises a clear RuntimeError if any required variable is missing so that
    misconfiguration fails fast on startup or first DB use.
    """

    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing database configuration env vars: " + ", ".join(missing)
        )

    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


@contextmanager
def get_connection(cursor_factory=RealDictCursor):
    """Yield a PostgreSQL connection with a dict-style cursor.

    Usage:

    >>> from database.db import get_connection
    >>> with get_connection() as conn:
    ...     with conn.cursor() as cur:
    ...         cur.execute("SELECT 1")
    ...         row = cur.fetchone()

    All connections are created on demand using env vars. This keeps the
    implementation simple and is sufficient for the current project scale.
    """

    cfg = _get_db_config()

    conn = psycopg2.connect(cursor_factory=cursor_factory, **cfg)
    try:
        yield conn
    finally:
        conn.close()
