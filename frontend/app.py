import os
import streamlit as st
from api_client import api_client
from views.auth_view import show_auth_page
from state import KEY_TOKEN, KEY_REFRESH_TOKEN, KEY_ACTIVE_CONNECTION_ID, init_session_state

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SchemaSay",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
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

# Cache profile data to avoid backend spamming on every rerun/click
verified = st.session_state.get("profile_verified", False)
cached_user_data = st.session_state.get("cached_profile_data", None)
status_code = None

if not verified or cached_user_data is None:
    with st.spinner("Verifying session..."):
        response = api_client.get_me(token)
    
    if response.status_code == 200:
        cached_user_data = response.json()
        st.session_state.profile_verified = True
        st.session_state.cached_profile_data = cached_user_data
        status_code = 200
    else:
        status_code = response.status_code
else:
    status_code = 200

if status_code == 200:
    user_data = cached_user_data
    display_name = user_data.get("full_name") or user_data.get("email") or "User"
    
    initials = "US"
    parts = display_name.split()
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1 and len(parts[0]) >= 2:
        initials = parts[0][:2].upper()

    # ── Action Bus Event Interceptor ──────────────────────────────────────────
    if "prompt" in st.query_params:
        st.session_state.prompt_text = st.query_params["prompt"]
        st.query_params.pop("prompt", None)
        st.rerun()

    if "action" in st.query_params:
        action = st.query_params["action"]
        
        # Toggle sidebar collapse
        if action == "toggle_sidebar":
            from utils.helpers import toggle_sidebar
            toggle_sidebar()
        # Toggle light/dark theme preference
        elif action == "toggle_theme":
            from utils.helpers import change_theme
            change_theme()
        # Toggles notifications panel dropdown
        elif action == "toggle_notifications":
            st.session_state.notifications_open = not st.session_state.notifications_open
            st.session_state.profile_open = False
        # Toggles profile details dropdown
        elif action == "toggle_profile":
            st.session_state.profile_open = not st.session_state.profile_open
            st.session_state.notifications_open = False
        # Toggles inline global search bar display
        elif action == "toggle_search":
            st.session_state.search_open = not st.session_state.search_open
        # Clears all unread badges from notifications
        elif action == "mark_read":
            from services.notification_service import mark_all_as_read
            mark_all_as_read()
            st.session_state.notifications_open = True
            
        # Quick Tip navigation index sets
        elif action.startswith("tip_"):
            try:
                st.session_state.current_tip_index = int(action[4:])
            except Exception:
                pass
                
        # Sidebar primary menu navigation links
        elif action.startswith("nav_"):
            page = action[4:]
            st.session_state.selected_sidebar_item = page
            # Close popup overlays on navigate
            st.session_state.notifications_open = False
            st.session_state.profile_open = False
            st.session_state.search_open = False
            
        # Logout triggers
        elif action == "logout":
            st.session_state.show_logout_dialog = True
            st.session_state.profile_open = False
        elif action == "confirm_logout":
            # Invalidate backend JWT session token before clearing local state variables
            try:
                api_client.logout(token)
            except Exception:
                pass
            from state import clear_session_state
            clear_session_state()
            st.session_state.show_logout_dialog = False
            st.query_params.clear()
            st.rerun()
        elif action == "cancel_logout":
            st.session_state.show_logout_dialog = False
            
        st.query_params.pop("action", None)
        st.rerun()

    # Load layout stylesheets
    _load_css("sidebar.css")
    _load_css("navbar.css")
    _load_css("dashboard_layout.css")
    _load_css("schemasay_ai.css")
    
    # ── Dynamic Theme Colors Override ─────────────────────────────────────────
    if st.session_state.get("theme") == "dark":
        st.markdown(
            """
            <style>
            :root {
                --color-bg-app: #0B0F19 !important;      /* Slate 950 dark background */
                --color-bg-card: #1E293B !important;     /* Slate 800 card */
                --color-border: #334155 !important;      /* Slate 700 borders */
                --color-text-primary: #F8FAFC !important;/* Light text */
                --color-text-secondary: #94A3B8 !important;
                --color-text-muted: #64748B !important;
                --color-bg-input: #0F172A !important;
            }
            /* Native Streamlit border card backgrounds */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: var(--color-bg-card) !important;
                border-color: var(--color-border) !important;
            }
            /* Text inputs override */
            div[data-testid="stTextArea"] textarea {
                background-color: var(--color-bg-input) !important;
                border-color: var(--color-border) !important;
                color: var(--color-text-primary) !important;
            }
            /* Code editor border preview */
            .sql-preview-container {
                border-color: var(--color-border) !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # ── Dynamic Header Title Mapping ──────────────────────────────────────────
    PAGE_TITLES = {
        "dashboard": "Dashboard",
        "connections": "Connections",
        "upload": "Upload File",
        "schema": "Schema Explorer",
        "schemasay_ai": "SchemaSay AI",
        "workbench": "SQL Workbench",
        "history": "Query History",
        "visualizations": "Visualizations",
        "results": "Results",
        "insights": "Insights",
        "settings": "Settings",
        "help": "Help"
    }
    active_nav_id = st.session_state.get("selected_sidebar_item", "dashboard")
    page_title = PAGE_TITLES.get(active_nav_id, "Dashboard")

    from components.sidebar import render_sidebar
    from components.navbar import render_navbar
    
    active_tip = st.session_state.get("current_tip_index", 0)
    sidebar_content = render_sidebar(active_tip).replace("\n", "")
    navbar_content = render_navbar(title=page_title, display_name=display_name, initials=initials).replace("\n", "")
    
    # ── 1. Render Navigation & Headers ────────────────────────────────────────
    # Render custom styled sidebar inside Streamlit's native sidebar structure
    st.sidebar.markdown(sidebar_content, unsafe_allow_html=True)
    
    # Render Top Navbar sticky at the top of main content block
    st.markdown(navbar_content, unsafe_allow_html=True)

    # ── 1.5 Render Main Page View Layouts ─────────────────────────────────────
    if active_nav_id == "schemasay_ai":
        # Process SQL generation via real backend FastAPI endpoint
        if st.session_state.get("sql_generation_status") == "loading":
            token = st.session_state[KEY_TOKEN]
            connection_id = st.session_state.get(KEY_ACTIVE_CONNECTION_ID)
            
            # Fetch connections dynamically if not cached/defaulted yet
            if not connection_id:
                try:
                    from utils.caching import get_cached_connections
                    conns = get_cached_connections(token)
                    if conns:
                        connection_id = conns[0]["id"]
                        st.session_state[KEY_ACTIVE_CONNECTION_ID] = connection_id
                except Exception:
                    pass
            
            if not connection_id:
                st.session_state.error_message = "No configured database connections found. Please configure a connection first under the Connections menu."
                st.session_state.sql_generation_status = "error"
                st.rerun()
            else:
                with st.spinner("Translating natural prompt into SQL structure..."):
                    try:
                        response = api_client.query_assistant(token, connection_id, st.session_state.prompt_text)
                        if response.status_code == 200:
                            res_data = response.json()
                            st.session_state.generated_sql = res_data.get("sql", "")
                            st.session_state.sql_generation_status = "success"
                            
                            # Append to recent prompts
                            if st.session_state.prompt_text not in st.session_state.recent_prompts:
                                st.session_state.recent_prompts.append(st.session_state.prompt_text)
                        else:
                            try:
                                err_detail = response.json().get("detail", "Failed to compile SQL query.")
                            except Exception:
                                err_detail = f"Database server error: {response.text[:200]}"
                            st.session_state.error_message = err_detail
                            st.session_state.sql_generation_status = "error"
                    except Exception as e:
                        st.session_state.error_message = f"Backend connection failed: {str(e)}"
                        st.session_state.sql_generation_status = "error"
                st.rerun()

        # Render the AI Copilot UI
        from components.schemasay_ai import render_ai_copilot_panel
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        # Double-container layout with empty slots matching visual mockup
        row1_col1, row1_col2 = st.columns([1, 1.1])
        with row1_col1:
            with st.container(border=True):
                st.markdown('<div class="card-height-r1"></div>', unsafe_allow_html=True)
                render_ai_copilot_panel()
        with row1_col2:
            with st.container(border=True):
                st.markdown('<div class="card-height-r1"></div>', unsafe_allow_html=True)
                st.write("#### SQL Workbench")
                st.info("Select a query or type SQL directly to run execution plans.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif active_nav_id == "connections":
        from views.connect_view import show_connection_manager
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        show_connection_manager()
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif active_nav_id != "dashboard":
        # Default placeholder views for other items
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.write(f"### {page_title}")
        st.info(f"The {page_title} dashboard module is loaded successfully.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ── 2. Render Confirm Logout Dialogue Modal ──────────────────────────────
    if st.session_state.get("show_logout_dialog", False):
        st.markdown(
            '<div style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(15,23,42,0.65); display:flex; align-items:center; justify-content:center; z-index:999999;">'
            '<div style="background:var(--color-bg-card); padding:24px; border-radius:12px; border:1px solid var(--color-border); box-shadow:var(--shadow-lg); width:320px; display:flex; flex-direction:column; gap:16px;">'
            '<div style="font-family:var(--font-display); font-weight:700; font-size:15px; color:var(--color-text-primary);">Confirm Logout</div>'
            '<div style="font-size:12px; color:var(--color-text-secondary); line-height:1.5;">Are you sure you want to end your active session and sign out of SchemaSay?</div>'
            '<div style="display:flex; justify-content:flex-end; gap:8px;">'
            '<a href="?action=cancel_logout" target="_self" style="padding:6px 14px; background:var(--color-bg-app); border:1px solid var(--color-border); border-radius:8px; text-decoration:none; color:var(--color-text-primary); font-size:11px; font-weight:600; display:inline-block; transition:var(--transition-fast);">Cancel</a>'
            '<a href="?action=confirm_logout" target="_self" style="padding:6px 14px; background:#EF4444; border-radius:8px; text-decoration:none; color:#FFFFFF; font-size:11px; font-weight:600; display:inline-block; box-shadow:0 1px 2px rgba(0,0,0,0.05); transition:var(--transition-fast);">Log Out</a>'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

elif status_code == 401 and KEY_REFRESH_TOKEN in st.session_state:
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
