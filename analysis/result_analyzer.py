from __future__ import annotations

from typing import Any

from analysis.metrics import determine_trend, percentage_change


def _extract_numeric_series(rows: list[dict[str, Any]], metric_key: str | None = None) -> tuple[str | None, list[float]]:
    if not rows:
        return metric_key, []

    first_row = rows[0]
    if isinstance(first_row, dict):
        candidate_keys = [metric_key] if metric_key else []
        if not candidate_keys:
            for key in first_row.keys():
                value = first_row.get(key)
                if isinstance(value, (int, float)):
                    candidate_keys.append(key)
                    break
        if not candidate_keys:
            return None, []
        key = candidate_keys[0]
        values = [float(row.get(key, 0.0)) for row in rows if isinstance(row, dict) and row.get(key) is not None]
        return key, values
    return None, []


def analyze_query_result(rows: list[dict[str, Any]], metric_key: str | None = None) -> dict[str, Any]:
    if not rows:
        return {
            "metric": metric_key,
            "trend": "flat",
            "summary": "No rows were returned for this query, so there is no evidence to analyze.",
            "change_pct": 0.0,
            "values": [],
        }

    metric_name, values = _extract_numeric_series(rows, metric_key)
    if not values:
        return {
            "metric": metric_name,
            "trend": "flat",
            "summary": "The result set did not include usable numeric values for trend analysis.",
            "change_pct": 0.0,
            "values": [],
        }

    start_value = values[0]
    end_value = values[-1]
    change_pct = percentage_change(start_value, end_value)
    trend = determine_trend(values)

    if metric_name:
        summary = (
            f"The {metric_name} metric moved by {change_pct:.2f}% from {start_value} to {end_value}, "
            f"indicating a {trend} trend."
        )
    else:
        summary = (
            f"The reported values moved by {change_pct:.2f}% from {start_value} to {end_value}, "
            f"indicating a {trend} trend."
        )

    return {
        "metric": metric_name,
        "trend": trend,
        "summary": summary,
        "change_pct": change_pct,
        "values": values,
    }
