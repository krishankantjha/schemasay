import streamlit as st
from typing import Any, Optional, List, Dict

# Centralized session state key definitions to prevent hidden coupling and typo-prone bugs
KEY_TOKEN = "token"
KEY_REFRESH_TOKEN = "refresh_token"
KEY_ACTIVE_CONNECTION_ID = "active_connection_id"
KEY_WORKBENCH_SQL = "workbench_sql_input"
KEY_QUERY_HISTORY = "active_query_history"
KEY_ACTIVE_TAB = "active_tab"
KEY_HISTORY_PAGE = "history_page"

def init_session_state() -> None:
    """
    Initializes session state keys with default values safely if not present.
    """
    if KEY_ACTIVE_TAB not in st.session_state:
        st.session_state[KEY_ACTIVE_TAB] = "AI Copilot"
    if KEY_WORKBENCH_SQL not in st.session_state:
        st.session_state[KEY_WORKBENCH_SQL] = "SELECT * FROM <table_name> LIMIT 10"
    if KEY_HISTORY_PAGE not in st.session_state:
        st.session_state[KEY_HISTORY_PAGE] = 1

def clear_session_state() -> None:
    """
    Clears all user session values from state upon logout.
    """
    keys_to_clear = [
        KEY_TOKEN, KEY_REFRESH_TOKEN, KEY_ACTIVE_CONNECTION_ID,
        KEY_WORKBENCH_SQL, KEY_QUERY_HISTORY, KEY_ACTIVE_TAB,
        KEY_HISTORY_PAGE
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
