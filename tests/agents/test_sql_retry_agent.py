from __future__ import annotations

import re

from datatalk.agents.sql_retry_agent import SQLRetryAgent
from datatalk.models.execution import SQLExecutionResult
from datatalk.workflows.query_workflow import QueryWorkflow


class FakeLLM:
    def generate_structured(
        self,
        *,
        prompt: str,
        response_model,
        temperature: float = 0.0,
    ):
        return response_model(
            corrected_sql="SELECT COUNT(customer_name) FROM customers;",
            reasoning="Use the plural table name.",
            confidence=0.95,
            detected_error="wrong table name",
            changes_made=["Changed customer to customers"],
        )


class FakeExecutor:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def execute(self, sql: str) -> SQLExecutionResult:
        self.calls.append(sql)

        if re.search(r"\bFROM\s+customer\b", sql, flags=re.IGNORECASE):
            return SQLExecutionResult(
                success=False,
                error='relation "customer" does not exist',
            )

        return SQLExecutionResult(
            success=True,
            rows=[],
            columns=[],
            row_count=0,
            error=None,
        )


class DummySchemaService:
    def get_table_schema(self, table: str):
        return None


class DummyAgent:
    pass


def test_sql_retry_agent():
    workflow = QueryWorkflow(
        question_agent=DummyAgent(),
        schema_explorer=DummyAgent(),
        sql_writer=DummyAgent(),
        sql_retry=SQLRetryAgent(llm=FakeLLM()),
        executor=FakeExecutor(),
        explanation_agent=DummyAgent(),
        schema_service=DummySchemaService(),
        memory_service=None,
    )

    execution, final_sql, history = workflow._execute_with_retry(
        question="How many customers are there?",
        sql="""
        SELECT COUNT(customer_name)
        FROM customer;
        """,
        schema="""
        customers(
            customer_id,
            company_name,
            contact_name
        )
        """,
    )

    assert execution.success
    assert final_sql.strip().upper().startswith("SELECT")
    assert len(history) > 0
