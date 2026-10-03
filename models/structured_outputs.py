from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StructuredQueryResult:
    status: str
    columns: list[str] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    row_count: int = 0
    error_type: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "status": self.status,
            "columns": self.columns,
            "rows": self.rows,
            "row_count": self.row_count,
        }
        if self.error_type is not None:
            payload["error_type"] = self.error_type
        if self.message is not None:
            payload["message"] = self.message
        return payload
