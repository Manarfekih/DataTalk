from __future__ import annotations

import streamlit as st


def render_chat_message(
    role: str,
    content: str,
) -> None:

    if role == "user":

        st.chat_message("user").write(content)

    else:

        st.chat_message("assistant").write(content)