"""
SchemaSay Frontend — Application Entrypoint

Responsibilities:
  1. Configure Streamlit page settings.
  2. Load global CSS design system.
  3. Initialize session state.
  4. Gate unauthenticated users to the auth page.
  5. Verify tokens with the backend and handle refresh/expiry.
  6. Render the appropriate page for authenticated users.
"""

import os
import streamlit as st
from api_client import api_client
from views.auth_view import show_auth_page
from state import KEY_TOKEN, KEY_REFRESH_TOKEN, init_session_state

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SchemaSay",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load Design System CSS ────────────────────────────────────────────────────
def _load_css(filename: str) -> None:
    """Injects a CSS file from the styles/ directory into the Streamlit page."""
    path = os.path.join(os.path.dirname(__file__), "styles", filename)
    if os.path.exists(path):
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

_load_css("variables.css")
_load_css("base.css")

# ── Session State Initialization ──────────────────────────────────────────────
init_session_state()

# ── Auth Gate ─────────────────────────────────────────────────────────────────
if KEY_TOKEN not in st.session_state:
    # Not logged in — show auth page (loads auth.css internally)
    _load_css("auth.css")
    show_auth_page()
    st.stop()

# ── Token Verification ────────────────────────────────────────────────────────
token = st.session_state[KEY_TOKEN]

with st.spinner("Verifying session..."):
    response = api_client.get_me(token)

if response.status_code == 200:
    # ── Authenticated: render dashboard
    # Dashboard pages will be imported here during Phase 10 rebuild.
    st.info(
        "✅ Authenticated successfully. Dashboard is being rebuilt — coming in the next phase.",
        icon="🔷",
    )
    st.stop()

elif response.status_code == 401 and KEY_REFRESH_TOKEN in st.session_state:
    # Access token expired — attempt silent refresh
    with st.spinner("Session expired. Renewing..."):
        refresh_res = api_client.refresh(st.session_state[KEY_REFRESH_TOKEN])

    if refresh_res.status_code == 200:
        res_data = refresh_res.json()
        st.session_state[KEY_TOKEN] = res_data["access_token"]
        st.session_state[KEY_REFRESH_TOKEN] = res_data["refresh_token"]
        st.rerun()
    else:
        # Refresh also failed — clear credentials and redirect to login
        st.session_state.pop(KEY_TOKEN, None)
        st.session_state.pop(KEY_REFRESH_TOKEN, None)
        st.error("Your session has expired. Please log in again.")
        st.rerun()

else:
    # Any other auth failure — clear and redirect
    st.session_state.pop(KEY_TOKEN, None)
    st.session_state.pop(KEY_REFRESH_TOKEN, None)
    st.error("Authentication failed. Please log in again.")
    st.rerun()
