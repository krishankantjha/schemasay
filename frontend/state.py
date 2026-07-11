"""
SchemaSay Frontend — Consolidated State Manager

Centralized session and application state key constants, defaults, and lifecycle functions.
Prevents hidden coupling, circular imports, and typo-prone string literals across components and views.
"""

import streamlit as st

# ── Session State Keys ────────────────────────────────────────────────────────

# Authentication
KEY_TOKEN         = "token"
KEY_REFRESH_TOKEN = "refresh_token"

# Database connection
KEY_ACTIVE_CONNECTION_ID = "active_connection_id"


def init_session_state() -> None:
    """
    Initializes all authentication, UI navigation, alerts, and AI copilot state keys 
    with safe default values if they have not already been set. Called once at app startup.
    """
    defaults = {
        KEY_ACTIVE_CONNECTION_ID: None,
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


def clear_session_state() -> None:
    """
    Clears all user-scoped session and UI inputs values upon logout.
    Preserves Streamlit-internal keys and global configurations like theme parameters.
    """
    keys_to_clear = [
        KEY_TOKEN,
        KEY_REFRESH_TOKEN,
        KEY_ACTIVE_CONNECTION_ID,
        "profile_verified",
        "cached_profile_data",
        "selected_sidebar_item",
        "prompt_text",
        "generated_sql",
        "sql_generation_status",
        "loading",
        "error_message",
        "notifications_open",
        "profile_open",
        "search_open",
        "show_logout_dialog",
        "recent_prompts"
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
