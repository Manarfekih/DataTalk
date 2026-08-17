from __future__ import annotations

import streamlit as st
import time
from components.reasoning import render_reasoning
from components.metrics import render_metrics
from components.sql_viewer import render_sql
from components.result_table import render_table
from components.charts import render_chart
from components.retry_history import render_retry_history


def init_conversation() -> None:
   
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(role: str, content: str, response_data: dict | None = None) -> None:
   
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "response_data": response_data,
    })


def stream_text(text: str, delay: float = 0.005) -> None:
    
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text + "▌")
        time.sleep(delay)
    placeholder.markdown(full_text)


def render_response_details(response_data: dict) -> None:
    
    # 1. Schema Exploration Reasoning
    if response_data.get("reasoning") or response_data.get("tables"):
        render_reasoning(
            response_data.get("reasoning", ""),
            response_data.get("tables", [])
        )

    # 2. Execution Performance Metrics
    render_metrics(response_data)

    # 3. Final Executed SQL Query
    if response_data.get("sql_query"):
        render_sql(response_data["sql_query"])

    # 4. Repairing & Retry Logs
    if response_data.get("retry_history"):
        render_retry_history(response_data["retry_history"])

    # 5. Data Table Viewer
    if response_data.get("rows"):
        render_table(response_data["rows"])

    # 6. Plotly Auto-Selected Visualization
    if response_data.get("rows"):
        render_chart(response_data["rows"])


def render_conversation_history() -> None:
   
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        response_data = message.get("response_data")

        with st.chat_message(role):
            st.markdown(content)
            if role == "assistant" and response_data:
                render_response_details(response_data)
