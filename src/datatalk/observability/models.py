from __future__ import annotations


from datetime import datetime

from pydantic import BaseModel, Field



class TraceEvent(BaseModel):
    


    trace_id: str


    node_name: str


    start_time: datetime


    end_time: datetime


    duration_ms: float



    input_data: dict = Field(
        default_factory=dict
    )


    output_data: dict = Field(
        default_factory=dict
    )


    success: bool = True


    error: str | None = None