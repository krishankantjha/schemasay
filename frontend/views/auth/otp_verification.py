import streamlit as st

def show_otp_verification_view():
    """
    Renders 6-digit OTP code confirmation fields view.
    """
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <div style="width: 46px; height: 46px; background-color: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg viewBox="0 0 24 24" width="20" height="20" style="fill: #4169E1;">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827; font-family: 'Inter', sans-serif;">Verify OTP Code</h3>
                <p style="margin: 0; font-size: 13px; color: #6B7280;">Enter the 6-digit confirmation code we sent to your email.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # OTP 6 Digit Grid Columns
    col_otp = st.columns(6)
    otp_val = []
    for i in range(6):
        with col_otp[i]:
            digit = st.text_input("", key=f"otp_{i}", placeholder="-", max_chars=1, label_visibility="collapsed")
            otp_val.append(digit)
    
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; margin-top: 10px; margin-bottom: 20px;">
            <span style="font-size: 11px; color: #6B7280;">Code expires in <strong style="color: #4169E1;">01:58</strong></span>
            <a href="#" style="font-size: 11px; color: #4169E1; font-weight: 600; text-decoration: none;">Resend Code</a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Verify & Activate", key="otp_verify_btn", type="primary", use_container_width=True):
        st.success("Verification successful! Profile activated.")
        st.session_state["auth_mode"] = "login"
        st.rerun()
