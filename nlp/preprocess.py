from __future__ import annotations


def preprocess(text: str) -> str:
    return " ".join(text.strip().split())
