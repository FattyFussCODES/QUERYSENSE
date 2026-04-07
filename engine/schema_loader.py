from __future__ import annotations

from typing import Any


def load_schema(connection) -> dict[str, Any]:
    """Load a lightweight schema representation.

    Supports SQLite via PRAGMA introspection. For other DBs, returns an empty schema.
    """

    module_name = connection.__class__.__module__
    if module_name.startswith("sqlite3"):
        cur = connection.cursor()
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in cur.fetchall()]
        finally:
            cur.close()

        schema: dict[str, Any] = {"dialect": "sqlite", "tables": {}}
        for table in tables:
            cur = connection.cursor()
            try:
                cur.execute(f"PRAGMA table_info({table})")
                cols = cur.fetchall()
            finally:
                cur.close()

            columns = [c[1] for c in cols]
            schema["tables"][table] = {"columns": columns}
        return schema

    return {"dialect": "unknown", "tables": {}}
