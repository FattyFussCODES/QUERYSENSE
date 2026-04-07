from __future__ import annotations

import sqlite3

import mysql.connector

from config.db_config import DBConfig


def create_connection(config: DBConfig, *, connect_to_database: bool = True):
    """Create a DB connection.

    Defaults to SQLite for a self-contained demo.
    """

    if config.dialect == "sqlite":
        # sqlite3 accepts a path; it will create the file if missing.
        conn = sqlite3.connect(config.sqlite_path)
        # Return rows as tuples for compatibility with executor/query_executor.py.
        return conn

    params: dict[str, object] = {
        "host": config.host,
        "port": config.port,
        "user": config.user,
        "password": config.password,
    }
    if connect_to_database:
        params["database"] = config.database

    return mysql.connector.connect(**params)