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

_load_css("globals.css")

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
    # Extract user profile data to dynamically populate header avatars
    user_data = response.json()
    display_name = user_data.get("full_name") or user_data.get("email") or "User"
    
    initials = "US"
    parts = display_name.split()
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1 and len(parts[0]) >= 2:
        initials = parts[0][:2].upper()

    # Load layout stylesheets
    _load_css("sidebar.css")
    _load_css("navbar.css")
    _load_css("dashboard_layout.css")
    _load_css("schemasay_ai.css")
    
    # Extract tip index query param to enable dynamic quick tip rotation
    active_tip = 0
    try:
        if "tip" in st.query_params:
            active_tip = int(st.query_params["tip"])
    except Exception:
        pass

    from components.sidebar import render_sidebar
    from components.navbar import render_navbar
    from components.schemasay_ai import render_ai_copilot_panel
    
    sidebar_content = render_sidebar(active_tip).replace("\n", "")
    navbar_content = render_navbar(title="Dashboard", display_name=display_name, initials=initials).replace("\n", "")
    
    # ── 1. Open Layout Containers ─────────────────────────────────────────────
    # Opens layout wrappers, let Streamlit draw widget columns inside them
    st.markdown(
        f'<div class="app-layout-wrapper">'
        f'<aside class="sidebar-container-shell">{sidebar_content}</aside>'
        f'<main class="main-content-container-shell">{navbar_content}'
        f'<div class="dashboard-container">', 
        unsafe_allow_html=True
    )
    
    # ── 2. Row 1: SchemaSay AI & SQL Workbench ────────────────────────────────
    row1_col1, row1_col2 = st.columns([1, 1.1])
    with row1_col1:
        st.markdown('<div class="dashboard-card card-r1-left">', unsafe_allow_html=True)
        render_ai_copilot_panel()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row1_col2:
        st.markdown('<div class="dashboard-card card-r1-right">', unsafe_allow_html=True)
        # SQL Workbench Card (Empty for Phase 5)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # ── 3. Row 2: Schema Explorer, Center tabs, Right feeds ───────────────────
    row2_col1, row2_col2, row2_col3 = st.columns([1.2, 3.2, 1.3])
    with row2_col1:
        st.markdown('<div class="dashboard-card card-r2-left">', unsafe_allow_html=True)
        # Schema Explorer Card (Empty for Phase 5)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown('<div class="dashboard-card card-r2-center">', unsafe_allow_html=True)
        # Center Panel Tabs Card (Empty for Phase 5)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row2_col3:
        st.markdown('<div class="dashboard-card card-r2-right">', unsafe_allow_html=True)
        # Right Feeds Card (Empty for Phase 5)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # ── 4. Row 3: Full Width Container ────────────────────────────────────────
    st.markdown(
        '<div class="col-row3-full">'
        '<div class="dashboard-card card-r3-full"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # ── 5. Close Layout Containers ────────────────────────────────────────────
    st.markdown('</div></main></div>', unsafe_allow_html=True)

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
