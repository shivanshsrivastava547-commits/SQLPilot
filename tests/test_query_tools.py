from database.executor import execute_query
from tools.query_tools import generate_query, validate_sql


def test_generate_query_uses_schema_context_for_common_business_question():
    schema = {
        "tables": [
            {
                "name": "orders",
                "columns": [
                    {"name": "id", "type": "INTEGER"},
                    {"name": "product", "type": "TEXT"},
                    {"name": "revenue", "type": "REAL"},
                ],
            }
        ]
    }

    query = generate_query("top 10 products by revenue", schema)

    assert query.strip().lower().startswith("select")
    assert "revenue" in query.lower()
    assert "order by" in query.lower()
    assert "limit" in query.lower()


def test_validate_sql_allows_safe_select_queries():
    query = "SELECT id, name FROM customers WHERE active = 1 LIMIT 10"
    assert validate_sql(query) == query


def test_validate_sql_rejects_destructive_statements():
    for unsafe in [
        "DELETE FROM customers",
        "UPDATE customers SET active = 0",
        "DROP TABLE customers",
        "INSERT INTO customers VALUES (1, 'A')",
    ]:
        try:
            validate_sql(unsafe)
            raise AssertionError(f"Expected unsafe SQL to be rejected: {unsafe}")
        except ValueError:
            pass


def test_execute_query_returns_structured_result_for_safe_sql():
    result = execute_query("SELECT 1 AS value", database_url="sqlite:///:memory:")

    assert result["status"] == "success"
    assert result["row_count"] == 1
    assert result["rows"][0]["value"] == 1
