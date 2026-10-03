from __future__ import annotations


def percentage_change(start_value: float, end_value: float) -> float:
    if start_value == 0:
        return 0.0 if end_value == 0 else 100.0 if end_value > 0 else -100.0
    return round(((end_value - start_value) / start_value) * 100, 2)


def determine_trend(values: list[float]) -> str:
    if not values:
        return "flat"
    if len(values) == 1:
        return "flat"
    first_value = float(values[0])
    last_value = float(values[-1])
    if last_value > first_value:
        return "up"
    if last_value < first_value:
        return "down"
    return "flat"
