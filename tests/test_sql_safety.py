from datatalk.guardrails import SQLSafety


def test_valid_select():
    safety = SQLSafety()

    result = safety.validate(
        "SELECT * FROM customers"
    )

    assert result.is_valid


def test_valid_with():
    safety = SQLSafety()

    result = safety.validate(
        """
        WITH temp AS (
            SELECT * FROM customers
        )
        SELECT * FROM temp
        """
    )

    assert result.is_valid


def test_block_delete():
    safety = SQLSafety()

    result = safety.validate(
        "DELETE FROM customers"
    )

    assert not result.is_valid


def test_block_drop():
    safety = SQLSafety()

    result = safety.validate(
        "DROP TABLE customers"
    )

    assert not result.is_valid


def test_block_multiple_statements():
    safety = SQLSafety()

    result = safety.validate(
        "SELECT * FROM customers; DELETE FROM customers"
    )

    assert not result.is_valid


def test_remove_comments():
    safety = SQLSafety()

    sql = """
    -- comment
    SELECT * FROM customers
    """

    cleaned = safety.sanitize(sql)

    assert "--" not in cleaned
    assert cleaned.startswith("SELECT")


def test_empty_query():
    safety = SQLSafety()

    result = safety.validate("")

    assert not result.is_valid