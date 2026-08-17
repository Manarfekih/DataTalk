from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_chart(rows: list[dict]) -> None:
    if not rows:
        return

    df = pd.DataFrame(rows)

    for col in df.columns:
        if df[col].dtype == "object":
            try:
                if df[col].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}").any():
                    df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    datetime_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    categorical_cols = [
        c for c in df.columns if c not in numeric_cols and c not in datetime_cols
    ]

    if not numeric_cols:
        st.info("This result does not contain numeric values to chart.")
        return

    default_chart = "Bar"
    x_col = None
    y_col = numeric_cols[0]

    if datetime_cols:
        x_col = datetime_cols[0]
        default_chart = "Line"
    elif categorical_cols:
        x_col = categorical_cols[0]
        if len(df[x_col].unique()) <= 6:
            default_chart = "Pie"
        else:
            default_chart = "Bar"
    elif len(numeric_cols) >= 2:
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        default_chart = "Scatter"
    else:
        x_col = "index"
        df = df.reset_index()
        default_chart = "Bar"

    chart_id = f"chart_select_{len(rows)}_{'_'.join(map(str, df.columns[:3]))}"

    st.write("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Interactive Visualization")
    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Line", "Area", "Pie", "Scatter"],
            index=["Bar", "Line", "Area", "Pie", "Scatter"].index(default_chart),
            key=chart_id,
        )

    layout_style = dict(
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    try:
        color_col = categorical_cols[0] if categorical_cols else None

        if chart_type == "Bar":
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{y_col} by {x_col}",
            )
        elif chart_type == "Line":
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{y_col} over {x_col}",
                markers=True,
            )
        elif chart_type == "Area":
            fig = px.area(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{y_col} Cumulative Area Chart",
            )
        elif chart_type == "Pie":
            fig = px.pie(
                df,
                names=x_col or df.index,
                values=y_col,
                hole=0.4,
                title=f"Distribution of {y_col}",
            )
        elif chart_type == "Scatter":
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{y_col} vs {x_col}",
            )
        else:
            fig = None

        if fig:
            fig.update_layout(layout_style)
            st.plotly_chart(fig, width="stretch")
    except Exception as e:
        st.error(f"Error rendering Plotly chart: {e}")

