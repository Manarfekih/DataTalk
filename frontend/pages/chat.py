from __future__ import annotations

import requests
import streamlit as st

from api import DataTalkAPI
from components.sidebar import render_sidebar
from components.conversation import (
    init_conversation,
    add_message,
    render_conversation_history,
    stream_text,
    render_response_details,
)

api = DataTalkAPI()


def render() -> None:
    """Render the Chat Interface page."""

    render_sidebar(api)
    init_conversation()

    st.title("DataTalk")
    st.caption("Conversational Analytics Agent powered by LangGraph")

    render_conversation_history()

    question = None
    if st.session_state.get("clicked_question"):
        question = st.session_state.clicked_question
        st.session_state.clicked_question = None

    if not question:
        question = st.chat_input("Ask a business question...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)
        add_message("user", question)

        try:
            with st.spinner("Thinking..."):
                response = api.ask(question)

            explanation = response.get(
                "explanation", "Here is the data matching your query:"
            )

            with st.chat_message("assistant"):
                stream_text(explanation)
                render_response_details(response)

            add_message("assistant", explanation, response_data=response)
            st.rerun()

        except (requests.ConnectionError, requests.Timeout, RuntimeError) as exc:
            st.error(str(exc))
        except requests.HTTPError as exc:
            st.error(f"API Error: {exc}")
        except Exception as exc:
            st.exception(exc)
