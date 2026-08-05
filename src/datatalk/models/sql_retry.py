from __future__ import annotations

from pydantic import BaseModel, Field


class SQLRetryOutput(BaseModel):
    should_retry: bool = Field(
        default=True,
        description="Whether the SQL query should be retried.",
    )

    corrected_sql: str = Field(
        description="Corrected SQL query.",
    )

    reasoning: str = Field(
        description="Explanation of the detected problem and fix.",
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    detected_error: str = Field(
        description="Detected SQL error category.",
    )

    changes_made: list[str] = Field(
        default_factory=list,
        description="Changes applied to the SQL query.",
    )
