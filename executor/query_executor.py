from __future__ import annotations

from typing import Any, Optional, Sequence


def execute_query(connection, sql: str, params: Optional[Sequence[Any]] = None):
	"""Execute a SQL statement and return (columns, rows) for SELECT queries."""

	cursor = connection.cursor()
	try:
		cursor.execute(sql, params or ())

		# Works for both sqlite3 and mysql.connector:
		# - SELECT queries set cursor.description
		# - statements like INSERT/UPDATE/DDL leave it as None
		if cursor.description is not None:
			rows = cursor.fetchall()
			columns = [c[0] for c in cursor.description]
			return columns, rows

		connection.commit()
		return [], []
	finally:
		cursor.close()