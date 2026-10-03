from __future__ import annotations

from math import sqrt
from typing import Any


def _numeric_series(rows: list[dict[str, Any]], metric_key: str | None = None) -> list[tuple[dict[str, Any], float]]:
    values: list[tuple[dict[str, Any], float]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = row.get(metric_key) if metric_key else None
        if value is None:
            if metric_key is None:
                for key, candidate in row.items():
                    if isinstance(candidate, (int, float)):
                        value = candidate
                        break
            else:
                continue
        if value is None or not isinstance(value, (int, float)):
            continue
        values.append((row, float(value)))
    return values


def detect_anomalies(rows: list[dict[str, Any]], metric_key: str | None = None) -> list[dict[str, Any]]:
    values = _numeric_series(rows, metric_key)
    if not values:
        return []

    numeric_values = [value for _, value in values]
    mean_value = sum(numeric_values) / len(numeric_values)
    variance = sum((item - mean_value) ** 2 for item in numeric_values) / len(numeric_values)
    std_dev = sqrt(variance) if variance > 0 else 0.0
    median_value = sorted(numeric_values)[len(numeric_values) // 2]
    threshold = max(std_dev * 1.2, abs(mean_value) * 0.35, abs(median_value) * 0.75, 1.0)

    anomalies: list[dict[str, Any]] = []
    for row, value in values:
        if abs(value - mean_value) > threshold or abs(value - median_value) > max(abs(median_value) * 0.75, 1.0):
            anomaly = {
                "row": row,
                "metric_key": metric_key or next((key for key in row if isinstance(row.get(key), (int, float))), None),
                "value": value,
                "deviation_pct": round(((value - mean_value) / mean_value * 100.0) if mean_value else 0.0, 2),
            }
            for key, candidate in row.items():
                if key.lower() in {"month", "date", "day", "period", "name", "customer_id"}:
                    anomaly[key] = candidate
            anomalies.append(anomaly)

    return anomalies


def summarize_data_quality(rows: list[dict[str, Any]], metric_key: str | None = None) -> dict[str, Any]:
    total_rows = len(rows)
    missing_values = 0
    duplicates = 0
    seen: set[tuple[tuple[str, Any], ...]] = set()

    for row in rows:
        if not isinstance(row, dict):
            continue
        if metric_key is not None and row.get(metric_key) is None:
            missing_values += 1
        for key, value in row.items():
            if value is None:
                missing_values += 1
        signature = tuple(sorted((str(key), value) for key, value in row.items() if value is not None))
        if signature in seen:
            duplicates += 1
        seen.add(signature)

    anomaly_count = len(detect_anomalies(rows, metric_key))
    quality_score = max(0, 100 - (missing_values * 12) - (duplicates * 10) - (anomaly_count * 8))

    return {
        "total_rows": total_rows,
        "missing_values": missing_values,
        "duplicate_rows": duplicates,
        "anomaly_count": anomaly_count,
        "quality_score": quality_score,
    }
