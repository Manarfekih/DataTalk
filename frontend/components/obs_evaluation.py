from __future__ import annotations

import streamlit as st


def render_evaluation(eval_data: dict | None) -> None:
    """Render evaluation metric cards from the latest benchmark report."""

    st.markdown("### 📊 Evaluation Metrics")

    if eval_data is None:
        st.warning(
            "No evaluation report found. "
            "Run benchmarks with `python -m datatalk.benchmarks` to generate one."
        )
        return

    generated_at = eval_data.get("generated_at", "—")
    st.caption(f"Report generated: {generated_at}")

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    total = eval_data.get("total_questions", 0)
    txt_acc = eval_data.get("text_to_sql_accuracy", 0.0)
    exec_acc = eval_data.get("execution_accuracy", 0.0)
    retry_sr = eval_data.get("retry_success_rate", 0.0)
    first_pass = eval_data.get("first_pass_accuracy", 0.0)
    avg_retry = eval_data.get("average_retry_count", 0.0)

    c1.metric("Total Questions", total)
    c2.metric("Text-to-SQL Accuracy", f"{txt_acc * 100:.1f}%")
    c3.metric("Execution Accuracy", f"{exec_acc * 100:.1f}%")
    c4.metric("Retry Success Rate", f"{retry_sr * 100:.1f}%")
    c5.metric("First-Pass Accuracy", f"{first_pass * 100:.1f}%")
    c6.metric("Avg Retry Count", f"{avg_retry:.2f}")

    st.divider()

    # Progress bar overview
    st.markdown("**Accuracy at a glance:**")

    metrics = {
        "Text-to-SQL Accuracy": txt_acc,
        "Execution Accuracy": exec_acc,
        "First-Pass Accuracy": first_pass,
        "Retry Success Rate": retry_sr,
    }
    for label, value in metrics.items():
        col1, col2 = st.columns([3, 7])
        col1.markdown(f"**{label}**")
        col2.progress(min(max(value, 0.0), 1.0))
