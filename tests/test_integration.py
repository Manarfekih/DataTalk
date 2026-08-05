from __future__ import annotations

from datatalk.core import container


def test_full_pipeline() -> None:
    

    container.initialize()

    result = container.query_workflow.ask(
        "How many customers are there?"
    )


    assert result.question
    assert result.tables
    assert result.reasoning
    assert result.sql_query
    assert result.explanation


    assert result.execution.success
    assert result.execution.row_count >= 1


    assert result.execution.elapsed_ms >= 0
    assert result.total_elapsed_ms >= 0


    assert result.retry_count >= 0
    assert len(result.retry_history) == result.retry_count


    if result.retry_count == 0:
        assert result.retry_history == []