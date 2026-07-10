"""
SchemaSay Utilities — Interactivity Helpers

Shortcuts for toggling common layout views and clearing user text states.
"""

import streamlit as st

def toggle_sidebar() -> None:
    """Toggles sidebar collapsed flag state."""
    if "sidebar_collapsed" not in st.session_state:
        st.session_state.sidebar_collapsed = False
    st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed

def change_theme() -> None:
    """Toggles active application design theme."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

def clear_prompt() -> None:
    """Resets prompt inputs, generated SQL values, and error flags."""
    st.session_state.prompt_text = ""
    st.session_state.generated_sql = ""
    st.session_state.error_message = ""
    st.session_state.sql_generation_status = "idle"
