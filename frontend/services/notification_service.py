"""
SchemaSay Services — Notification Service

Encapsulates helper functions for updating list and counter values for alerts.
"""

import streamlit as st
from typing import List, Dict

def get_notifications() -> List[Dict]:
    """Retrieves list of active alerts from session state."""
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    return st.session_state.notifications

def get_unread_count() -> int:
    """Calculates number of unread alerts."""
    return sum(1 for n in get_notifications() if n.get("unread", False))

def mark_all_as_read() -> None:
    """Clears all unread badges across alerts list."""
    notifications = get_notifications()
    for n in notifications:
        n["unread"] = False
    st.session_state.notifications = notifications

def clear_notifications() -> None:
    """Wipes all notifications records."""
    st.session_state.notifications = []
