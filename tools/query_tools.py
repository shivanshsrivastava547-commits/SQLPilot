from __future__ import annotations

import re
from typing import Any

from database.executor import execute_query as execute_db_query
from database.safety import validate_sql as validate_db_sql


def validate_sql(query: str) -> str:
    return validate_db_sql(query)


def generate_query(question: str, schema: dict[str, Any] | None = None) -> str:
    if not question or not question.strip():
        raise ValueError("A user question is required to generate a query.")

    cleaned_question = question.strip()
    question_lower = cleaned_question.lower()

    tables = []
    if isinstance(schema, dict):
        tables = schema.get("tables", [])

    table_name = ""
    if tables:
        for table in tables:
            name = str(table.get("name", "")).lower()
            if any(token in question_lower for token in ["order", "sales", "revenue", "product", "customer"]):
                if any(token in name for token in ["order", "sale", "product", "customer"]):
                    table_name = str(table.get("name", ""))
                    break
        if not table_name:
            table_name = str(tables[0].get("name", ""))

    if not table_name:
        table_name = "data"

    columns = []
    if tables:
        for table in tables:
            if str(table.get("name", "")) == table_name:
                columns = table.get("columns", [])
                break

    metric_column = ""
    for column in columns:
        name = str(column.get("name", "")).lower()
        if name in {"revenue", "amount", "total", "sales", "price", "profit"}:
            metric_column = str(column.get("name", ""))
            break
    if not metric_column:
        for column in columns:
            name = str(column.get("name", "")).lower()
            if "amount" in name or "total" in name or "value" in name:
                metric_column = str(column.get("name", ""))
                break
    if not metric_column and columns:
        metric_column = str(columns[0].get("name", ""))

    dimension_column = ""
    for column in columns:
        name = str(column.get("name", "")).lower()
        if name in {"product", "product_name", "name", "category", "customer", "customer_name", "region"}:
            dimension_column = str(column.get("name", ""))
            break
    if not dimension_column and columns:
        dimension_column = str(columns[1].get("name", "")) if len(columns) > 1 else str(columns[0].get("name", ""))

    if "top" in question_lower or "highest" in question_lower or "best" in question_lower:
        direction = "DESC"
    else:
        direction = "DESC"

    query = (
        f"SELECT {dimension_column}, {metric_column} FROM {table_name} "
        f"ORDER BY {metric_column} {direction} LIMIT 10"
    )

    return validate_sql(query)


def execute_query(query: str, database_url: str | None = None) -> dict[str, Any]:
    return execute_db_query(query, database_url=database_url)
