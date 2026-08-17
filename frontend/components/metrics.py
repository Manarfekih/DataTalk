from __future__ import annotations

import streamlit as st


def render_metrics(response):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Rows",

        response["row_count"],

    )

    c2.metric(

        "Execution",

        f"{response['execution_time_ms']:.2f} ms",

    )

    c3.metric(

        "Retries",

        response["retry_count"],

    )

    c4.metric(

        "Total",

        f"{response['total_time_ms']:.2f} ms",

    )