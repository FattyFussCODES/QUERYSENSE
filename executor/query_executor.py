from __future__ import annotations

from typing import Any, Sequence


def execute_query(connection, sql: str, params: Sequence[Any] | None = None):
	"""Execute a SQL statement and return (columns, rows) for SELECT queries."""

	cursor = connection.cursor()
	try:
		cursor.execute(sql, params or ())

		if cursor.with_rows:
			rows = cursor.fetchall()
			columns = [c[0] for c in (cursor.description or [])]
			return columns, rows

		connection.commit()
		return [], []
	finally:
		cursor.close()