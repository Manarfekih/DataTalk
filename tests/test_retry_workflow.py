from __future__ import annotations

import pytest

from datatalk.workflows.query_workflow import QueryWorkflow
from datatalk.models import (
    SQLRetryOutput,
    SQLWriterOutput,
)
from datatalk.models.execution import SQLExecutionResult



class FakeQuestionAgent:


    def process(self, question):

        class Result:

            corrected_question = question

            needs_clarification = False


        return Result()



class FakeSchemaExplorer:


    def explore(self, question):

        class Result:

            relevant_tables=[
                "customers"
            ]

            schema_context=[
                "customers(customer_id)"
            ]

            reasoning="customer table"


        return Result()



class FakeSQLWriter:


    def __init__(self):

        self.calls = 0


    def write_sql(
        self,
        question,
        tables,
    ):

        self.calls += 1


        return SQLWriterOutput(

            sql_query=
            "SELECT wrong_column FROM customers",

            explanation=
            "bad sql"
        )



class FakeRetryAgent:


    def should_retry(self,error):

        return True



    def retry(
        self,
        **kwargs
    ):


        return SQLRetryOutput(

            corrected_sql=
            "SELECT customer_id FROM customers",

            reasoning=
            "fixed column",

            confidence=
            0.95,

            detected_error=
            "wrong column",

            changes_made=[
                "replace column"
            ]

        )



class FakeExecutor:


    def __init__(self):

        self.calls=0


    def execute(self,sql):

        self.calls +=1


        if self.calls == 1:

            return SQLExecutionResult(

                success=False,

                error=
                "column wrong_column does not exist"

            )


        return SQLExecutionResult(

            success=True,

            rows=[
                {
                    "customer_id":1
                }
            ],

            row_count=1

        )



def test_workflow_retry():

    workflow = QueryWorkflow(

        question_agent=
        FakeQuestionAgent(),

        schema_explorer=
        FakeSchemaExplorer(),

        sql_writer=
        FakeSQLWriter(),

        sql_retry=
        FakeRetryAgent(),

        executor=
        FakeExecutor(),

    )


    result = workflow.ask(
        "show customers"
    )


    assert (
        result.execution.success
    )


    assert (
        "customer_id"
        in result.sql_query
    )