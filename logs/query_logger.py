from __future__ import annotations

import datetime as dt
from pathlib import Path


def log_query(sql: str, *, filename: str = "queries.log") -> None:
    Path("logs").mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().isoformat(timespec="seconds")
    with (Path("logs") / filename).open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {sql}\n")
