from __future__ import annotations

import streamlit as st


def render_sql(sql: str):

    with st.expander(

        "📝 Generated SQL",

        expanded=False,

    ):

        st.code(

            sql,

            language="sql",

        )