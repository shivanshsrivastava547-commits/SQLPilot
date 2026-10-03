from __future__ import annotations

from typing import Any


def build_hypotheses(question: str, rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    question_text = (question or "").lower()
    base_hypotheses = [
        {
            "name": "Category concentration hypothesis",
            "description": "Revenue is falling because a small set of categories or products is contributing less revenue than before.",
            "evidence_needed": "Compare revenue by category or product over time to find any concentrated drop.",
            "query_hint": "SELECT category, revenue FROM sales_by_category ORDER BY revenue DESC LIMIT 10",
        },
        {
            "name": "Volume decline hypothesis",
            "description": "The business sold fewer units or had less transaction volume, leading to the decline in revenue.",
            "evidence_needed": "Check order counts, unit counts, or transaction totals for the same period.",
            "query_hint": "SELECT date, COUNT(*) AS orders, SUM(revenue) AS revenue FROM transactions GROUP BY date ORDER BY date",
        },
        {
            "name": "Price mix hypothesis",
            "description": "Revenue dropped because the mix shifted toward lower-priced products or lower-margin offerings.",
            "evidence_needed": "Inspect product mix, average selling price, or segment share over time.",
            "query_hint": "SELECT product_segment, AVG(price) AS avg_price, SUM(revenue) AS revenue FROM orders GROUP BY product_segment",
        },
    ]

    if not any(keyword in question_text for keyword in ["why", "decline", "decrease", "drop", "fall"]):
        return [
            {
                "name": "Direct observation hypothesis",
                "description": "The current result set explains the observed change directly.",
                "evidence_needed": "Review the supporting rows and confirm the metric change is consistent with the question.",
                "query_hint": "SELECT * FROM results LIMIT 20",
            }
        ]

    if rows:
        numeric_values = []
        for row in rows:
            for value in row.values():
                if isinstance(value, (int, float)):
                    numeric_values.append(float(value))
        if numeric_values and max(numeric_values) > 0:
            spread = (max(numeric_values) - min(numeric_values)) / max(numeric_values)
            if spread < 0.2:
                base_hypotheses[1]["description"] = "The observed change is small and may reflect a stable but slightly smaller transaction volume rather than a structural shift."

    return base_hypotheses


def evaluate_hypothesis(hypothesis: dict[str, Any], rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if not hypothesis:
        return {"status": "inconclusive", "support_score": 0, "reason": "No hypothesis was supplied."}

    evidence_strength = 60
    if rows:
        numeric_values = []
        for row in rows:
            for value in row.values():
                if isinstance(value, (int, float)):
                    numeric_values.append(float(value))
        if numeric_values:
            spread = max(numeric_values) - min(numeric_values)
            evidence_strength = min(95, max(40, int((spread / max(max(numeric_values), 1.0)) * 100) + 30))

    support_score = min(100, max(0, evidence_strength + (len(hypothesis.get("description", "")) // 10)))
    if support_score >= 75:
        status = "supported"
    elif support_score >= 45:
        status = "inconclusive"
    else:
        status = "unsupported"

    return {
        "status": status,
        "support_score": support_score,
        "reason": hypothesis.get("description", "The hypothesis is plausible but not yet fully proven."),
    }
