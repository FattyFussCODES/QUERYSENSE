from __future__ import annotations

from typing import Any

from engine.condition_parser import parse_conditions
from engine.intent_detector import detect_intent
from engine.schema_loader import load_schema
from engine.sql_generator import SQLQuery, generate_sql_query
from executor.query_executor import execute_query
from logs.query_logger import log_query
from nlp.entity_extractor import extract_entities
from nlp.preprocess import preprocess


def run_nl_query(
    connection,
    question: str,
    *,
    table: str = "students",
    log: bool = True,
) -> dict[str, Any]:
    normalized = preprocess(question)

    intent = detect_intent(normalized)
    entities = extract_entities(normalized)
    conditions = parse_conditions(normalized)
    schema = load_schema(connection)

    sql_query: SQLQuery = generate_sql_query(
        intent,
        entities,
        conditions,
        table=table,
        schema=schema,
        original_text=normalized,
    )

    if log:
        log_query(sql_query.sql)

    columns, rows = execute_query(connection, sql_query.sql, sql_query.params)

    return {
        "question": question,
        "normalized": normalized,
        "intent": intent,
        "sql": sql_query.sql,
        "params": list(sql_query.params),
        "columns": columns,
        "rows": rows,
    }
