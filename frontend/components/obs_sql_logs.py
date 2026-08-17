from __future__ import annotations

import pandas as pd
import streamlit as st


def render_sql_logs(executions: list[dict]) -> None:
    """Render the SQL execution log with success/failure colouring."""

    st.markdown("### 🗄️ SQL Execution Logs")

    if not executions:
        st.info("No SQL execution logs yet. Run a query to start recording.")
        return

    df = pd.DataFrame(executions)
    df["status"] = df["success"].map(lambda v: "✅ OK" if v else "❌ Failed")
    df["execution_time_ms"] = df["execution_time_ms"].round(2)

    # Summary metrics
    total = len(df)
    succeeded = df["success"].sum()
    failed = total - succeeded
    avg_time = df["execution_time_ms"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Queries", total)
    c2.metric("Successful", int(succeeded))
    c3.metric("Failed", int(failed))
    c4.metric("Avg Time", f"{avg_time:.1f} ms")

    st.divider()

    # Filter
    show_failed_only = st.checkbox(
        "Show failed only",
        key="sql_log_filter_failed",
    )
    view = df[~df["success"]] if show_failed_only else df

    display_cols = [
        "timestamp",
        "status",
        "execution_time_ms",
        "rows_returned",
        "sql",
        "error",
    ]
    display_cols = [c for c in display_cols if c in view.columns]

    st.dataframe(
        view[display_cols].rename(columns={
            "timestamp": "Timestamp",
            "status": "Status",
            "execution_time_ms": "Time (ms)",
            "rows_returned": "Rows",
            "sql": "SQL",
            "error": "Error",
        }),
        width="stretch",
        hide_index=True,
    )

