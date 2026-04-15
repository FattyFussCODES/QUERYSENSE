from __future__ import annotations

from typing import Any

from engine.llm_sql_generator import generate_sql_from_llm
from engine.schema_loader import load_schema
from executor.query_executor import execute_query
from logs.query_logger import log_query


def run_nl_query(
    connection,
    question: str,
    *,
    table: str = "students",
    log: bool = True,
) -> dict[str, Any]:
    
    schema = load_schema(connection)
    
    # Utilize Generative AI for SQL Translation
    sql = generate_sql_from_llm(question, schema, table)
    
    if log:
        log_query(sql)

    columns, rows = execute_query(connection, sql, ())

    return {
        "question": question,
        "normalized": question,
        "intent": "llm",
        "sql": sql,
        "params": [],
        "columns": columns,
        "rows": rows,
    }
