from __future__ import annotations

import streamlit as st

from pages import chat, observability
from styles import load_css

# Page config
st.set_page_config(
    page_title="DataTalk",
    layout="wide",
    page_icon="📊",
)

load_css()

# Role selector
if "role" not in st.session_state:
    st.session_state.role = "Normal User"

with st.sidebar:
    st.markdown("---")
    st.session_state.role = st.radio(
        "👤 View Mode",
        options=["Normal User", "Admin / Developer"],
        index=0 if st.session_state.role == "Normal User" else 1,
        horizontal=False,
    )
    st.markdown("---")

# Navigation
pages = [
    st.Page(
        chat.render,
        title="Chat",
        icon="💬",
        url_path="chat",
        default=True,
    ),
]

if st.session_state.role == "Admin / Developer":
    pages.append(
        st.Page(
            observability.render,
            title="Observability",
            icon="🔭",
            url_path="observability",
        )
    )

page = st.navigation(pages)
page.run()
