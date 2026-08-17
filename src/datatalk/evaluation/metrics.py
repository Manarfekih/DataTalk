from __future__ import annotations

import logging
import re

from datatalk.evaluation.models import EvaluationResult


logger = logging.getLogger(__name__)


class SQLNormalizer:
    """Normalize SQL for text-to-SQL comparison."""

    @staticmethod
    def normalize(sql: str | None) -> str:
        if not sql:
            return ""

        normalized = sql.lower()
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = normalized.strip()
        normalized = normalized.rstrip(";")
        return normalized


class EvaluationMetrics:
    """Compute evaluation metrics for benchmark results."""

    @staticmethod
    def normalize_sql(sql: str | None) -> str:
        return SQLNormalizer.normalize(sql)

    @classmethod
    def text_to_sql_accuracy(cls, results: list[EvaluationResult]) -> float:
        if not results:
            return 0.0

        correct = 0
        for result in results:
            generated = cls.normalize_sql(result.generated_sql)
            expected = cls.normalize_sql(result.expected_sql)
            if generated == expected:
                correct += 1

        return correct / len(results)

    @staticmethod
    def execution_accuracy(results: list[EvaluationResult]) -> float:
        if not results:
            return 0.0

        correct = sum(1 for result in results if result.execution_correct)
        return correct / len(results)

    @staticmethod
    def retry_success_rate(results: list[EvaluationResult]) -> float:
        retry_cases = [result for result in results if result.retry_used]
        if not retry_cases:
            return 0.0

        successful = sum(1 for result in retry_cases if result.retry_success)
        return successful / len(retry_cases)

    @staticmethod
    def first_pass_accuracy(results: list[EvaluationResult]) -> float:
        if not results:
            return 0.0

        successful = sum(
            1
            for result in results
            if result.execution_correct and result.retry_count == 0
        )
        return successful / len(results)

    @staticmethod
    def average_retry_count(results: list[EvaluationResult]) -> float:
        if not results:
            return 0.0

        total = sum(result.retry_count for result in results)
        return total / len(results)
