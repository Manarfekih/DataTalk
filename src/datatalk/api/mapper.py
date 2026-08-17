from __future__ import annotations


from datatalk.graph.state import DataTalkState

from .models import (
    QueryResponse,
    RetryAttemptResponse,
)





def to_query_response(
    state: DataTalkState,
) -> QueryResponse:


    execution = state.get(
        "execution"
    )



    return QueryResponse(

        question=
            state.get(
                "question",
                ""
            ),


        tables=
            state.get(
                "tables",
                []
            ),


        reasoning=
            state.get(
                "reasoning",
                ""
            ),


        sql_query=
            state.get(
                "sql_query",
                ""
            ),


        explanation=
            state.get(
                "explanation",
                ""
            ),



        rows=(
            execution.rows
            if execution
            else []
        ),



        columns=(
            execution.columns
            if execution
            else []
        ),



        row_count=(
            len(execution.rows)
            if execution
            else 0
        ),



        execution_time_ms=(
            execution.elapsed_ms
            if execution
            else 0.0
        ),



        total_time_ms=
            state.get(
                "total_elapsed_ms",
                0.0
            ),



        retry_count=
            state.get(
                "retry_count",
                0
            ),



        retry_history=[
            RetryAttemptResponse(
                attempt_number=a.attempt_number,
                original_sql=a.original_sql,
                error=a.error,
                corrected_sql=a.corrected_sql,
                reasoning=a.reasoning,
                confidence=a.confidence,
                detected_error=a.detected_error,
                changes_made=a.changes_made,
            )
            for a in state.get("retry_history", [])
        ],
    )