from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    

    content: str
    provider: str
    model: str

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

    latency_ms: float | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )