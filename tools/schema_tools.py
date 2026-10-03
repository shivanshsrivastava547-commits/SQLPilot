from __future__ import annotations

from typing import Any

from database.schema_inspector import inspect_database as _inspect_database
from database.schema_inspector import inspect_relationships as _inspect_relationships
from database.schema_inspector import inspect_table as _inspect_table


def inspect_database(database_url: str | None = None) -> dict[str, Any]:
    return _inspect_database(database_url)


def inspect_table(table_name: str, database_url: str | None = None) -> dict[str, Any]:
    return _inspect_table(table_name, database_url)


def inspect_relationships(database_url: str | None = None) -> list[dict[str, Any]]:
    return _inspect_relationships(database_url)
