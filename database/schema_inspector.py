from __future__ import annotations

import copy
from functools import lru_cache
from typing import Any

from sqlalchemy import inspect

from database.connection import create_engine


def _normalize_table_name(table_name: str) -> str:
    if not table_name or not table_name.strip():
        raise ValueError("Table name is required.")
    return table_name.strip()


@lru_cache(maxsize=32)
def _cached_inspect_table(table_name: str, database_url: str | None) -> dict[str, Any]:
    normalized_name = _normalize_table_name(table_name)
    engine = create_engine(database_url, read_only=True)
    inspector = inspect(engine)

    if normalized_name not in inspector.get_table_names():
        raise ValueError(f"Table '{normalized_name}' does not exist in the connected database.")

    primary_key = inspector.get_pk_constraint(normalized_name)
    constrained_columns = primary_key.get("constrained_columns", [])

    columns: list[dict[str, Any]] = []
    for column in inspector.get_columns(normalized_name):
        columns.append(
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": bool(column.get("nullable", True)),
                "default": column.get("default"),
                "primary_key": column["name"] in constrained_columns,
            }
        )

    return {
        "name": normalized_name,
        "columns": columns,
        "data_types": {column["name"]: column["type"] for column in columns},
        "nullable": {column["name"]: column["nullable"] for column in columns},
        "primary_keys": constrained_columns,
    }


@lru_cache(maxsize=16)
def _cached_inspect_relationships(database_url: str | None) -> list[dict[str, Any]]:
    engine = create_engine(database_url, read_only=True)
    inspector = inspect(engine)
    table_names = sorted(inspector.get_table_names())

    relationships: list[dict[str, Any]] = []
    for table_name in table_names:
        for foreign_key in inspector.get_foreign_keys(table_name):
            relationships.append(
                {
                    "table": table_name,
                    "columns": foreign_key.get("constrained_columns", []),
                    "references": {
                        "table": foreign_key.get("referred_table"),
                        "columns": foreign_key.get("referred_columns", []),
                    },
                    "relationship_direction": f"{table_name} -> {foreign_key.get('referred_table')}",
                }
            )

    return sorted(relationships, key=lambda item: (item["table"], item["references"]["table"]))


def inspect_table(table_name: str, database_url: str | None = None) -> dict[str, Any]:
    return copy.deepcopy(_cached_inspect_table(table_name, database_url))


def inspect_relationships(database_url: str | None = None) -> list[dict[str, Any]]:
    return copy.deepcopy(_cached_inspect_relationships(database_url))


@lru_cache(maxsize=8)
def _cached_inspect_database(database_url: str | None) -> dict[str, Any]:
    engine = create_engine(database_url, read_only=True)
    inspector = inspect(engine)

    tables = [_cached_inspect_table(table_name, database_url) for table_name in sorted(inspector.get_table_names())]
    return {
        "tables": tables,
        "relationships": _cached_inspect_relationships(database_url),
    }


def inspect_database(database_url: str | None = None) -> dict[str, Any]:
    return copy.deepcopy(_cached_inspect_database(database_url))


inspect_database.cache_clear = _cached_inspect_database.cache_clear
inspect_database.cache_info = _cached_inspect_database.cache_info
