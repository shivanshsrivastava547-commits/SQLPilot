from __future__ import annotations

from typing import Any

from analysis.metrics import percentage_change


def _extract_numeric_metric(rows: list[dict[str, Any]], metric_key: str | None = None) -> tuple[str | None, list[float]]:
    if not rows:
        return metric_key, []

    first_row = rows[0]
    if not isinstance(first_row, dict):
        return metric_key, []

    key = metric_key
    if key is None:
        for candidate in first_row:
            if isinstance(first_row[candidate], (int, float)):
                key = candidate
                break

    if key is None:
        return None, []

    values = [float(row.get(key, 0.0)) for row in rows if isinstance(row, dict)]
    return key, values


def build_proactive_insights(rows: list[dict[str, Any]], metric_key: str | None = None) -> list[dict[str, Any]]:
    if not rows:
        return []

    key, values = _extract_numeric_metric(rows, metric_key)
    if not values:
        return []

    first = values[0]
    last = values[-1]
    change = percentage_change(first, last)
    trend = "decline" if last < first else "increase"

    insights: list[dict[str, Any]] = []
    if abs(change) >= 20:
        status = "alert" if abs(change) >= 40 else "watch"
        summary = (
            f"{key or 'The selected metric'} changed by {change:.2f}% from the first observation to the latest one, "
            f"showing a notable {trend}."
        )
        recommendation = "Follow-up investigation is recommended to confirm the underlying driver and check for anomalies."
        insights.append(
            {
                "status": status,
                "summary": summary,
                "metric": key,
                "change_pct": change,
                "recommendation": recommendation,
            }
        )

    if not insights:
        insights.append(
            {
                "status": "stable",
                "summary": f"{key or 'The selected metric'} remains relatively stable across the current observation window.",
                "metric": key,
                "change_pct": change,
                "recommendation": "No immediate follow-up required; continue monitoring the trend over time.",
            }
        )

    return insights
