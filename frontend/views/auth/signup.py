import streamlit as st
from api_client import api_client

def show_signup_view():
    """
    Renders the sign-up inputs and details forms, handling new workspace registration.
    """
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <div style="width: 46px; height: 46px; background-color: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg viewBox="0 0 24 24" width="20" height="20" style="fill: #4169E1;">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Create your account to get started</h3>
                <p style="margin: 0; font-size: 13px; color: #6B7280;">Enter your details to create an account</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    reg_email = st.text_input("Email Address", key="reg_email", placeholder="Enter your email address")
    reg_name = st.text_input("Full Name", key="reg_name", placeholder="Enter your full name")
    reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a strong password")
    
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 14px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 8px; color: #4169E1; font-weight: 600; font-size: 13px; margin-bottom: 5px;">
                <span>🛡️</span> Password Requirements
            </div>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 11px; color: #6B7280; line-height: 1.5;">
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

    if st.button("Create Account", key="reg_btn", type="primary", use_container_width=True):
        if not reg_email or not reg_password:
            st.error("Email and password are required fields")
        else:
            with st.spinner("Registering platform profile..."):
                try:
                    response = api_client.register(reg_email, reg_password, reg_name)
                    if response.status_code == 201:
                        st.session_state["auth_mode"] = "otp_verification"
                        st.rerun()
                    else:
                        try:
                            detail = response.json().get("detail", "Registration failed")
                        except ValueError:
                            detail = f"Server Error ({response.status_code}): {response.text[:200]}"
                        st.error(detail)
                except Exception as e:
                    st.error(f"Failed to connect to authentication server: {str(e)}")
    
    st.write("")
    with st.container(key="signin_row_container"):
        col_lbl, col_btn = st.columns([2.1, 1])
        with col_lbl:
            st.markdown("<p style='text-align: right; margin: 0; font-size: 13px; color: #6B7280; font-weight: 500; line-height: 32px;'>Already have an account?</p>", unsafe_allow_html=True)
        with col_btn:
            if st.button("Log in", key="toggle_to_login", type="secondary"):
                st.session_state["auth_mode"] = "login"
                st.rerun()
