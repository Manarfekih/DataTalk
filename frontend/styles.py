from __future__ import annotations

import streamlit as st


def load_css() -> None:

    st.markdown(
        """
<style>
/* Page Layout */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Base card styling using Streamlit variables */
.metric-card {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.15);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-align: center;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    border-color: var(--primary-color);
}

/* User Message Styling overlay */
.user-message {
    background-color: rgba(0, 104, 249, 0.1);
    border-left: 4px solid var(--primary-color);
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    color: var(--text-color);
}

/* Assistant Message Styling overlay */
.assistant-message {
    background-color: var(--secondary-background-color);
    border-left: 4px solid #10b981;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    color: var(--text-color);
}

/* SQL Viewer styling */
.sql-box {
    background-color: #1a1a1a;
    color: #9cdcfe;
    padding: 16px;
    border-radius: 8px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.9rem;
    line-height: 1.5;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow-x: auto;
}

/* Sidebar Customizations */
.sidebar-status-container {
    background-color: rgba(128, 128, 128, 0.08);
    padding: 12px;
    border-radius: 8px;
    border: 1px solid rgba(128, 128, 128, 0.15);
    margin-bottom: 10px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 12px;
}

.status-online {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
}

.status-offline {
    background-color: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

/* Custom Scrollbar for better browser experience */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(128, 128, 128, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(128, 128, 128, 0.5);
}

</style>
        """,
        unsafe_allow_html=True,
    )