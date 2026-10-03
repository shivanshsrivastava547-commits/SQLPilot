import pytest

from database.connection import create_engine, get_connection, test_connection
from database.safety import validate_sql


def test_create_engine_supports_sqlite_memory_for_local_validation():
    engine = create_engine("sqlite:///:memory:")
    assert engine is not None


def test_test_connection_accepts_valid_sqlite_url():
    is_ok, message = test_connection("sqlite:///:memory:")
    assert is_ok is True
    assert "successful" in message.lower()


def test_get_connection_returns_engine_for_sqlite_memory():
    engine = get_connection("sqlite:///:memory:")
    assert engine is not None


def test_validate_sql_rejects_dangerous_statements():
    with pytest.raises(ValueError):
        validate_sql("DROP TABLE users;")

    with pytest.raises(ValueError):
        validate_sql("UPDATE users SET name = 'x';")
