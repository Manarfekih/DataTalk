from __future__ import annotations

import logging
import time

from datatalk.evaluation.evaluator import DataTalkEvaluator
from datatalk.evaluation.models import EvaluationCase, EvaluationResult
from datatalk.graph.workflow import DataTalkGraph
from datatalk.services.sql_executor import SQLExecutor


logger = logging.getLogger(__name__)


class EvaluationRunner:

    def __init__(self, graph: DataTalkGraph, sql_executor: SQLExecutor | None = None) -> None:
        self.graph = graph
        self.evaluator = DataTalkEvaluator()
        self.sql_executor = sql_executor

    def run_case(self, case: EvaluationCase) -> EvaluationResult:
        logger.info("Running evaluation case %s", case.id)
        start = time.perf_counter()

        try:
            result = self.graph.invoke(
                {
                    "question": case.question,
                    "max_retries": 2,
                    "retry_count": 0,
                }
            )

            elapsed = (time.perf_counter() - start) * 1000
            execution = result.get("execution")
            generated_sql = result.get("sql_query")
            rows = result.get("rows", [])
            retry_count = result.get("retry_count", 0)

            execution_success = bool(execution.success) if execution else False
            retry_used = retry_count > 0
            retry_success = retry_used and execution_success
            sql_correct = self.evaluator.compare_sql(generated_sql, case.expected_sql)

            expected_rows, has_expected_rows = self._resolve_expected_rows(case)
            execution_correct = (
                execution_success
                and has_expected_rows
                and self.evaluator.compare_rows(rows, expected_rows)
            )

            return EvaluationResult(
                case_id=case.id,
                category=case.category,
                question=case.question,
                generated_sql=generated_sql,
                expected_sql=case.expected_sql,
                sql_correct=sql_correct,
                generated_rows=rows,
                expected_rows=expected_rows,
                execution_success=execution_success,
                execution_correct=execution_correct,
                retry_used=retry_used,
                retry_success=retry_success,
                retry_count=retry_count,
                execution_time_ms=elapsed,
            )
        except Exception as exc:
            logger.exception("Evaluation failed for %s", case.id)
            return EvaluationResult(
                case_id=case.id,
                category=case.category,
                question=case.question,
                expected_sql=case.expected_sql,
                sql_correct=False,
                execution_success=False,
                execution_correct=False,
                retry_used=False,
                retry_success=False,
                error=str(exc),
            )

    def run(self, cases: list[EvaluationCase]) -> list[EvaluationResult]:
        return [self.run_case(case) for case in cases]

    def _resolve_expected_rows(self, case: EvaluationCase) -> tuple[list[dict], bool]:
        if case.expected_rows:
            return case.expected_rows, True

        if self.sql_executor is None:
            logger.warning(
                "No SQL executor configured; cannot derive expected rows for %s.",
                case.id,
            )
            return [], False

        expected_execution = self.sql_executor.execute(case.expected_sql)
        if not expected_execution.success:
            logger.warning(
                "Expected SQL failed for %s: %s",
                case.id,
                expected_execution.error,
            )
            return [], False

        return expected_execution.rows, True
