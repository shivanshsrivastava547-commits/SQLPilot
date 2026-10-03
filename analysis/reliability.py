from __future__ import annotations

from typing import Any

from database.safety import validate_sql


def build_reliability_report(schema: dict[str, Any] | None, query: str | None = None) -> dict[str, Any]:
    tables = (schema or {}).get("tables", []) if isinstance(schema, dict) else []
    checks = {
        "schema_present": bool(tables),
        "sql_safe": True,
        "read_only_query": True,
    }
    issues: list[str] = []

    if not checks["schema_present"]:
        issues.append("Database schema is not available for validation.")

    if query:
        try:
            validate_sql(query)
        except ValueError as exc:
            checks["sql_safe"] = False
            checks["read_only_query"] = False
            issues.append(str(exc))

    status = "healthy" if not issues else "warning"
    return {
        "status": status,
        "checks": checks,
        "issues": issues,
    }
