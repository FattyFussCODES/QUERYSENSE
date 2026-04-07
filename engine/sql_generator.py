from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from engine.condition_parser import Condition
from engine.intent_detector import detect_limit
from nlp.entity_extractor import Entity


@dataclass(frozen=True)
class SQLQuery:
    sql: str
    params: tuple[Any, ...] = ()


def _whitelist_columns(schema: Optional[dict], table: str) -> set[str]:
    try:
        cols = schema.get("tables", {}).get(table, {}).get("columns", []) if schema else []
        return {str(c) for c in cols}
    except Exception:
        return set()


def generate_sql_query(
    intent: str,
    entities: Iterable[Entity],
    conditions: Iterable[Condition],
    *,
    table: str = "students",
    schema: Optional[dict] = None,
    original_text: Optional[str] = None,
) -> SQLQuery:
    allowed_cols = _whitelist_columns(schema, table)
    if not allowed_cols:
        allowed_cols = {"student_id", "name", "course", "marks"}

    requested_cols = [e.value for e in entities if getattr(e, "kind", None) == "column" and e.value in allowed_cols]
    requested_cols = list(dict.fromkeys(requested_cols))  # preserve order, de-dupe

    params: list[Any] = []
    where_clauses: list[str] = []
    for cond in conditions:
        if cond.column not in allowed_cols:
            continue
        if cond.op not in {"=", ">", "<", ">=", "<="}:
            continue
        where_clauses.append(f"{cond.column} {cond.op} ?")
        params.append(cond.value)

    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)

    order_sql = ""
    limit_sql = ""
    limit = detect_limit(original_text or "") if original_text else None

    if intent in {"max", "min"} or limit is not None:
        direction = "DESC" if intent == "max" or limit is not None else "ASC"
        order_sql = f" ORDER BY marks {direction}"
        if limit is not None:
            limit_sql = " LIMIT ?"
            params.append(limit)
        elif intent in {"max", "min"}:
            limit_sql = " LIMIT 1"

    if intent == "count":
        select_sql = "COUNT(*) AS count"
        return SQLQuery(sql=f"SELECT {select_sql} FROM {table}{where_sql}", params=tuple(params))

    if intent == "avg":
        select_sql = "AVG(marks) AS avg_marks"
        return SQLQuery(sql=f"SELECT {select_sql} FROM {table}{where_sql}", params=tuple(params))

    if intent in {"max", "min"}:
        # When asking for highest/lowest, return the row(s) for context.
        select_cols = requested_cols or ["name", "course", "marks"]
        select_sql = ", ".join(select_cols)
        return SQLQuery(
            sql=f"SELECT {select_sql} FROM {table}{where_sql}{order_sql}{limit_sql}",
            params=tuple(params),
        )

    select_sql = ", ".join(requested_cols) if requested_cols else "*"
    return SQLQuery(sql=f"SELECT {select_sql} FROM {table}{where_sql}{order_sql}{limit_sql}", params=tuple(params))


def generate_sql(intent: str, entities: list, conditions: list, *, table: str = "students") -> str:
    """Backwards-compatible helper returning only the SQL string."""
    return generate_sql_query(intent, entities, conditions, table=table).sql
