from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    column: str
    op: str
    value: object


def parse_conditions(text: str) -> list[Condition]:
    text_l = text.lower()
    conditions: list[Condition] = []

    # marks comparisons
    marks_patterns: list[tuple[str, str]] = [
        (r"\bmarks\s*(?:>=|greater than or equal to|at least)\s*(\d+)\b", ">="),
        (r"\bmarks\s*(?:<=|less than or equal to|at most)\s*(\d+)\b", "<="),
        (r"\bmarks\s*(?:>|above|over|greater than|more than)\s*(\d+)\b", ">"),
        (r"\bmarks\s*(?:<|below|under|less than)\s*(\d+)\b", "<"),
        (r"\bmarks\s*(?:=|equal to|equals)\s*(\d+)\b", "="),
    ]
    for pattern, op in marks_patterns:
        m = re.search(pattern, text_l)
        if m:
            conditions.append(Condition(column="marks", op=op, value=int(m.group(1))))
            break

    # course equality: "in AI", "course AI", "enrolled in DBMS"
    # Prefer quoted values: course "AI"
    m = re.search(r"\bcourse\s*[=:]?\s*['\"]([^'\"]+)['\"]", text, flags=re.IGNORECASE)
    if m:
        conditions.append(Condition(column="course", op="=", value=m.group(1).strip()))
        return conditions

    m = re.search(r"\b(?:in|enrolled in)\s+([a-zA-Z][\w-]*)\b", text_l)
    if m and m.group(1) not in {"students", "student", "course", "marks"}:
        # Keep original casing best-effort by slicing from original text
        val = m.group(1)
        conditions.append(Condition(column="course", op="=", value=val.upper() if val.isalpha() and val.islower() else val))

    return conditions
