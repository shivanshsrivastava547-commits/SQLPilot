"""Database access layer package for SQLPilot."""

from database.connection import create_engine, get_connection, test_connection
from database.executor import MAX_QUERY_ROWS, MAX_SQL_REPAIR_ATTEMPTS, QUERY_TIMEOUT, execute_query, execute_read_query
from database.safety import (
    contains_prompt_injection,
    redact_sensitive_data,
    validate_sql,
    validate_user_input,
)
from database.schema_inspector import inspect_database, inspect_relationships, inspect_table

__all__ = [
    "create_engine",
    "get_connection",
    "test_connection",
    "execute_read_query",
    "execute_query",
    "validate_sql",
    "validate_user_input",
    "contains_prompt_injection",
    "redact_sensitive_data",
    "MAX_QUERY_ROWS",
    "QUERY_TIMEOUT",
    "MAX_SQL_REPAIR_ATTEMPTS",
    "inspect_database",
    "inspect_table",
    "inspect_relationships",
]
