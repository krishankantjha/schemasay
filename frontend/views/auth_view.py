import streamlit as st
from api_client import api_client

def show_auth_page():
    """
    Displays the login and registration forms in a side-by-side workspace split.
    Coordinates authentication and registration requests with the API client.
    """
    # Centered Logo and Main Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 60px; height: 60px; background-color: #EFF6FF; border-radius: 16px; margin-bottom: 1rem; border: 1px solid #DBEAFE;">
                <span style="font-size: 2rem; color: #2563EB;">🛡️</span>
            </div>
            <h1 style="margin: 0; font-size: 2.25rem; font-weight: 700;">Welcome to <span style="color: #2563EB;">SchemaSay</span></h1>
            <p style="margin: 0.25rem 0 0 0; color: #64748B; font-size: 1rem;">Your AI-Powered SQL Analytics Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([0.1, 9.8, 0.1])
    with col2:
        with st.container(border=True):
            col_login, col_div, col_signup = st.columns([1, 0.05, 1])

            # Left Column: Login Flow
            with col_login:
                st.markdown(
                    """
                    <div style="background-color: #EFF6FF; border: 1px solid #DBEAFE; padding: 0.75rem 1rem; border-radius: 8px; color: #1E40AF; display: flex; align-items: center; gap: 8px; margin-bottom: 1.25rem;">
                        <span style="font-size: 1.1rem;">🔑</span>
                        <span style="font-size: 0.875rem; font-weight: 500;">Access your SchemaSay workspace</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                email = st.text_input("Email Address", key="login_email", placeholder="Enter your email address")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                
                # Forgot password placeholder aligned right
                st.markdown("<p style='text-align: right; margin-top: -0.5rem; font-size: 0.8rem;'><a href='#' style='color: #2563EB; text-decoration: none;'>Forgot your password?</a></p>", unsafe_allow_html=True)
                
                st.write("")
                if st.button("🔑 Login", key="login_btn", use_container_width=True):
                    if not email or not password:
                        st.error("Please fill in all fields")
                        return
                    
                    with st.spinner("Authenticating credentials..."):
                        response = api_client.login(email, password)
                        
                    if response.status_code == 200:
                        try:
                            res_data = response.json()
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

            # Middle Column: Vertical Divider Line
            with col_div:
                st.markdown(
                    """
                    <div style="border-left: 1px solid #E2E8F0; height: 420px; margin: 0 auto; width: 1px;"></div>
                    """,
                    unsafe_allow_html=True
                )

            # Right Column: Registration Flow
            with col_signup:
                st.markdown(
                    """
                    <div style="background-color: #EFF6FF; border: 1px solid #DBEAFE; padding: 0.75rem 1rem; border-radius: 8px; color: #1E40AF; display: flex; align-items: center; gap: 8px; margin-bottom: 1.25rem;">
                        <span style="font-size: 1.1rem;">👤</span>
                        <span style="font-size: 0.875rem; font-weight: 500;">Create your account to get started</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                reg_email = st.text_input("Email Address", key="reg_email", placeholder="Enter your email address")
                reg_name = st.text_input("Full Name", key="reg_name", placeholder="Enter your full name")
                reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a strong password")
                
                st.markdown(
                    """
                    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1.25rem;">
                        <div style="display: flex; align-items: center; gap: 8px; color: #2563EB; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.25rem;">
                            <span>🛡️</span> Password Requirements
                        </div>
                        <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.75rem; color: #64748B; line-height: 1.5;">
                            <li>Minimum 8 characters in length</li>
                            <li>At least one uppercase character (A-Z)</li>
                            <li>At least one lowercase character (a-z)</li>
                            <li>At least one numerical digit (0-9)</li>
                            <li>At least one special symbol (!@#$%^&*, etc.)</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button("👤 Create Account", key="reg_btn", use_container_width=True):
                    if not reg_email or not reg_password:
                        st.error("Email and password are required fields")
                        return
                        
                    with st.spinner("Registering platform profile..."):
                        response = api_client.register(reg_email, reg_password, reg_name)
                        
                    if response.status_code == 201:
                        st.success("Account created successfully. You can now log in.")
                    else:
                        try:
                            detail = response.json().get("detail", "Registration failed")
                        except ValueError:
                            detail = f"Server Error ({response.status_code}): {response.text[:200]}"
                        st.error(detail)
