import streamlit as st
from api_client import api_client
from views.auth_view import show_auth_page
from views.connect_view import show_connection_manager
from views.query_view import show_query_assistant_panel
from views.sidebar_view import render_sidebar_view
from state import KEY_TOKEN, KEY_REFRESH_TOKEN, init_session_state

st.set_page_config(
    page_title="SchemaSay",
    layout="wide"
)

# Load global CSS styling overrides
import os
css_path = os.path.join(os.path.dirname(__file__), "index.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_session_state()

# Check if the user is logged in
if KEY_TOKEN not in st.session_state:
    show_auth_page()
else:
    token = st.session_state[KEY_TOKEN]
    
    # Query backend user profile
    with st.spinner("Verifying secure session..."):
        response = api_client.get_me(token)
    
    if response.status_code == 200:
        # Render the sidebar component (returns the navigation selection)
        page = render_sidebar_view()
        
        # Render corresponding page based on active page selection
        if page == "Database Connections":
            show_connection_manager()
        else:
            show_query_assistant_panel()
            
    elif response.status_code == 401 and KEY_REFRESH_TOKEN in st.session_state:
        # Access token expired — try to renew it using the refresh token
        with st.spinner("Session expired. Attempting secure renewal..."):
            refresh_response = api_client.refresh(st.session_state[KEY_REFRESH_TOKEN])
            
        if refresh_response.status_code == 200:
            res_data = refresh_response.json()
            st.session_state[KEY_TOKEN] = res_data["access_token"]
            st.session_state[KEY_REFRESH_TOKEN] = res_data["refresh_token"]
            st.rerun()
        else:
            # Session expired and cannot be renewed
            st.session_state.pop(KEY_TOKEN, None)
            st.session_state.pop(KEY_REFRESH_TOKEN, None)
            st.error("Session has expired. Please log in again.")
            st.rerun()
    else:
        # Any other error, clear credentials
        st.session_state.pop(KEY_TOKEN, None)
        st.session_state.pop(KEY_REFRESH_TOKEN, None)
        st.error("Authentication check failed. Please log in again.")
        st.rerun()
