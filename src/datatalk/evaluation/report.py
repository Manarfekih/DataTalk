from __future__ import annotations

import json
import logging
from base64 import b64encode
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from datatalk.evaluation.metrics import EvaluationMetrics
from datatalk.evaluation.models import EvaluationResult


logger = logging.getLogger(__name__)

MAX_REPORT_ROWS = 5


class EvaluationReport:

    def __init__(self, results: list[EvaluationResult]) -> None:
        self.results = results

    def summary(self) -> dict:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_questions": len(self.results),
            "text_to_sql_accuracy": EvaluationMetrics.text_to_sql_accuracy(self.results),
            "execution_accuracy": EvaluationMetrics.execution_accuracy(self.results),
            "retry_success_rate": EvaluationMetrics.retry_success_rate(self.results),
            "first_pass_accuracy": EvaluationMetrics.first_pass_accuracy(self.results),
            "average_retry_count": EvaluationMetrics.average_retry_count(self.results),
        }

    def save_json(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "summary": self.summary(),
            "results": [self._serialize_result(result) for result in self.results],
        }

        with open(path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False)

        logger.info("Evaluation JSON saved: %s", path)

    def save_markdown(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        summary = self.summary()
        content = self._build_markdown(summary)

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        logger.info("Evaluation Markdown saved: %s", path)

    def _build_markdown(self, summary: dict) -> str:
        content = [
            "# DataTalk Evaluation Report",
            "",
            "## Generated",
            "",
            summary["generated_at"],
            "",
            "## General Metrics",
            "",
            "| Metric | Score |",
            "|---|---:|",
            f"| Total Questions | {summary['total_questions']} |",
            f"| Text-to-SQL Accuracy | {summary['text_to_sql_accuracy']:.2%} |",
            f"| Execution Accuracy | {summary['execution_accuracy']:.2%} |",
            f"| Retry Success Rate | {summary['retry_success_rate']:.2%} |",
            f"| First Pass Accuracy | {summary['first_pass_accuracy']:.2%} |",
            f"| Average Retry Count | {summary['average_retry_count']:.2f} |",
            "",
            "## Failed Cases",
            "",
        ]

        failed_cases = [
            result
            for result in self.results
            if result.error or not result.sql_correct or not result.execution_correct
        ]

        if not failed_cases:
            content.append("No failed cases - all benchmarks passed.")
            content.append("")
            return "\n".join(content)

        for result in failed_cases:
            content.extend(
                [
                    f"### Case {result.case_id}",
                    "",
                    f"**Question:** {result.question}",
                    "",
                    f"**Text-to-SQL Correct:** {result.sql_correct}",
                    "",
                    f"**Execution Correct:** {result.execution_correct}",
                    "",
                    f"**Execution Succeeded:** {result.execution_success}",
                    "",
                    "**Generated SQL:**",
                    "",
                    "```sql",
                    result.generated_sql or "",
                    "```",
                    "",
                    "**Expected SQL:**",
                    "",
                    "```sql",
                    result.expected_sql or "",
                    "```",
                    "",
                    "**Expected Rows:**",
                    "",
                    self._preview_label(result.expected_rows),
                    "",
                    "```json",
                    json.dumps(
                        self._row_preview(result.expected_rows),
                        indent=2,
                        ensure_ascii=False,
                    ),
                    "```",
                    "",
                    "**Generated Rows:**",
                    "",
                    self._preview_label(result.generated_rows),
                    "",
                    "```json",
                    json.dumps(
                        self._row_preview(result.generated_rows),
                        indent=2,
                        ensure_ascii=False,
                    ),
                    "```",
                    "",
                    f"**Error:** {result.error or 'None'}",
                    "",
                ]
            )

        return "\n".join(content)

    @staticmethod
    def _serialize_result(result: EvaluationResult) -> dict:
        if hasattr(result, "model_dump"):
            data = EvaluationReport._json_safe(result.model_dump(mode="json"))
        elif hasattr(result, "dict"):
            data = EvaluationReport._json_safe(result.dict())
        elif hasattr(result, "__dict__"):
            data = EvaluationReport._json_safe(result.__dict__)
        else:
            return {"value": str(result)}

        if isinstance(data, dict):
            generated_rows = result.generated_rows
            expected_rows = result.expected_rows
            data["generated_row_count"] = len(generated_rows)
            data["expected_row_count"] = len(expected_rows)
            data["generated_rows_truncated"] = len(generated_rows) > MAX_REPORT_ROWS
            data["expected_rows_truncated"] = len(expected_rows) > MAX_REPORT_ROWS
            data["generated_rows"] = EvaluationReport._row_preview(generated_rows)
            data["expected_rows"] = EvaluationReport._row_preview(expected_rows)

        return data

    @staticmethod
    def _row_preview(rows: list[dict]) -> list[dict]:
        return EvaluationReport._json_safe(rows[:MAX_REPORT_ROWS])

    @staticmethod
    def _preview_label(rows: list[dict]) -> str:
        row_count = len(rows)
        shown_count = min(row_count, MAX_REPORT_ROWS)

        if row_count > MAX_REPORT_ROWS:
            return f"Showing first {shown_count} of {row_count} rows."

        return f"Showing {shown_count} of {row_count} rows."

    @staticmethod
    def _json_safe(value: object) -> object:
        if isinstance(value, dict):
            return {str(key): EvaluationReport._json_safe(val) for key, val in value.items()}
        if isinstance(value, list):
            return [EvaluationReport._json_safe(item) for item in value]
        if isinstance(value, tuple):
            return [EvaluationReport._json_safe(item) for item in value]
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, UUID):
            return str(value)
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return b64encode(value).decode("ascii")
        return value
