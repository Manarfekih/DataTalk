from __future__ import annotations

import streamlit as st


def render_reasoning(reasoning: str, tables: list[str]) -> None:
    
    if not reasoning and not tables:
        return

    with st.expander("🔍 Schema Reasoning & Context", expanded=False):
        if tables:
            st.markdown("**Tables Identified:**")
            badges = " ".join([f"`{t}`" for t in tables])
            st.markdown(badges)
            st.markdown("")

        if reasoning:
            st.markdown("**Reasoning:**")
            st.markdown(reasoning)
