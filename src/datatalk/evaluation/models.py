from __future__ import annotations


from pydantic import BaseModel, Field



class EvaluationCase(BaseModel):
    """
    Single benchmark question.
    """


    id: str = Field(
        description="Unique benchmark identifier"
    )


    question: str = Field(
        description="Natural language question"
    )


    expected_sql: str = Field(
        description="Reference SQL query"
    )


    expected_rows: list[dict] = Field(
        default_factory=list,
        description="Expected database output"
    )


    category: str = Field(
        default="general",
        description="Benchmark category"
    )





class EvaluationResult(BaseModel):
    """
    Result of executing one benchmark case.
    """


    case_id: str


    category: str = "general"


    question: str



    # SQL generation

    generated_sql: str | None = None


    expected_sql: str | None = None


    sql_correct: bool = False



    # Execution

    generated_rows: list[dict] = Field(
        default_factory=list
    )


    expected_rows: list[dict] = Field(
        default_factory=list
    )


    execution_success: bool = False


    execution_correct: bool = False



    # Retry

    retry_used: bool = False


    retry_success: bool = False


    retry_count: int = 0



    # Performance

    execution_time_ms: float = 0.0



    error: str | None = None