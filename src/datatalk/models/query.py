from dataclasses import dataclass, field

from datatalk.models.retry_history import RetryAttempt
from .execution import SQLExecutionResult





@dataclass(slots=True)
class QueryResult:


    question:str

    tables:list[str]

    reasoning:str

    sql_query:str

    explanation:str

    execution:SQLExecutionResult

    total_elapsed_ms:float


    retry_count:int = 0

    retry_history:list[RetryAttempt] = field(
        default_factory=list
    )