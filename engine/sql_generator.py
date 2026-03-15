from __future__ import annotations


def generate_sql(_intent: str, _entities: list, _conditions: list, *, table: str = "users") -> str:
    return f"SELECT * FROM {table}"
