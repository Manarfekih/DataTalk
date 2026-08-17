from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path
from statistics import mean

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from datatalk.observability import tracer, execution_logger


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/observability", tags=["observability"])

EVAL_REPORT = Path("reports/evaluation.json")




class TraceEventResponse(BaseModel):
    trace_id: str
    node_name: str
    start_time: str
    end_time: str
    duration_ms: float
    success: bool
    error: str | None = None


class ExecutionLogResponse(BaseModel):
    timestamp: str
    sql: str
    success: bool
    rows_returned: int
    execution_time_ms: float
    error: str | None = None


class NodeStats(BaseModel):
    node_name: str
    call_count: int
    avg_duration_ms: float
    error_count: int
    error_rate: float


class RetryStats(BaseModel):
    total_executions: int
    total_errors: int
    error_rate: float
    avg_execution_time_ms: float
    common_errors: list[dict]


class ObsStatsResponse(BaseModel):
    node_stats: list[NodeStats]
    retry_stats: RetryStats


class EvalSummaryResponse(BaseModel):
    generated_at: str | None = None
    total_questions: int = 0
    text_to_sql_accuracy: float = 0.0
    execution_accuracy: float = 0.0
    retry_success_rate: float = 0.0
    first_pass_accuracy: float = 0.0
    average_retry_count: float = 0.0




@router.get(
    "/traces",
    response_model=list[TraceEventResponse],
    summary="Return all agent trace spans",
)
def get_traces() -> list[TraceEventResponse]:
    traces = tracer.storage.load_all()
    return [
        TraceEventResponse(
            trace_id=t.trace_id,
            node_name=t.node_name,
            start_time=t.start_time.isoformat(),
            end_time=t.end_time.isoformat(),
            duration_ms=t.duration_ms,
            success=t.success,
            error=t.error,
        )
        for t in reversed(traces)   
    ]


@router.get(
    "/executions",
    response_model=list[ExecutionLogResponse],
    summary="Return SQL execution history",
)
def get_executions() -> list[ExecutionLogResponse]:
    logs = execution_logger.load_all()
    return [
        ExecutionLogResponse(
            timestamp=e.timestamp.isoformat(),
            sql=e.sql,
            success=e.success,
            rows_returned=e.rows_returned,
            execution_time_ms=e.execution_time_ms,
            error=e.error,
        )
        for e in reversed(logs)
    ]


@router.get(
    "/stats",
    response_model=ObsStatsResponse,
    summary="Aggregated latency, error, and retry statistics",
)
def get_stats() -> ObsStatsResponse:

    traces = tracer.storage.load_all()
    by_node: dict[str, list] = defaultdict(list)
    for t in traces:
        by_node[t.node_name].append(t)

    node_stats = []
    for node, events in sorted(by_node.items()):
        durations = [e.duration_ms for e in events]
        errors = [e for e in events if not e.success]
        node_stats.append(
            NodeStats(
                node_name=node,
                call_count=len(events),
                avg_duration_ms=round(mean(durations), 2) if durations else 0.0,
                error_count=len(errors),
                error_rate=round(len(errors) / len(events), 4) if events else 0.0,
            )
        )

    logs = execution_logger.load_all()
    total = len(logs)
    failed = [e for e in logs if not e.success]
    error_counts: dict[str, int] = defaultdict(int)
    for e in failed:
        key = (e.error or "Unknown")[:80]
        error_counts[key] += 1

    common_errors = [
        {"error": k, "count": v}
        for k, v in sorted(error_counts.items(), key=lambda x: -x[1])[:10]
    ]

    avg_time = (
        round(mean(e.execution_time_ms for e in logs), 2) if logs else 0.0
    )

    retry_stats = RetryStats(
        total_executions=total,
        total_errors=len(failed),
        error_rate=round(len(failed) / total, 4) if total else 0.0,
        avg_execution_time_ms=avg_time,
        common_errors=common_errors,
    )

    return ObsStatsResponse(
        node_stats=node_stats,
        retry_stats=retry_stats,
    )


@router.get(
    "/evaluation",
    response_model=EvalSummaryResponse,
    summary="Return evaluation report summary",
)
def get_evaluation() -> EvalSummaryResponse:
    if not EVAL_REPORT.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No evaluation report found. Run benchmarks first.",
        )

    with open(EVAL_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    return EvalSummaryResponse(
        generated_at=summary.get("generated_at"),
        total_questions=summary.get("total_questions", 0),
        text_to_sql_accuracy=summary.get("text_to_sql_accuracy", 0.0),
        execution_accuracy=summary.get("execution_accuracy", 0.0),
        retry_success_rate=summary.get("retry_success_rate", 0.0),
        first_pass_accuracy=summary.get("first_pass_accuracy", 0.0),
        average_retry_count=summary.get("average_retry_count", 0.0),
    )
