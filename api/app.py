from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from config.db_config import get_db_config
from database.init_db import init_db
from engine.query_service import run_nl_query
from executor.db_connection import create_connection
from executor.result_formatter import to_records


def create_app():
    app = FastAPI(title="QuerySense", version="0.1.0")

    class QueryRequest(BaseModel):
        query: str = Field(..., min_length=1)
        preview_sql: bool = True

    class QueryResponse(BaseModel):
        sql: str
        columns: list[str]
        rows: list[list[object]]
        records: list[dict[str, object]]

    @app.on_event("startup")
    def _startup() -> None:
        # Ensure DB exists with schema + seed.
        init_db()

    @app.get("/health")
    def health() -> dict[str, str]:
        config = get_db_config()
        return {"status": "ok", "dialect": config.dialect}

    @app.post("/query", response_model=QueryResponse)
    def query(req: QueryRequest) -> QueryResponse:
        config = get_db_config()
        conn = create_connection(config)
        try:
            result = run_nl_query(conn, req.query)
            columns = result["columns"]
            rows = [list(r) for r in result["rows"]]
            records = to_records(columns, rows)
            return QueryResponse(sql=result["sql"], columns=columns, rows=rows, records=records)
        finally:
            conn.close()

    return app
