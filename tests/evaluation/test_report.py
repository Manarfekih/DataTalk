from datatalk.evaluation.models import EvaluationResult
from datatalk.evaluation.report import EvaluationReport


def test_markdown_report_serializes_bytes() -> None:
    report = EvaluationReport(
        [
            EvaluationResult(
                case_id="bytes_001",
                question="test",
                generated_rows=[{"payload": b"hello"}],
                expected_rows=[{"payload": b"hello"}],
                execution_success=True,
                execution_correct=False,
            )
        ]
    )

    markdown = report._build_markdown(report.summary())

    assert "hello" in markdown


def test_serialized_report_truncates_large_row_sets() -> None:
    result = EvaluationResult(
        case_id="large_001",
        question="test",
        generated_rows=[{"id": value} for value in range(10)],
        expected_rows=[{"id": value} for value in range(10)],
    )

    serialized = EvaluationReport._serialize_result(result)

    assert serialized["generated_row_count"] == 10
    assert serialized["expected_row_count"] == 10
    assert serialized["generated_rows_truncated"] is True
    assert serialized["expected_rows_truncated"] is True
    assert len(serialized["generated_rows"]) == 5
    assert len(serialized["expected_rows"]) == 5
