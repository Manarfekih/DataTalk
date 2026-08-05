from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetryAttempt:


    attempt_number: int


    original_sql: str


    error: str


    corrected_sql: str


    reasoning: str


    confidence: float


    detected_error: str


    changes_made: list[str] = field(
        default_factory=list
    )