from __future__ import annotations

import re
from typing import Optional


def detect_intent(text: str) -> str:
    text_l = text.lower()

    if any(k in text_l for k in ["count", "how many", "number of"]):
        return "count"
    if any(k in text_l for k in ["average", "avg", "mean"]):
        return "avg"
    if any(k in text_l for k in ["maximum", "max", "highest", "top"]):
        return "max"
    if any(k in text_l for k in ["minimum", "min", "lowest"]):
        return "min"
    return "select"


def detect_limit(text: str) -> Optional[int]:
    """Extract a LIMIT from queries like 'top 5 students'."""

    m = re.search(r"\btop\s+(\d+)\b", text.lower())
    if not m:
        return None
    try:
        value = int(m.group(1))
        return value if value > 0 else None
    except ValueError:
        return None
