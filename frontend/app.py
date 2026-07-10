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
    
    # ── 1. Render Navigation & Headers ────────────────────────────────────────
    # Render custom styled sidebar inside Streamlit's native sidebar structure
    st.sidebar.markdown(sidebar_content, unsafe_allow_html=True)
    
    # Render Top Navbar sticky at the top of main content block
    st.markdown(navbar_content, unsafe_allow_html=True)
    
    # ── 2. Render Main Grid Canvas ───────────────────────────────────────────
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Row 1: SchemaSay AI & SQL Workbench
    row1_col1, row1_col2 = st.columns([1, 1.1])
    with row1_col1:
        with st.container(border=True):
            st.markdown('<div class="card-height-r1"></div>', unsafe_allow_html=True)
            render_ai_copilot_panel()
            
    with row1_col2:
        with st.container(border=True):
            st.markdown('<div class="card-height-r1"></div>', unsafe_allow_html=True)
            # SQL Workbench (Empty for Phase 5)
            pass
            
    # Row 2: Schema Explorer, Center panel, Right feeds
    row2_col1, row2_col2, row2_col3 = st.columns([1.2, 3.2, 1.3])
    with row2_col1:
        with st.container(border=True):
            st.markdown('<div class="card-height-r2"></div>', unsafe_allow_html=True)
            # Schema Explorer (Empty for Phase 5)
            pass
            
    with row2_col2:
        with st.container(border=True):
            st.markdown('<div class="card-height-r2"></div>', unsafe_allow_html=True)
            # Center Panel (Empty for Phase 5)
            pass
            
    with row2_col3:
        with st.container(border=True):
            st.markdown('<div class="card-height-r2"></div>', unsafe_allow_html=True)
            # Right Feeds (Empty for Phase 5)
            pass
            
    # ── 4. Row 3: Full Width Container ────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<div class="card-height-r3"></div>', unsafe_allow_html=True)
        # Footer Card (Empty for Phase 5)
        pass
        
    # ── 5. Close Layout Containers ────────────────────────────────────────────
    st.markdown('</div>', unsafe_allow_html=True)

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
