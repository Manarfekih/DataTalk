from __future__ import annotations

import logging
from typing import Any

from datatalk.guardrails import SQLSafety
from datatalk.llm.base import BaseLLMProvider
from datatalk.models import RetryAttempt, SQLExperience, SQLRetryOutput
from datatalk.prompts.sql_retry import SQL_RETRY_PROMPT


logger = logging.getLogger(__name__)


class SQLRetryAgent:
    """
    Repairs SQL queries that fail during execution.

    Responsibilities:
        - Analyze SQL execution errors
        - Generate corrected SQL
        - Use previous retry attempts
        - Use ChromaDB memory examples
        - Validate generated SQL safety

    Input:
        - Question
        - Failed SQL
        - Database error
        - Schema context
        - Retry history
        - Similar successful corrections

    Output:
        - Corrected SQL
        - Reasoning
        - Confidence
    """

    NON_RETRYABLE_ERRORS = (
        "permission denied",
        "authentication",
        "connection refused",
        "connection reset",
        "timeout",
        "ssl",
    )

    def __init__(self, llm: BaseLLMProvider) -> None:
        self._llm = llm
        self._sql_safety = SQLSafety()

    
    # Retry Decision

    def should_retry(self, error: str) -> bool:
        error = error.lower()
        return not any(keyword in error for keyword in self.NON_RETRYABLE_ERRORS)

    # Generate SQL Correction

    def retry(
        self,
        *,
        question: str,
        sql: str,
        error: str,
        schema: str,
        history: list[RetryAttempt],
        memory: list[SQLExperience],
    ) -> SQLRetryOutput:
        logger.info("Generating SQL correction...")

        prompt = self._build_prompt(
            question=question,
            sql=sql,
            error=error,
            schema=schema,
            history=history,
            memory=memory,
        )

        result = self._generate_retry_output(prompt)
        corrected_sql = self._sql_safety.validate_or_raise(result.corrected_sql)
        result = result.model_copy(update={"corrected_sql": corrected_sql})

        logger.info(
            "SQL correction generated with confidence %.2f",
            result.confidence,
        )

        return result

    def _build_prompt(
        self,
        *,
        question: str,
        sql: str,
        error: str,
        schema: str,
        history: list[RetryAttempt],
        memory: list[SQLExperience],
    ) -> str:
        return SQL_RETRY_PROMPT.format(
            question=question,
            sql=sql,
            error=error,
            schema=schema,
            history=self._format_history(history),
            memory=self._format_memory(memory),
        )

    def _generate_retry_output(self, prompt: str) -> SQLRetryOutput:
        return self._llm.generate_structured(
            prompt=prompt,
            response_model=SQLRetryOutput,
            temperature=0.0,
        )

    
    @staticmethod
    def _format_history(history: list[RetryAttempt]) -> str:
        if not history:
            return "No previous retry attempts."

        blocks: list[str] = []
        for item in history:
            blocks.append(SQLRetryAgent._format_history_item(item))

        return "\n\n".join(blocks)

    @staticmethod
    def _format_history_item(item: RetryAttempt) -> str:
        changes = ", ".join(item.changes_made) if item.changes_made else "None"

        return f"""
Attempt #{item.attempt_number}

Failed SQL:
{item.original_sql}

Database Error:
{item.error}

Corrected SQL:
{item.corrected_sql}

Reasoning:
{item.reasoning}

Confidence:
{item.confidence:.2f}

Detected Error:
{item.detected_error}

Changes:
{changes}
""".strip()

  
    @staticmethod
    def _format_memory(memory: list[SQLExperience]) -> str:
        if not memory:
            return "No similar SQL correction examples found."

        blocks: list[str] = []
        for index, item in enumerate(memory, start=1):
            blocks.append(
                SQLRetryAgent._format_memory_item(
                    index=index,
                    item=item,
                )
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _format_memory_item(*, index: int, item: SQLExperience) -> str:
        changes = SQLRetryAgent._format_changes(item.changes_made)

        return f"""
Example #{index}

Original Question:
{item.question}

Failed SQL:
{item.original_sql}

Database Error:
{item.error}

Corrected SQL:
{item.corrected_sql}

Reasoning:
{item.reasoning}

Detected Error:
{item.detected_error}

Changes:
{changes}

Confidence:
{item.confidence:.2f}
""".strip()

    @staticmethod
    def _format_changes(changes_made: Any) -> str:
        if isinstance(changes_made, list):
            return ", ".join(changes_made) if changes_made else "None"

        return str(changes_made)
