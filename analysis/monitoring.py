from __future__ import annotations

from typing import Any

from analysis.metrics import percentage_change


def _extract_numeric_series(rows: list[dict[str, Any]], metric_key: str | None = None) -> tuple[str | None, list[float]]:
    if not rows:
        return metric_key, []

    first_row = rows[0]
    if not isinstance(first_row, dict):
        return metric_key, []

    key = metric_key
    if key is None:
        for candidate_key, value in first_row.items():
            if isinstance(value, (int, float)):
                key = candidate_key
                break

    if key is None:
        return None, []

    values = [float(row.get(key, 0.0)) for row in rows if isinstance(row, dict)]
    return key, values


def build_monitoring_report(
    rows: list[dict[str, Any]],
    metric_key: str | None = None,
    schedule: str = "weekly",
) -> dict[str, Any]:
    metric_name, values = _extract_numeric_series(rows, metric_key)
    if not values:
        return {
            "schedule": schedule,
            "status": "stable",
            "summary": "No numeric metric data was available for the monitoring window.",
            "change_pct": 0.0,
            "notification": "No immediate action required; monitoring window contained no numeric values.",
        }

    start_value = values[0]
    end_value = values[-1]
    change = percentage_change(start_value, end_value)

    if abs(change) >= 40:
        status = "alert"
        summary = (
            f"{metric_name or 'The monitored metric'} changed by {change:.2f}% over the {schedule} monitoring window, "
            f"which is a significant movement that warrants review."
        )
        notification = f"Alert: {metric_name or 'metric'} is up or down by {abs(change):.2f}% over the last {schedule} cycle."
    elif abs(change) >= 20:
        status = "watch"
        summary = (
            f"{metric_name or 'The monitored metric'} changed by {change:.2f}% over the {schedule} monitoring window, "
            "which should be tracked closely."
        )
        notification = f"Watch: {metric_name or 'metric'} has shifted by {abs(change):.2f}% during the current {schedule} cycle."
    else:
        status = "stable"
        summary = (
            f"{metric_name or 'The monitored metric'} remained relatively stable across the {schedule} monitoring window."
        )
        notification = f"Stable: no material shift reported for {metric_name or 'the selected metric'} in the last {schedule} cycle."

    return {
        "schedule": schedule,
        "status": status,
        "summary": summary,
        "metric": metric_name,
        "change_pct": change,
        "notification": notification,
    }
