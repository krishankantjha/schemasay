import streamlit as st
from api_client import api_client

def show_login_view():
    """
    Renders the sign-in input form and triggers backend authentication.
    """
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <div style="width: 46px; height: 46px; background-color: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg viewBox="0 0 24 24" width="20" height="20" style="fill: #4169E1;">
                    <path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Access your SchemaSay workspace</h3>
                <p style="margin: 0; font-size: 13px; color: #6B7280;">Welcome back! Please login to continue</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    email = st.text_input("Email Address", key="login_email", placeholder="Enter your email address")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    col_forgot, _ = st.columns([1.2, 1])
    with col_forgot:
        if st.button("Forgot your password?", key="nav_to_forgot_pwd"):
            st.session_state["auth_mode"] = "forgot_password"
            st.rerun()
    
    st.write("")
    if st.button("Login", key="login_btn", type="primary", use_container_width=True):
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Authenticating credentials..."):
                try:
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
                except Exception as e:
                    st.error(f"Failed to connect to authentication server: {str(e)}")
    
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin: 20px 0;">
            <div style="height: 1px; background-color: #E2E8F0; flex-grow: 1;"></div>
            <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Or continue with</span>
            <div style="height: 1px; background-color: #E2E8F0; flex-grow: 1;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_sso1, col_sso2, col_sso3 = st.columns(3)
    with col_sso1:
        st.button("Google", key="sso_google", use_container_width=True)
    with col_sso2:
        st.button("GitHub", key="sso_github", use_container_width=True)
    with col_sso3:
        st.button("Microsoft", key="sso_microsoft", use_container_width=True)

    st.write("")
    with st.container(key="signup_row_container"):
        col_lbl, col_btn = st.columns([1.8, 1])
        with col_lbl:
            st.markdown("<p style='text-align: right; margin: 0; font-size: 13px; color: #6B7280; font-weight: 500; line-height: 32px;'>Don't have an account?</p>", unsafe_allow_html=True)
        with col_btn:
            if st.button("Sign up", key="toggle_to_signup", type="secondary"):
                st.session_state["auth_mode"] = "signup"
                st.rerun()
