"""
SchemaSay Frontend — Session State Manager

Centralized session state key constants and lifecycle functions.
Prevents hidden coupling and typo-prone string literals across views.
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
    Initializes all required session state keys with safe default values
    if they have not already been set. Called once at app startup.
    """
    defaults = {
        KEY_ACTIVE_CONNECTION_ID: None,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def clear_session_state() -> None:
    """
    Clears all user-scoped session values upon logout.
    Preserves Streamlit-internal keys to avoid rerun side effects.
    """
    keys_to_clear = [
        KEY_TOKEN,
        KEY_REFRESH_TOKEN,
        KEY_ACTIVE_CONNECTION_ID,
        "profile_verified",
        "cached_profile_data",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
