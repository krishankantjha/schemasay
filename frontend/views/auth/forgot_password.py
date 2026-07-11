import streamlit as st

def show_forgot_password_view():
    """
    Renders the forgot password email request view.
    """
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <div style="width: 46px; height: 46px; background-color: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg viewBox="0 0 24 24" width="20" height="20" style="fill: #4169E1;">
                    <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Forgot password?</h3>
                <p style="margin: 0; font-size: 13px; color: #6B7280;">Enter your email to receive recovery instructions</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    forgot_email = st.text_input("Email Address", key="forgot_email", placeholder="Enter your registered email address")
    
    if st.button("Send Reset Link", key="forgot_btn", type="primary", use_container_width=True):
        if not forgot_email:
            st.error("Please enter your email address")
        else:
            st.success("If that email address exists, we have sent instructions to reset your password.")
            st.session_state["auth_mode"] = "email_verification"
            st.rerun()
            
    st.write("")
    if st.button("Back to Log in", key="back_to_login_forgot", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.rerun()
