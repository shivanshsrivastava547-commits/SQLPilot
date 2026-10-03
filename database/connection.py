from __future__ import annotations

import os
from functools import lru_cache

from sqlalchemy import Engine, create_engine as sqlalchemy_create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config import settings


def normalize_database_url(database_url: str | None = None) -> str:
    url = (database_url or os.getenv("DATABASE_URL") or settings.database_url or "").strip()
    if not url:
        raise ValueError("Database URL is required. Set DATABASE_URL or pass a valid connection string.")
    return url


def create_engine(database_url: str | None = None, *, read_only: bool = True) -> Engine:
    url = normalize_database_url(database_url)

    engine_kwargs: dict[str, object] = {
        "pool_pre_ping": True,
        "future": True,
    }

    if url.lower().startswith(("postgresql://", "postgresql+psycopg://", "postgres://", "postgres+psycopg://")):
        if read_only:
            engine_kwargs["connect_args"] = {"options": "-c default_transaction_read_only=on"}

    try:
        return sqlalchemy_create_engine(url, **engine_kwargs)
    except (TypeError, ValueError, SQLAlchemyError) as exc:
        raise ValueError(f"Invalid database URL or engine configuration: {exc}") from exc


@lru_cache(maxsize=4)
def get_connection(database_url: str | None = None) -> Engine:
    return create_engine(database_url)


def test_connection(database_url: str | None = None) -> tuple[bool, str]:
    url = normalize_database_url(database_url)

    try:
        engine = create_engine(url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "Database connection successful."
    except Exception as exc:  # pragma: no cover - error path is exercised by users and integration checks
        message = str(exc).strip() or exc.__class__.__name__
        return False, message


test_connection.__test__ = False
