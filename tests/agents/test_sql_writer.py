from __future__ import annotations

import pytest

from datatalk.agents.sql_writer import SQLWriterAgent
from datatalk.models.agent_outputs import SQLWriterOutput
from datatalk.services import schema_service


class FakeLLM:
    

    def __init__(
        self,
        sql: str,
        explanation: str = "Generated SQL",
    ) -> None:

        self._sql = sql
        self._explanation = explanation

    def generate_structured(
        self,
        *,
        prompt: str,
        response_model,
        temperature: float = 0.1,
    ):

        return response_model(
            sql_query=self._sql,
            explanation=self._explanation,
        )


@pytest.fixture
def sql_writer() -> SQLWriterAgent:

    llm = FakeLLM(
        sql="""
        SELECT *
        FROM customers
        """
    )

    return SQLWriterAgent(
        llm=llm,
        schema_service=schema_service,
    )


def test_write_sql_success(
    sql_writer: SQLWriterAgent,
):

    result = sql_writer.write_sql(
        question="Show all customers",
        tables=["customers"],
    )

    assert isinstance(result, SQLWriterOutput)

    assert result.sql_query.strip().upper().startswith(
        "SELECT"
    )

    assert result.sql_query.strip() != ""


def test_build_schema_context(
    sql_writer: SQLWriterAgent,
):

    context = sql_writer._build_schema_context(
        ["customers"]
    )

    assert "Table: customers" in context

    schema = schema_service.get_table_schema(
        "customers"
    )

    for column in schema.columns:

        assert column.name in context


def test_invalid_table():

    llm = FakeLLM(
        sql="SELECT * FROM fake_table"
    )

    writer = SQLWriterAgent(
        llm=llm,
        schema_service=schema_service,
    )

    with pytest.raises(ValueError):

        writer.write_sql(
            question="Test",
            tables=["fake_table"],
        )


def test_empty_table_list(
    sql_writer: SQLWriterAgent,
):

    with pytest.raises(ValueError):

        sql_writer.write_sql(
            question="Show customers",
            tables=[],
        )


def test_unsafe_sql():

    llm = FakeLLM(
        sql="""
        DROP TABLE customers
        """
    )

    writer = SQLWriterAgent(
        llm=llm,
        schema_service=schema_service,
    )

    with pytest.raises(ValueError):

        writer.write_sql(
            question="Delete customers",
            tables=["customers"],
        )


