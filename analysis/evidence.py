from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def create_evidence_entry(
    finding: str,
    query_id: str,
    sql: str,
    result: list[dict[str, Any]] | None,
    purpose: str,
) -> dict[str, Any]:
    return {
        "id": f"{query_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
        "query_id": query_id,
        "finding": finding,
        "sql": sql,
        "purpose": purpose,
        "result": result or [],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
