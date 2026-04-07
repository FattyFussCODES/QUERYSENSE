from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:
    kind: str
    value: str


def extract_entities(text: str) -> list[Entity]:
    text_l = text.lower()
    entities: list[Entity] = []

    if any(w in text_l for w in ["student", "students"]):
        entities.append(Entity(kind="table", value="students"))

    # Column mentions
    column_aliases: dict[str, list[str]] = {
        "name": ["name", "names"],
        "course": ["course", "courses", "subject", "subjects"],
        "marks": ["marks", "mark", "score", "scores"],
    }
    for canonical, aliases in column_aliases.items():
        if any(a in text_l for a in aliases):
            entities.append(Entity(kind="column", value=canonical))

    return entities
