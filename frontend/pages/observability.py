from __future__ import annotations

import requests
import streamlit as st

from api import DataTalkAPI
from components.obs_traces import render_trace_timeline
from components.obs_sql_logs import render_sql_logs
from components.obs_errors import render_error_summary
from components.obs_evaluation import render_evaluation

api = DataTalkAPI()



def _fetch_safe(method_name: str) -> object | None:
    try:
        return getattr(api, method_name)()
    except (requests.ConnectionError, requests.Timeout, RuntimeError):
        return None
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            return None
        return None
    except Exception:
        return None



def render() -> None:

    st.markdown(
        """
        <style>
        .obs-header {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            border-radius: 16px;
            padding: 28px 36px;
            margin-bottom: 28px;
        }
        .obs-header h1 {
            color: #e0d7ff;
            font-size: 2rem;
            margin: 0 0 6px 0;
        }
        .obs-header p {
            color: #a89fd4;
            font-size: 0.95rem;
            margin: 0;
        }
        .obs-badge {
            display: inline-block;
            background: #7c3aed;
            color: white;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 20px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        </style>
        <div class="obs-header">
            <div class="obs-badge">Admin · Developer View</div>
            <h1>🔭 Observability Dashboard</h1>
            <p>Real-time agent traces · SQL logs · Error analysis · Evaluation metrics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_refresh, col_info = st.columns([1, 5])
    with col_refresh:
        refresh = st.button("🔄 Refresh Data", width="stretch")
    with col_info:
        st.caption(
            "Data is read from `logs/traces.json`, `logs/executions.json`, "
            "and `reports/evaluation.json`."
        )

    if refresh:
        st.cache_data.clear()

    # Fetch all data 
    with st.spinner("Loading observability data..."):
        traces = _fetch_safe("get_traces") or []
        executions = _fetch_safe("get_executions") or []
        stats = _fetch_safe("get_stats") or {}
        evaluation = _fetch_safe("get_evaluation")  

    # API offline banner 
    if not traces and not executions and not stats:
        st.warning(
            "⚠️ Could not reach the DataTalk API. "
            "Make sure the backend is running at the URL configured in `.env`."
        )

    # Tabs 
    tab_traces, tab_sql, tab_errors, tab_eval = st.tabs([
        "🕸️ Agent Traces & Latency",
        "🗄️ SQL Logs",
        "🚨 Errors & Retries",
        "📊 Evaluation Metrics",
    ])

    with tab_traces:
        render_trace_timeline(traces)

    with tab_sql:
        render_sql_logs(executions)

    with tab_errors:
        render_error_summary(stats)

    with tab_eval:
        render_evaluation(evaluation)

