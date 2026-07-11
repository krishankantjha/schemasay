import streamlit as st

def show_email_verification_view():
    """
    Renders email client verification link instructions view.
    """
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px; margin-bottom: 25px;">
            <div style="font-size: 48px; margin-bottom: 15px;">✉️</div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Check your email inbox</h3>
            <p style="margin: 8px 0 0 0; font-size: 13px; color: #6B7280; line-height: 1.5;">
                We have sent a secure recovery link to your email address.<br/>
                Please click on the link to reset your account credentials.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.button("Open Email Client", key="open_email_client_btn", type="primary", use_container_width=True)
    
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <span style="font-size: 12px; color: #6B7280;">Didn't receive instructions? <a href="#" style="color: #4169E1; font-weight: 600; text-decoration: none;">Resend Link</a></span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    if st.button("Back to Log in", key="back_to_login_email", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.rerun()
