from __future__ import annotations

import logging
from typing import Any

from datatalk.evaluation.models import EvaluationCase


logger = logging.getLogger(__name__)


class DataTalkEvaluator:

    def __init__(self, numeric_tolerance: float = 1e-6) -> None:
        self.numeric_tolerance = numeric_tolerance

    def compare_rows(
        self,
        generated_rows: list[dict[str, Any]],
        expected_rows: list[dict[str, Any]],
    ) -> bool:
        if len(generated_rows) != len(expected_rows):
            return False

        generated_normalized = self._normalize_rows(generated_rows)
        expected_normalized = self._normalize_rows(expected_rows)
        return generated_normalized == expected_normalized

    def compare_sql(self, generated_sql: str | None, expected_sql: str | None) -> bool:
        return self.normalize_sql(generated_sql) == self.normalize_sql(expected_sql)

    def compare_sql_result(self, generated_sql: str | None, expected_sql: str | None) -> bool:
        return self.compare_sql(generated_sql, expected_sql)

    def _normalize_rows(self, rows: list[dict[str, Any]]) -> list[tuple]:
        normalized: list[tuple] = []

        for row in rows:
            normalized_row = tuple(
                sorted(
                    (key, self._normalize_value(value))
                    for key, value in row.items()
                )
            )
            normalized.append(normalized_row)

        normalized.sort()
        return normalized

    def _normalize_value(self, value: Any):
        if isinstance(value, float):
            return round(value, 6)
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return value.strip().lower()
        if value is None:
            return None
        return value

    @staticmethod
    def normalize_sql(sql: str | None) -> str:
        if not sql:
            return ""

        sql = sql.lower()
        sql = " ".join(sql.split())
        return sql.strip().rstrip(";")
