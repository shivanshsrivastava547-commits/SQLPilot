from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy import text

from database.connection import get_connection
from database.safety import validate_sql
from models.structured_outputs import StructuredQueryResult

MAX_QUERY_ROWS = 500
QUERY_TIMEOUT = 30
MAX_SQL_REPAIR_ATTEMPTS = 2


def execute_read_query(query: str, database_url: str | None = None) -> pd.DataFrame:
    validated_query = validate_sql(query)
    engine = get_connection(database_url)

    with engine.connect() as connection:
        rows = connection.execution_options(timeout=QUERY_TIMEOUT).execute(text(validated_query)).mappings().all()

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows[:MAX_QUERY_ROWS])


def execute_query(query: str, database_url: str | None = None) -> dict[str, Any]:
    try:
        validated_query = validate_sql(query)
        engine = get_connection(database_url)

        with engine.connect() as connection:
            result = connection.execution_options(timeout=QUERY_TIMEOUT).execute(text(validated_query))
            rows = [dict(row) for row in result.mappings().all()]
            columns = list(result.keys())

        capped_rows = rows[:MAX_QUERY_ROWS]
        structured_result = StructuredQueryResult(
            status="success",
            columns=columns,
            rows=capped_rows,
            row_count=len(capped_rows),
        )
        return structured_result.to_dict()
    except Exception as exc:
        structured_result = StructuredQueryResult(
            status="error",
            error_type=exc.__class__.__name__,
            message=str(exc),
        )
        return structured_result.to_dict()
