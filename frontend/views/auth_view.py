import streamlit as st
from api_client import api_client

def show_auth_page():
    """
    Renders the login and registration forms using Streamlit tabs.
    Coordinates authentication requests with the API client.
    Handles non-JSON error responses from the backend safely.
    Uses spinner loaders to prevent duplicate actions.
    """
    st.subheader("Account Authentication")

    # Setup separate tabs for login and account creation
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    # Login Flow
    with tab_login:
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if not email or not password:
                st.error("Please fill in all fields")
                return
            
            # Use spinner loading indicator to block inputs
            with st.spinner("Authenticating credentials..."):
                response = api_client.login(email, password)
                
            if response.status_code == 200:
                try:
                    res_data = response.json()
                    # Store access and refresh tokens in session state
                    st.session_state["token"] = res_data["access_token"]
                    st.session_state["refresh_token"] = res_data["refresh_token"]
                    st.success("Authentication successful")
                    st.rerun()
                except ValueError:
                    st.error("Server responded with invalid token data format")
            else:
                try:
                    detail = response.json().get("detail", "Authentication failed")
                except ValueError:
                    detail = f"Server Error ({response.status_code}): {response.text[:200]}"
                st.error(detail)

    # Registration Flow
    with tab_signup:
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        
        # Helper collapse block explaining complexity requirements
        with st.expander("Password Requirements", expanded=False):
            st.caption("- Minimum 8 characters in length")
            st.caption("- At least one uppercase character (A-Z)")
            st.caption("- At least one lowercase character (a-z)")
            st.caption("- At least one numerical digit (0-9)")
            st.caption("- At least one special symbol (!@#$%^&*, etc.)")

        if st.button("Create Account", key="reg_btn"):
            if not reg_email or not reg_password:
                st.error("Email and password are required fields")
                return
                
            with st.spinner("Registering platform profile..."):
                response = api_client.register(reg_email, reg_password, reg_name)
                
            if response.status_code == 201:
                st.success("Account created successfully. Please switch to the Login tab.")
            else:
                try:
                    detail = response.json().get("detail", "Registration failed")
                except ValueError:
                    detail = f"Server Error ({response.status_code}): {response.text[:200]}"
                st.error(detail)
