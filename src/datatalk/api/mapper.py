from __future__ import annotations

from datatalk.models import QueryResult

from .models import (
    QueryResponse,
    RetryAttemptResponse,
)


def to_retry_attempt_response(
    retry,
) -> RetryAttemptResponse:
    """
    Convert internal RetryAttempt model
    into API response model.
    """

    return RetryAttemptResponse(
        attempt_number=retry.attempt_number,
        original_sql=retry.original_sql,
        error=retry.error,
        corrected_sql=retry.corrected_sql,
        reasoning=retry.reasoning,
        confidence=retry.confidence,
        detected_error=retry.detected_error,
        changes_made=retry.changes_made,
    )



def to_query_response(
    result: QueryResult,
) -> QueryResponse:
    """
    Convert workflow QueryResult
    into FastAPI QueryResponse.
    """

    return QueryResponse(

        question=result.question,

        tables=result.tables,

        reasoning=result.reasoning,

        sql_query=result.sql_query,

        explanation=result.explanation,


        rows=(
            result.execution.rows
            if result.execution
            else []
        ),


        columns=(
            result.execution.columns
            if result.execution
            else []
        ),


        row_count=(
            result.execution.row_count
            if result.execution
            else 0
        ),


        execution_time_ms=(
            result.execution.elapsed_ms
            if result.execution
            else 0.0
        ),


        total_time_ms=result.total_elapsed_ms,


        retry_count=result.retry_count,


        retry_history=[
            to_retry_attempt_response(item)
            for item in result.retry_history
        ],


    )