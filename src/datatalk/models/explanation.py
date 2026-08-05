from __future__ import annotations

from pydantic import BaseModel, Field


class ExplanationOutput(BaseModel):
    

    explanation: str = Field(
        description="Simple explanation of the SQL result."
    )