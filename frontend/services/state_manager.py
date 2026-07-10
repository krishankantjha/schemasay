"""
SchemaSay Services — State Manager

Defines all central st.session_state configuration defaults for frontend interactivity.
"""

import streamlit as st

def init_application_states() -> None:
    """
    Initializes all interactive frontend state parameters with safe defaults
    on initial user session load.
    """
    defaults = {
        "current_page": "dashboard",
        "selected_sidebar_item": "dashboard",
        "prompt_text": "",
        "generated_sql": "",
        "sql_generation_status": "idle",  # "idle" | "loading" | "success" | "error"
        "loading": False,
        "notifications": [
            {"id": 1, "text": "PostgreSQL database connected successfully", "unread": True, "time": "2 mins ago"},
            {"id": 2, "text": "New schema reflections compiled for public tables", "unread": True, "time": "1 hr ago"},
            {"id": 3, "text": "Security backup complete for credentials key", "unread": False, "time": "1 day ago"}
        ],
        "theme": "light",                  # "light" | "dark"
        "connection_status": "Connected to PostgreSQL",
        "user_information": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "role": "Administrator"
        },
        "sidebar_collapsed": False,
        "recent_prompts": [],
        "error_message": "",
        "current_tip_index": 0,
        "notifications_open": False,
        "profile_open": False,
        "search_open": False,
        "show_logout_dialog": False
    }

    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
