from __future__ import annotations

import logging

from datatalk.graph.state import DataTalkState


logger = logging.getLogger(__name__)


class GraphNodes:


    def __init__(
        self,
        question_agent,
        schema_explorer,
        sql_writer,
        sql_executor,
        sql_retry,
        explanation_agent,
        memory_service=None,
    ):


        self.question_agent = question_agent

        self.schema_explorer = schema_explorer

        self.sql_writer = sql_writer

        self.sql_executor = sql_executor

        self.sql_retry = sql_retry

        self.explanation_agent = explanation_agent

        self.memory_service = memory_service



    # Question Understanding

    def understand_question(
        self,
        state: DataTalkState,
    ):


        result = self.question_agent.process(
            state["question"]
        )


        if result.needs_clarification:

            raise ValueError(
                result.clarification_question
            )


        return {

            "clean_question":
                result.corrected_question

        }



    # Schema Exploration

    def explore_schema(
        self,
        state: DataTalkState,
    ):


        result = self.schema_explorer.explore(
            state["clean_question"]
        )


        return {

            "tables":
                result.relevant_tables,


            "reasoning":
                result.reasoning,

        }



    # SQL Generation

    def generate_sql(
        self,
        state: DataTalkState,
    ):


        result = self.sql_writer.write_sql(

            question=state["clean_question"],

            tables=state["tables"]

        )


        return {

            "sql_query":
                result.sql_query

        }



    # SQL Execution

    def execute_sql(
        self,
        state: DataTalkState,
    ):


        execution = self.sql_executor.execute(

            state["sql_query"]

        )


        return {


            "execution":
                execution,


            "rows":
                execution.rows,


            "columns":
                execution.columns,


        }



    # SQL Retry

    def retry_sql(
        self,
        state: DataTalkState,
    ):


        execution = state["execution"]


        retry_count = state.get(
            "retry_count",
            0
        )


        retry = self.sql_retry.retry(

            question=state["clean_question"],

            sql=state["sql_query"],

            error=execution.error or "",

            schema="",

            history=state.get(
                "retry_history",
                []
            ),

            memory=[],

        )


        return {

            "sql_query":
                retry.corrected_sql,


            "retry_count":
                retry_count + 1,

        }



    # Explanation

    def explain(
        self,
        state: DataTalkState,
    ):


        result = self.explanation_agent.explain(

            question=state["clean_question"],

            columns=state["columns"],

            rows=state["rows"]

        )


        return {

            "explanation":
                result.explanation

        }