from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_trace_timeline(traces: list[dict]) -> None:
    """Render a trace events table and node latency bar chart."""

    st.markdown("### 🕸️ Agent Trace Spans")

    if not traces:
        st.info("No trace data yet. Run a query to start recording traces.")
        return

    df = pd.DataFrame(traces)

    # ── Status badges 
    df["status"] = df["success"].map(
        lambda v: "✅ OK" if v else "❌ Error"
    )
    df["duration_ms"] = df["duration_ms"].round(2)

    display_cols = [
        "node_name",
        "duration_ms",
        "status",
        "error",
        "start_time",
        "trace_id",
    ]
    display_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[display_cols].rename(columns={
            "node_name": "Node",
            "duration_ms": "Duration (ms)",
            "status": "Status",
            "error": "Error",
            "start_time": "Started",
            "trace_id": "Trace ID",
        }),
        width="stretch",
        hide_index=True,
    )

    # Node latency chart 
    st.markdown("### ⏱️ Node Latency Overview")

    latency = (
        df.groupby("node_name")["duration_ms"]
        .mean()
        .reset_index()
        .sort_values("duration_ms", ascending=True)
        .rename(columns={"node_name": "Node", "duration_ms": "Avg Duration (ms)"})
    )

    fig = px.bar(
        latency,
        x="Avg Duration (ms)",
        y="Node",
        orientation="h",
        color="Avg Duration (ms)",
        color_continuous_scale=px.colors.sequential.Plasma_r,
        text=latency["Avg Duration (ms)"].apply(lambda v: f"{v:.1f} ms"),
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        margin=dict(l=20, r=40, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_title=None,
        xaxis_title="Average Duration (ms)",
    )
    st.plotly_chart(fig, width="stretch")

