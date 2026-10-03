from __future__ import annotations

from typing import Any


def normalize_result_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    safe_payload = dict(payload or {})
    rows = safe_payload.get("rows")
    if rows is None:
        safe_payload["rows"] = []
    elif not isinstance(rows, list):
        safe_payload["rows"] = list(rows)

    columns = safe_payload.get("columns") or []
    safe_payload["columns"] = list(columns)
    safe_payload["row_count"] = len(safe_payload["rows"])
    safe_payload["status"] = safe_payload.get("status", "success")
    return safe_payload


def handle_result_error(error: Exception | str) -> dict[str, Any]:
    message = str(error) if not isinstance(error, str) else error
    return {
        "status": "error",
        "message": message,
        "error_type": error.__class__.__name__ if hasattr(error, "__class__") else "Error",
        "rows": [],
        "columns": [],
        "row_count": 0,
    }
