import tempfile

from sqlalchemy import text

from database.connection import create_engine
from database.schema_inspector import inspect_database, inspect_relationships, inspect_table


def build_sqlite_database():
    temp_db = tempfile.NamedTemporaryFile(prefix="sqlpilot_schema_", suffix=".db", delete=False)
    temp_db.close()
    database_url = f"sqlite:///{temp_db.name}"

    engine = create_engine(database_url)
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"))
        connection.execute(
            text(
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, "
                "FOREIGN KEY (customer_id) REFERENCES customers(id))"
            )
        )

    return database_url


def test_inspect_database_returns_schema_snapshot():
    database_url = build_sqlite_database()
    db_info = inspect_database(database_url)

    assert {table["name"] for table in db_info["tables"]} == {"customers", "orders"}
    assert any(column["name"] == "id" for column in db_info["tables"][0]["columns"])
    assert "relationships" in db_info


def test_inspect_table_returns_columns_and_primary_keys():
    database_url = build_sqlite_database()
    table_info = inspect_table("customers", database_url)

    assert table_info["name"] == "customers"
    assert any(column["name"] == "id" and column["primary_key"] is True for column in table_info["columns"])
    assert table_info["primary_keys"] == ["id"]


def test_inspect_relationships_returns_foreign_keys():
    database_url = build_sqlite_database()
    relationships = inspect_relationships(database_url)

    assert any(
        rel["table"] == "orders" and rel["references"]["table"] == "customers"
        for rel in relationships
    )
