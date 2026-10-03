from __future__ import annotations

from typing import Any


_METRIC_HINTS = {
    "revenue": "Revenue appears to be a primary business metric in this table.",
    "sales": "This table likely tracks sales volume or value.",
    "orders": "Order counts are present, which is useful for testing volume effects.",
    "amount": "Amount-like data exists and may indicate spend or transaction value.",
    "total": "Total-like data could indicate aggregate business performance.",
    "quantity": "Quantity data can help explain volume shifts.",
}


def build_explore_findings(schema: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not schema:
        return []

    tables = schema.get("tables", []) or []
    findings: list[dict[str, Any]] = []

    for table in tables:
        name = table.get("name", "unknown")
        columns = table.get("columns", []) or []
        column_names = [column.get("name", "") for column in columns]
        metric_labels = []
        for column in columns:
            normalized = str(column.get("name", "")).lower()
            if any(keyword in normalized for keyword in ["revenue", "sales", "orders", "amount", "total", "quantity"]):
                metric_labels.append(column.get("name", ""))

        if not metric_labels:
            continue

        metric_summary = ", ".join(metric_labels[:3])
        findings.append(
            {
                "finding": f"{name} contains metric signals worth investigating: {metric_summary}.",
                "evidence": [
                    f"Table '{name}' includes business-value columns: {metric_summary}.",
                    "The presence of metric columns suggests the table can support trend, mix, and volume analysis.",
                ],
            }
        )

    if not findings:
        findings.append(
            {
                "finding": "No obvious KPI columns were detected in the schema, so the database may require a more targeted exploration.",
                "evidence": [
                    "The available schema does not include revenue-, sales-, or order-like columns.",
                    "A follow-up query could inspect table names and relationships to identify the strongest candidate metrics.",
                ],
            }
        )

    return findings
