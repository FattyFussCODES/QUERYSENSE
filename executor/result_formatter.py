from __future__ import annotations

from typing import Any, Iterable


def to_records(columns: list[str], rows: Iterable[Iterable[Any]]) -> list[dict[str, Any]]:
	"""Convert (columns, rows) into JSON-friendly list-of-dicts."""
	col_list = list(columns)
	return [dict(zip(col_list, list(row))) for row in rows]


def to_table(columns: list[str], rows: Iterable[Iterable[Any]]) -> str:
	"""Render a minimal fixed-width table for CLI output."""
	rows_list = [list(r) for r in rows]
	cols = list(columns)
	if not cols:
		return "(no columns)"
	widths = [len(str(c)) for c in cols]
	for r in rows_list:
		for i, v in enumerate(r):
			widths[i] = max(widths[i], len(str(v)))

	def fmt_row(values: list[Any]) -> str:
		return " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(values))

	header = fmt_row(cols)
	sep = "-+-".join("-" * w for w in widths)
	body = "\n".join(fmt_row(r) for r in rows_list)
	return "\n".join([header, sep, body]) if body else "\n".join([header, sep])