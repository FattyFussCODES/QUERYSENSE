from __future__ import annotations

from pathlib import Path

from config.db_config import get_db_config
from executor.db_connection import create_connection


def _run_sql_file(connection, path: Path) -> None:
    sql_text = path.read_text(encoding="utf-8")

    # sqlite3 supports executing multi-statement scripts safely via executescript.
    if connection.__class__.__module__.startswith("sqlite3"):
        connection.executescript(sql_text)
        connection.commit()
        return

    cursor = connection.cursor()
    try:
        for statement in sql_text.split(";"):
            stmt = statement.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
        connection.commit()
    finally:
        cursor.close()


def init_db() -> None:
    """Creates the database (if missing) then applies schema + optional seed data."""

    config = get_db_config()

    if config.dialect == "mysql":
        server_conn = create_connection(config, connect_to_database=False)
        try:
            cur = server_conn.cursor()
            try:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")
            finally:
                cur.close()
        finally:
            server_conn.close()

    db_conn = create_connection(config, connect_to_database=True)
    try:
        base_dir = Path(__file__).resolve().parent
        _run_sql_file(db_conn, base_dir / "schema.sql")

        seed_path = base_dir / "sample_data.sql"
        if seed_path.exists():
            _run_sql_file(db_conn, seed_path)
    finally:
        db_conn.close()
