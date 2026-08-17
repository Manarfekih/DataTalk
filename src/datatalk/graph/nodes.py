from __future__ import annotations


import logging
import time


from datatalk.graph.state import DataTalkState


from datatalk.observability import tracer



logger = logging.getLogger(__name__)



container = None



def set_container(app_container):

    global container

    container = app_container





# Question Understanding


def _understand_question_impl(
    question_agent,
    state: DataTalkState,
):

    with tracer.span(
        "question_understanding",
        {
            "question": state["question"]
        },
    ):

        result = question_agent.process(
            state["question"]
        )


        if result.needs_clarification:

            raise ValueError(
                result.clarification_question
            )


        return {

            "clean_question":
                result.corrected_question,


            "start_time":
                time.perf_counter(),

        }





# Schema Exploration


def _explore_schema_impl(
    schema_explorer,
    state: DataTalkState,
):

    with tracer.span(
        "schema_exploration",
        {
            "question":
                state["clean_question"]
        },
    ):


        result = schema_explorer.explore(
            state["clean_question"]
        )


        return {

            "tables":
                result.relevant_tables,


            "reasoning":
                result.reasoning,

        }





# SQL Generation


def _generate_sql_impl(
    sql_writer,
    state: DataTalkState,
):

    with tracer.span(
        "sql_generation",
        {
            "tables":
                state["tables"]
        },
    ):


        result = sql_writer.write_sql(

            question=
                state["clean_question"],


            tables=
                state["tables"],

        )


        return {

            "sql_query":
                result.sql_query,

        }





# SQL Execution


def _execute_sql_impl(
    sql_executor,
    state: DataTalkState,
):


    with tracer.span(

        "sql_execution",

        {
            "sql":
                state["sql_query"]
        },

    ):


        execution = sql_executor.execute(

            state["sql_query"]

        )


        return {


            "execution":
                execution,


            "rows":
                execution.rows,


            "columns":
                execution.columns,


            "error_message":
                execution.error or "",

        }





# SQL Retry


def _retry_sql_impl(
    sql_retry,
    sql_memory,
    state: DataTalkState,
):


    with tracer.span(

        "sql_retry",

        {
            "sql":
                state["sql_query"],


            "error":
                state.get(
                    "error_message",
                    ""
                ),

        },

    ):


        execution = state["execution"]


        retry_count = state.get(
            "retry_count",
            0,
        )


        failed_sql = state["sql_query"]


        error = execution.error or ""



        logger.info(
            "Searching SQL memory..."
        )


        memory = []


        if sql_memory:


            memory = sql_memory.retrieve(

                question=
                    state["clean_question"],


                sql=
                    failed_sql,


                error=
                    error,


                top_k=3,

            )



        logger.info(

            "Retrieved %d memories",

            len(memory),

        )




        retry = sql_retry.retry(

            question=
                state["clean_question"],


            sql=
                failed_sql,


            error=
                error,


            schema="",


            history=
                state.get(
                    "retry_history",
                    []
                ),


            memory=
                memory,

        )



        return {


            "sql_query":
                retry.corrected_sql,


            "retry_count":
                retry_count + 1,

        }





# Explanation


def _explain_impl(
    explanation_agent,
    state: DataTalkState,
):


    with tracer.span(

        "explanation",

        {
            "rows":
                len(state["rows"])
        },

    ):


        result = explanation_agent.explain(

            question=
                state["clean_question"],


            columns=
                state["columns"],


            rows=
                state["rows"],

        )


        elapsed = (

            time.perf_counter()

            -

            state["start_time"]

        ) * 1000



        return {


            "explanation":
                result.explanation,


            "total_elapsed_ms":
                elapsed,

        }





class GraphNodes:
    """
    Wraps all agent/service dependencies into a single object whose methods
    are registered as LangGraph nodes by DataTalkGraph.

    This is the class-based alternative to using the module-level free
    functions (``understand_question``, ``explore_schema``, etc.) which
    rely on the global ``container``.  ``Container._create_graph`` uses
    this class so that the graph is fully dependency-injected.
    """

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
        self._question_agent = question_agent
        self._schema_explorer = schema_explorer
        self._sql_writer = sql_writer
        self._sql_executor = sql_executor
        self._sql_retry = sql_retry
        self._explanation_agent = explanation_agent
        self._memory_service = memory_service

    # ── Node callables ────────────────────────────────────────────────────

    def understand_question(self, state: DataTalkState):
        return _understand_question_impl(self._question_agent, state)

    def explore_schema(self, state: DataTalkState):
        return _explore_schema_impl(self._schema_explorer, state)

    def generate_sql(self, state: DataTalkState):
        return _generate_sql_impl(self._sql_writer, state)

    def execute_sql(self, state: DataTalkState):
        return _execute_sql_impl(self._sql_executor, state)

    def retry_sql(self, state: DataTalkState):
        return _retry_sql_impl(self._sql_retry, self._memory_service, state)

    def explain(self, state: DataTalkState):
        return _explain_impl(self._explanation_agent, state)


# ── Module-level node functions (use global container) ────────────────────────
# These are kept for backward compatibility with any code that still wires
# nodes directly from module imports.


def understand_question(
    state: DataTalkState,
):

    return _understand_question_impl(

        container.question_agent,

        state,

    )




def explore_schema(
    state: DataTalkState,
):

    return _explore_schema_impl(

        container.schema_explorer,

        state,

    )





def generate_sql(
    state: DataTalkState,
):

    return _generate_sql_impl(

        container.sql_writer,

        state,

    )





def execute_sql(
    state: DataTalkState,
):

    return _execute_sql_impl(

        container.sql_executor,

        state,

    )





def retry_sql(
    state: DataTalkState,
):

    return _retry_sql_impl(

        container.sql_retry,

        container.sql_memory,

        state,

    )





def explain(
    state: DataTalkState,
):

    return _explain_impl(

        container.explanation_agent,

        state,

    )