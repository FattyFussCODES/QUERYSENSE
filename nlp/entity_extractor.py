from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:
    kind: str
    value: str


def extract_entities(_text: str) -> list[Entity]:
    return []
