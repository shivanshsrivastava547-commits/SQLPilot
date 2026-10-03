from __future__ import annotations

from typing import Any


AMBIGUOUS_DEFINITIONS: dict[str, list[str]] = {
    "best customers": [
        "Highest total spending",
        "Most orders",
        "Highest average order value",
        "Most recent purchases",
    ],
    "best product": [
        "Highest revenue",
        "Highest profit margin",
        "Most units sold",
        "Highest average rating",
    ],
}


def detect_clarification_need(question: str) -> dict[str, Any] | None:
    cleaned = (question or "").strip()
    if not cleaned:
        return None

    lowered = cleaned.lower()

    for phrase, options in AMBIGUOUS_DEFINITIONS.items():
        if phrase in lowered:
            return {
                "question": f'How should "{phrase}" be defined?',
                "options": options,
            }

    if "best customers" in lowered or ("best" in lowered and "customer" in lowered):
        return {
            "question": 'How should "best customers" be defined?',
            "options": AMBIGUOUS_DEFINITIONS["best customers"],
        }

    if "best" in lowered and "product" in lowered:
        return {
            "question": 'How should "best product" be defined?',
            "options": AMBIGUOUS_DEFINITIONS["best product"],
        }

    return None
