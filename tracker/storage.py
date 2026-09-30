"""SQLite persistence for speedtest results."""
import sqlite3
from contextlib import contextmanager

from .runner import SpeedResult

DEFAULT_DB = "speedtest.db"


@contextmanager
def _conn(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DEFAULT_DB) -> None:
    with _conn(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                download_mbps   REAL    NOT NULL,
                upload_mbps     REAL    NOT NULL,
                ping_ms         REAL    NOT NULL,
                server_name     TEXT,
                server_country  TEXT,
                timestamp       TEXT    NOT NULL
            )
        """)


def save_result(result: SpeedResult, db_path: str = DEFAULT_DB) -> None:
    init_db(db_path)
    with _conn(db_path) as conn:
        conn.execute(
            "INSERT INTO results (download_mbps, upload_mbps, ping_ms, server_name, server_country, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (result.download_mbps, result.upload_mbps, result.ping_ms,
             result.server_name, result.server_country, result.timestamp),
        )


def fetch_all(limit: int = 100, db_path: str = DEFAULT_DB) -> list[dict]:
    init_db(db_path)
    with _conn(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM results ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
