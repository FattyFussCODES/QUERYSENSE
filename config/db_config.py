from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


@dataclass(frozen=True)
class DBConfig:
    dialect: Literal["sqlite", "mysql"]
    sqlite_path: str
    host: str
    port: int
    user: str
    password: str
    database: str


def get_db_config() -> DBConfig:
    load_dotenv(override=False)

    dialect = (os.getenv("DB_DIALECT", "sqlite") or "sqlite").strip().lower()
    if dialect not in {"sqlite", "mysql"}:
        dialect = "sqlite"

    default_sqlite_path = str(Path("database") / "querysense.db")
    sqlite_path = os.getenv("DB_PATH", default_sqlite_path)

    host = os.getenv("DB_HOST", "localhost")
    port_str = os.getenv("DB_PORT", "3306")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "QuerySense")

    try:
        port = int(port_str)
    except ValueError:
        port = 3306

    return DBConfig(
        dialect=dialect,
        sqlite_path=sqlite_path,
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )