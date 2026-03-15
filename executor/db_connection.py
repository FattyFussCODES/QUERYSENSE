from __future__ import annotations

import mysql.connector

from config.db_config import DBConfig


def create_connection(config: DBConfig, *, connect_to_database: bool = True):
    """Create a MySQL connection.

    If connect_to_database is False, connects to the server without selecting a DB.
    """

    params: dict[str, object] = {
        "host": config.host,
        "port": config.port,
        "user": config.user,
        "password": config.password,
    }
    if connect_to_database:
        params["database"] = config.database

    return mysql.connector.connect(**params)