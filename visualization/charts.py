from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


TIME_KEYS = {"month", "months", "date", "dates", "day", "days", "week", "weeks", "period", "periods", "time"}


def choose_chart_type(rows: list[dict[str, Any]], x_key: str | None = None, y_key: str | None = None) -> str:
    if not rows:
        return "table"

    first_row = rows[0]
    keys = list(first_row.keys())
    if x_key is None:
        for key in keys:
            lowered = key.lower()
            if lowered in TIME_KEYS:
                x_key = key
                break
    if y_key is None:
        for key in keys:
            value = first_row.get(key)
            if isinstance(value, (int, float)) and key.lower() not in {"id"}:
                y_key = key
                break

    if not x_key or not y_key:
        return "bar" if y_key else "table"

    if x_key.lower() in TIME_KEYS:
        return "line"

    if len(keys) >= 2 and x_key in keys and y_key in keys:
        return "bar"

    return "scatter"


def build_chart(rows: list[dict[str, Any]], x_key: str | None = None, y_key: str | None = None) -> dict[str, Any]:
    if not rows:
        return {"type": "table", "data": [], "layout": {}}

    chart_type = choose_chart_type(rows, x_key=x_key, y_key=y_key)

    if x_key is None:
        x_key = next((key for key in rows[0].keys() if key.lower() in TIME_KEYS), None)
    if y_key is None:
        y_key = next((key for key in rows[0].keys() if isinstance(rows[0].get(key), (int, float)) and key.lower() not in {"id"}), None)

    if not x_key or not y_key:
        return {"type": "table", "data": [], "layout": {}}

    x_values = [row.get(x_key) for row in rows]
    y_values = [float(row.get(y_key, 0.0)) for row in rows]

    if chart_type == "line":
        fig = go.Figure(data=[go.Scatter(x=x_values, y=y_values, mode="lines+markers", name=y_key)])
    elif chart_type == "scatter":
        fig = go.Figure(data=[go.Scatter(x=y_values, y=x_values, mode="markers", name=x_key)])
    else:
        fig = go.Figure(data=[go.Bar(x=x_values, y=y_values, name=y_key)])

    fig.update_layout(
        title=f"{y_key} by {x_key}",
        xaxis_title=x_key,
        yaxis_title=y_key,
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
    )

    chart = fig.to_dict()
    chart["type"] = chart_type
    if chart.get("layout", {}).get("xaxis"):
        chart["layout"]["xaxis"]["title"] = x_key
    if chart.get("layout", {}).get("yaxis"):
        chart["layout"]["yaxis"]["title"] = y_key
    return chart
