from __future__ import annotations

import json
import logging
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from datatalk.evaluation.metrics import EvaluationMetrics
from datatalk.evaluation.models import EvaluationResult


logger = logging.getLogger(__name__)


class EvaluationReport:
    """Generate JSON and markdown reports from evaluation results."""

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
            if result.error or not result.execution_correct
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
                    "```json",
                    json.dumps(self._json_safe(result.expected_rows), indent=2, ensure_ascii=False),
                    "```",
                    "",
                    "**Generated Rows:**",
                    "",
                    json.dumps(self._json_safe(result.generated_rows), indent=2, ensure_ascii=False),
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
            return EvaluationReport._json_safe(result.model_dump(mode="json"))
        if hasattr(result, "dict"):
            return EvaluationReport._json_safe(result.dict())
        if hasattr(result, "__dict__"):
            return EvaluationReport._json_safe(result.__dict__)
        return {"value": str(result)}

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
        return value

