from __future__ import annotations

from typing import TypedDict, Any

from datatalk.models.execution import SQLExecutionResult
from datatalk.models.retry_history import RetryAttempt



class DataTalkState(TypedDict, total=False):

    question: str

    clean_question: str

    tables: list[str]

    reasoning: str

    sql_query: str


    execution: SQLExecutionResult


    rows: list[dict[str, Any]]

    columns: list[str]


    error_message: str


    retry_count: int

    retry_history: list[RetryAttempt]

    max_retries:int


    explanation:str

    total_elapsed_ms:float