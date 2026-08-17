from __future__ import annotations

from datatalk.graph.state import DataTalkState



def execution_router(state: DataTalkState):
    execution = state.get("execution")

    if execution is None:
        return "retry"

    if execution.success:
        return "success"

    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    if retry_count < max_retries:
        return "retry"

    return "explain"



def retry_router(state: DataTalkState):
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    if retry_count < max_retries:
        return "execute"

    return "explain"
