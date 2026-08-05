from __future__ import annotations

import logging
import time
from typing import Any

from datatalk.agents import (
    ExplanationAgent,
    QuestionUnderstandingAgent,
    SchemaExplorerAgent,
    SQLRetryAgent,
    SQLWriterAgent,
)
from datatalk.memory import SQLMemoryService
from datatalk.models import (
    QueryResult,
    RetryAttempt,
    SQLExperience,
    SQLRetryOutput,
)
from datatalk.services import SQLExecutor, SchemaService


logger = logging.getLogger(__name__)


class QueryWorkflow:
    def __init__(
        self,
        question_agent: QuestionUnderstandingAgent,
        schema_explorer: SchemaExplorerAgent,
        sql_writer: SQLWriterAgent,
        sql_retry: SQLRetryAgent,
        executor: SQLExecutor,
        explanation_agent: ExplanationAgent,
        schema_service: SchemaService,
        max_sql_retries: int = 2,
        min_retry_confidence: float = 0.70,
        memory_service: SQLMemoryService | None = None,
    ) -> None:
        self._question_agent = question_agent
        self._schema_explorer = schema_explorer
        self._sql_writer = sql_writer
        self._sql_retry = sql_retry
        self._executor = executor
        self._explanation_agent = explanation_agent
        self._schema_service = schema_service
        self._max_sql_retries = max_sql_retries
        self._min_retry_confidence = min_retry_confidence
        self._memory_service = memory_service

    # =====================================================
    # Main Workflow
    # =====================================================

    def ask(self, question: str) -> QueryResult:
        start = time.perf_counter()

        logger.info("Processing question: %s", question)

        clean_question = self._understand_question(question)
        schema_result = self._explore_schema(clean_question)
        relevant_tables = schema_result.relevant_tables

        logger.info("Relevant tables: %s", relevant_tables)

        sql = self._generate_sql(
            question=clean_question,
            tables=relevant_tables,
        )
        schema_text = self._build_schema_context(relevant_tables)

        execution, final_sql, retry_history = self._execute_with_retry(
            question=clean_question,
            sql=sql,
            schema=schema_text,
        )

        explanation = self._build_explanation(
            question=clean_question,
            execution=execution,
        )

        elapsed_ms = (time.perf_counter() - start) * 1000

        return self._build_query_result(
            question=question,
            reasoning=schema_result.reasoning,
            tables=relevant_tables,
            sql_query=final_sql,
            explanation=explanation,
            execution=execution,
            elapsed_ms=elapsed_ms,
            retry_history=retry_history,
        )

    def _understand_question(self, question: str) -> str:
        question_result = self._question_agent.process(question)

        if question_result.needs_clarification:
            raise ValueError(question_result.clarification_question)

        return question_result.corrected_question

    def _explore_schema(self, question: str):
        return self._schema_explorer.explore(question)

    def _generate_sql(self, *, question: str, tables: list[str]) -> str:
        sql_result = self._sql_writer.write_sql(
            question=question,
            tables=tables,
        )
        return sql_result.sql_query

    def _build_explanation(self, *, question: str, execution: Any) -> str:
        if execution.success:
            explanation_result = self._explanation_agent.explain(
                question=question,
                columns=execution.columns,
                rows=execution.rows,
            )
            return explanation_result.explanation

        return "Unable to execute SQL query: " + (execution.error or "Unknown error")

    def _build_query_result(
        self,
        *,
        question: str,
        reasoning: str,
        tables: list[str],
        sql_query: str,
        explanation: str,
        execution: Any,
        elapsed_ms: float,
        retry_history: list[RetryAttempt],
    ) -> QueryResult:
        return QueryResult(
            question=question,
            tables=tables,
            reasoning=reasoning,
            sql_query=sql_query,
            explanation=explanation,
            execution=execution,
            total_elapsed_ms=elapsed_ms,
            retry_history=retry_history,
            retry_count=len(retry_history),
        )

    # =====================================================
    # Retry Engine
    # =====================================================

    def _execute_with_retry(
        self,
        *,
        question: str,
        sql: str,
        schema: str,
    ):
        execution = self._executor.execute(sql)
        history: list[RetryAttempt] = []
        attempt = 0

        while not execution.success and attempt < self._max_sql_retries:
            failed_sql = sql
            error = execution.error or ""

            logger.warning(
                "SQL failed (%d/%d): %s",
                attempt + 1,
                self._max_sql_retries,
                error,
            )

            if not self._sql_retry.should_retry(error):
                break

            memory = self._retrieve_retry_memory(
                question=question,
                sql=failed_sql,
                error=error,
            )

            retry = self._sql_retry.retry(
                question=question,
                sql=failed_sql,
                error=error,
                schema=schema,
                history=history,
                memory=memory,
            )

            if retry.confidence < self._min_retry_confidence:
                break

            history.append(
                self._build_retry_attempt(
                    attempt_number=attempt + 1,
                    failed_sql=failed_sql,
                    error=error,
                    retry=retry,
                )
            )

            sql = retry.corrected_sql
            execution = self._executor.execute(sql)

            if execution.success and self._memory_service:
                self._store_successful_experience(
                    question=question,
                    failed_sql=failed_sql,
                    corrected_sql=sql,
                    error=error,
                    retry=retry,
                )

            attempt += 1

        return execution, sql, history

    def _retrieve_retry_memory(
        self,
        *,
        question: str,
        sql: str,
        error: str,
    ) -> list[SQLExperience]:
        if not self._memory_service:
            return []

        return self._memory_service.retrieve(
            question=question,
            sql=sql,
            error=error,
            top_k=3,
        )

    def _build_retry_attempt(
        self,
        *,
        attempt_number: int,
        failed_sql: str,
        error: str,
        retry: SQLRetryOutput,
    ) -> RetryAttempt:
        return RetryAttempt(
            attempt_number=attempt_number,
            original_sql=failed_sql,
            error=error,
            corrected_sql=retry.corrected_sql,
            reasoning=retry.reasoning,
            confidence=retry.confidence,
            detected_error=retry.detected_error,
            changes_made=retry.changes_made,
        )

    def _store_successful_experience(
        self,
        *,
        question: str,
        failed_sql: str,
        corrected_sql: str,
        error: str,
        retry: SQLRetryOutput,
    ) -> None:
        self._memory_service.add(
            SQLExperience(
                question=question,
                original_sql=failed_sql,
                corrected_sql=corrected_sql,
                error=error,
                reasoning=retry.reasoning,
                confidence=retry.confidence,
                detected_error=retry.detected_error,
                changes_made=retry.changes_made,
            )
        )

    # =====================================================
    # Schema Context Builder
    # =====================================================

    def _build_schema_context(self, tables: list[str]) -> str:
        parts: list[str] = []

        for table in tables:
            schema = self._schema_service.get_table_schema(table)
            if schema is None:
                continue

            parts.append(str(schema))

        return "\n\n".join(parts)
