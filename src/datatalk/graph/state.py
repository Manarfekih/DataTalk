from __future__ import annotations


from typing import TypedDict, Any


from datatalk.models.execution import SQLExecutionResult

from datatalk.models.retry_history import RetryAttempt





class DataTalkState(TypedDict, total=False):



    question: str



    # Question understanding

    clean_question: str



    # Schema

    tables: list[str]

    reasoning: str



    # SQL

    sql_query: str



    # Execution

    execution: SQLExecutionResult


    rows: list[dict[str, Any]]


    columns: list[str]


    error_message: str



    # Retry system

    retry_count: int


    retry_history: list[RetryAttempt]


    max_retries: int




    start_time: float


    total_elapsed_ms: float



    # Final answer

    explanation: str