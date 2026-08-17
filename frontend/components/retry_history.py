from __future__ import annotations

import streamlit as st


def render_retry_history(retry_history: list[dict]) -> None:
   
    if not retry_history:
        return

    st.write("---")
    st.markdown("### 🔄 SQL Repair History")
    
    for attempt in retry_history:
        num = attempt.get("attempt_number", 1)
        detected_error = attempt.get("detected_error", "SQL Error")
        
        with st.expander(f"Attempt #{num}: {detected_error}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**❌ Failed SQL:**")
                st.code(attempt.get("original_sql", ""), language="sql")
                st.markdown(f"**Error Details:**\n`{attempt.get('error', '')}`")
            with col2:
                st.markdown("**✅ Corrected SQL:**")
                st.code(attempt.get("corrected_sql", ""), language="sql")
                st.markdown(f"**Confidence:** `{attempt.get('confidence', 0.0):.2f}`")
            
            st.markdown(f"**Correction Reasoning:** {attempt.get('reasoning', '')}")
            
            changes = attempt.get("changes_made", [])
            if changes:
                st.markdown("**Changes Made:**")
                for change in changes:
                    st.markdown(f"- {change}")
