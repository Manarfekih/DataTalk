from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field



class ExecutionLog(BaseModel):
    


    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


    sql: str


    success: bool


    rows_returned: int = 0


    execution_time_ms: float = 0.0


    error: str | None = None