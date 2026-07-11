import streamlit as st

def show_reset_password_view():
    """
    Renders the password update/reset view.
    """
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <div style="width: 46px; height: 46px; background-color: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg viewBox="0 0 24 24" width="20" height="20" style="fill: #4169E1;">
                    <path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6-5c1.66 0 3 1.34 3 3v2H9V6c0-1.66 1.34-3 3-3z"/>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Reset Password</h3>
                <p style="margin: 0; font-size: 13px; color: #6B7280;">Set a strong password for your workspace account</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    new_pwd = st.text_input("New Password", type="password", key="reset_new_pwd", placeholder="Enter new password")
    confirm_pwd = st.text_input("Confirm New Password", type="password", key="reset_confirm_pwd", placeholder="Confirm new password")
    
    if st.button("Update Password", key="reset_pwd_btn", type="primary", use_container_width=True):
        if not new_pwd or new_pwd != confirm_pwd:
            st.error("Passwords must match and cannot be empty")
        else:
            st.success("Password reset complete. You can now login.")
            st.session_state["auth_mode"] = "login"
            st.rerun()
