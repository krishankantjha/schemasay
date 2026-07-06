import streamlit as st
from api_client import api_client
from views.auth_view import show_auth_page
from views.connect_view import show_connection_manager

st.set_page_config(
    page_title="SchemaSay",
    layout="wide"
)

st.title("SchemaSay")
st.subheader("Your AI-Powered SQL Analytics Platform")

st.write("---")

# Verify user session status
if "token" not in st.session_state:
    show_auth_page()
else:
    token = st.session_state["token"]
    
    # Query backend user profile
    with st.spinner("Verifying secure session..."):
        response = api_client.get_me(token)
    
    if response.status_code == 200:
        # Successful validation
        user_data = response.json()
        display_name = user_data.get("full_name") or user_data.get("email")
        
        # Configure Sidebar Navigation Panel
        st.sidebar.title("SchemaSay")
        st.sidebar.write(f"Logged in as: **{display_name}**")
        st.sidebar.markdown("---")
        
        page = st.sidebar.radio(
            "Navigation Menu",
            options=["Query Assistant", "Database Connections"]
        )
        
        st.sidebar.markdown("---")
        # Logout handles local state and issues backend revocation
        if st.sidebar.button("Log Out"):
            with st.spinner("Logging out..."):
                api_client.logout(token)
            st.session_state.pop("token", None)
            st.session_state.pop("refresh_token", None)
            st.success("Session terminated.")
            st.rerun()

        # Render corresponding page based on active page selection
        if page == "Database Connections":
            show_connection_manager()
        else:
            # Query Assistant Home Dashboard Placeholder (implemented in later phases)
            st.write(f"### Welcome back, {display_name}!")
            st.write("You are successfully authenticated.")
            st.info("Select 'Database Connections' in the sidebar menu to connect your external servers or upload CSV/Excel files.")
            
    elif response.status_code == 401 and "refresh_token" in st.session_state:
        # Access token expired, attempt to rotate credentials using refresh token
        with st.spinner("Session expired. Attempting secure renewal..."):
            refresh_response = api_client.refresh(st.session_state["refresh_token"])
            
        if refresh_response.status_code == 200:
            res_data = refresh_response.json()
            st.session_state["token"] = res_data["access_token"]
            st.session_state["refresh_token"] = res_data["refresh_token"]
            st.rerun()
        else:
            # Session expired and cannot be renewed
            st.session_state.pop("token", None)
            st.session_state.pop("refresh_token", None)
            st.error("Session has expired. Please log in again.")
            st.rerun()
    else:
        # Any other error, clear credentials
        st.session_state.pop("token", None)
        st.session_state.pop("refresh_token", None)
        st.error("Authentication check failed. Please log in again.")
        st.rerun()
