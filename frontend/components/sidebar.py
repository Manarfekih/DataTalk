from __future__ import annotations

import streamlit as st


EXAMPLES = [
    "How many customers are there?",
    "Top 10 products by sales",
    "Revenue by country",
    "Orders last month",
    "Top employees by revenue",
]


def render_sidebar(api) -> None:
   
    st.sidebar.title("📊 DataTalk")
    st.sidebar.caption("Conversational Database Agent")
    st.sidebar.divider()

    # Clear Chat History Button
    if st.sidebar.button("🧹 Clear Chat History", width="stretch"):
        st.session_state.messages = []
        if "clicked_question" in st.session_state:
            st.session_state.clicked_question = None
        st.success("Chat history cleared!")
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("💡 Example Questions")
    st.sidebar.info("Click a question below to run it directly:")

    for question in EXAMPLES:
        if st.sidebar.button(question, width="stretch", key=f"btn_{question}"):
            st.session_state.clicked_question = question
            st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("🔌 System Status")

    try:
        health = api.health()
        
        st.sidebar.markdown(
            '<div class="sidebar-status-container">'
            'API: <span class="status-pill status-online">● Online</span>'
            '</div>',
            unsafe_allow_html=True
        )

        db_status = "● Connected" if health.get("database") else "○ Disconnected"
        db_class = "status-online" if health.get("database") else "status-offline"
        
        st.sidebar.markdown(
            f'<div>Database: <span class="status-pill {db_class}">{db_status}</span></div>',
            unsafe_allow_html=True
        )

        llm_status = "● Ready" if health.get("llm") else "○ Unavailable"
        llm_class = "status-online" if health.get("llm") else "status-offline"
        
        st.sidebar.markdown(
            f'<div style="margin-top: 8px;">LLM: <span class="status-pill {llm_class}">{llm_status}</span></div>',
            unsafe_allow_html=True
        )

    except Exception:
        st.sidebar.markdown(
            '<div class="sidebar-status-container">'
            'API: <span class="status-pill status-offline">● Offline</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.sidebar.warning("Could not establish a connection to the backend service.")
