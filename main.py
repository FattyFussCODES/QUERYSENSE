from __future__ import annotations

import argparse

from config.db_config import get_db_config
from database.init_db import init_db
from engine.query_service import run_nl_query
from executor.db_connection import create_connection
from executor.result_formatter import to_table


def main() -> None:
    parser = argparse.ArgumentParser(description="QuerySense (NL → SQL) demo")
    parser.add_argument("query", nargs="?", help="Natural language query to run")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database schema + seed data")
    args = parser.parse_args()

    if args.init_db and not args.query:
        init_db()
        print("Database initialized.")
        return

    if not args.query:
        parser.error("Provide a query string, or use --init-db")

    init_db()
    config = get_db_config()
    conn = create_connection(config)
    try:
        result = run_nl_query(conn, args.query)
        print("SQL:")
        print(result["sql"])
        print()
        print("Results:")
        print(to_table(result["columns"], result["rows"]))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
