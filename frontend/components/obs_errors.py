from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_error_summary(stats: dict) -> None:
    """Render error summary and retry statistics panels."""

    node_stats: list[dict] = stats.get("node_stats", [])
    retry_stats: dict = stats.get("retry_stats", {})

    # ── Per-node error rate ────────────────────────────────────────────────
    st.markdown("### 🚨 Error Summary by Node")

    if not node_stats:
        st.info("No trace data available yet.")
    else:
        df_nodes = pd.DataFrame(node_stats)
        error_nodes = df_nodes[df_nodes["error_count"] > 0].copy()

        if error_nodes.empty:
            st.success("✅ No errors recorded across any graph node.")
        else:
            error_nodes["error_rate_pct"] = (
                error_nodes["error_rate"] * 100
            ).round(2)

            fig = px.bar(
                error_nodes.sort_values("error_count", ascending=True),
                x="error_count",
                y="node_name",
                orientation="h",
                color="error_rate_pct",
                color_continuous_scale="Reds",
                text="error_count",
                labels={
                    "node_name": "Node",
                    "error_count": "Errors",
                    "error_rate_pct": "Error Rate (%)",
                },
                title="Error Count per Agent Node",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                margin=dict(l=20, r=40, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title=None,
            )
            st.plotly_chart(fig, width="stretch")

    # ── Retry / SQL stats ─────────────────────────────────────────────────
    st.markdown("### 🔄 Retry Statistics")

    if not retry_stats:
        st.info("No SQL execution data available yet.")
        return

    total = retry_stats.get("total_executions", 0)
    errors = retry_stats.get("total_errors", 0)
    error_rate = retry_stats.get("error_rate", 0.0)
    avg_time = retry_stats.get("avg_execution_time_ms", 0.0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Executions", total)
    c2.metric("Errors", errors)
    c3.metric("Error Rate", f"{error_rate * 100:.1f}%")
    c4.metric("Avg Exec Time", f"{avg_time:.1f} ms")

    common_errors: list[dict] = retry_stats.get("common_errors", [])
    if common_errors:
        st.markdown("**Most Common Errors:**")
        df_err = pd.DataFrame(common_errors).rename(
            columns={"error": "Error Message", "count": "Occurrences"}
        )
        st.dataframe(df_err, width="stretch", hide_index=True)
    else:
        st.success("✅ No SQL errors recorded.")

