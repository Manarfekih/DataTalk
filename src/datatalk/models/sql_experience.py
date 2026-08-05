from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field



class SQLExperience(BaseModel):


    id: str = Field(
        default_factory=lambda: str(uuid4())
    )


    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )


    question: str

    original_sql: str

    corrected_sql: str

    error: str

    reasoning: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    detected_error: str

    changes_made: list[str] = Field(
        default_factory=list
    )

    execution_success: bool = True