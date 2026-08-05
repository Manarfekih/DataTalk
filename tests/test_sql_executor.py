from datatalk.guardrails import SQLSafety
from datatalk.services import SQLExecutor
from datatalk.database.connection import db_manager


def test_execute_simple_query():

    executor = SQLExecutor(
        db=db_manager,
        safety=SQLSafety()
    )

    result = executor.execute(
        "SELECT 1"
    )

    assert result.success
    assert result.row_count == 1


def test_block_unsafe_query():

    executor = SQLExecutor(
        db=db_manager,
        safety=SQLSafety()
    )

    result = executor.execute(
        "DROP TABLE customers"
    )

    assert not result.success