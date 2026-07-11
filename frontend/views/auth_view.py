import streamlit as st

def show_auth_page():
    """
    Displays the login and registration screen with a product pitch sidebar.
    Uses session state to delegate form rendering to subviews inside views/auth/.
    """
    # Initialize session state for switching auth modes
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    # Centered Main Container Wrapper
    col_padding1, col_container, col_padding2 = st.columns([0.1, 9.8, 0.1])
    
    with col_container:
        with st.container(border=True, key="auth_container_card"):
            col_brand, col_form = st.columns([1, 1.2])

            # Left Column: Product Branding & Features Pitch Sidebar
            with col_brand:
                with st.container(key="brand_panel_container"):
                    st.markdown(
                        """
                        <div style="display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 520px;">
                            <div>
                                <!-- Brand logo -->
                                <div style="text-align: center; margin-bottom: 25px;">
                                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                        <svg viewBox="0 0 24 24" width="60" height="60" style="fill: none; stroke: #FFFFFF; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;">
                                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                            <ellipse cx="12" cy="11" rx="5" ry="2.5" style="fill: rgba(255,255,255,0.1); stroke: #FFFFFF; stroke-width: 1.5;"/>
                                            <path d="M7 14c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5" style="stroke: #FFFFFF; stroke-width: 1.5;"/>
                                            <path d="M7 17c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5" style="stroke: #FFFFFF; stroke-width: 1.5;"/>
                                        </svg>
                                    </div>
                                    <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.025em; font-family: 'Inter', sans-serif;">Welcome to <span style="color: #60A5FA;">SchemaSay</span></h2>
                                    <p style="color: #94A3B8; font-size: 12px; margin-top: 5px; font-weight: 500;">Your AI-Powered SQL Analytics Platform</p>
                                </div>
                                <!-- Pitch items -->
                                <div style="margin-top: 20px; display: flex; flex-direction: column; gap: 15px;">
                                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 12px 16px; display: flex; gap: 14px; align-items: center;">
                                        <div style="width: 38px; height: 38px; background-color: rgba(65, 105, 225, 0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                            <svg viewBox="0 0 24 24" width="20" height="20" style="fill: white;">
                                                <path d="M12 2C6.48 2 2 4.02 2 6.5v11C2 20.0 6.48 22 12 22s10-2.0 10-4.5v-11C22 4.02 17.52 2 12 2zm0 3c4.1 0 7.3 1.2 7.8 2.2-.5 1-3.7 2.2-7.8 2.2S4.7 8.2 4.2 7.2C4.7 6.2 7.9 5 12 5z"/>
                                            </svg>
                                        </div>
                                        <div>
                                            <strong style="color: white; font-size: 13px; display: block; font-weight: 600;">Connect to Any Database</strong>
                                            <span style="color: #94A3B8; font-size: 11px;">PostgreSQL, MySQL, SQL Server, SQLite & more</span>
                                        </div>
                                    </div>
                                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 12px 16px; display: flex; gap: 14px; align-items: center;">
                                        <div style="width: 38px; height: 38px; background-color: rgba(65, 105, 225, 0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                            <svg viewBox="0 0 24 24" width="20" height="20" style="fill: white;">
                                                <path d="M7.5 5.6L10 7 8.6 4.5 10 2 7.5 3.4 5 2l1.4 2.5L5 7zm12 9.8l-2.5-1.4-1.4 2.5 1.4 2.5 2.5-1.4 2.5 1.4-1.4-2.5zM19.5 2l-2.5 1.4-1.4-2.5 1.4 2.5 2.5 1.4 2.5-1.4-1.4 2.5zM14.59 7.7l-9.8 9.8c-.39.39-.39 1.02 0 1.41l1.41 1.41c.39.39 1.02.39 1.41 0l9.8-9.8c.39-.39.39-1.02 0-1.41l-1.41-1.41c-.39-.39-1.03-.39-1.42 0z"/>
                                            </svg>
                                        </div>
                                        <div>
                                            <strong style="color: white; font-size: 13px; display: block; font-weight: 600;">AI SQL Copilot</strong>
                                            <span style="color: #94A3B8; font-size: 11px;">Convert plain English to SQL in seconds</span>
                                        </div>
                                    </div>
                                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 12px 16px; display: flex; gap: 14px; align-items: center;">
                                        <div style="width: 38px; height: 38px; background-color: rgba(65, 105, 225, 0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                            <svg viewBox="0 0 24 24" width="20" height="20" style="fill: white;">
                                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
                                            </svg>
                                        </div>
                                        <div>
                                            <strong style="color: white; font-size: 13px; display: block; font-weight: 600;">Visualize & Analyze</strong>
                                            <span style="color: #94A3B8; font-size: 11px;">Beautiful charts and actionable insights</span>
                                        </div>
                                    </div>
                                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 12px 16px; display: flex; gap: 14px; align-items: center;">
                                        <div style="width: 38px; height: 38px; background-color: rgba(65, 105, 225, 0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                            <svg viewBox="0 0 24 24" width="20" height="20" style="fill: white;">
                                                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-1 15.41L8.59 14l1.41-1.41 1 1 3.59-3.59 1.41 1.41L11 16.41z"/>
                                            </svg>
                                        </div>
                                        <div>
                                            <strong style="color: white; font-size: 13px; display: block; font-weight: 600;">Secure & Private</strong>
                                            <span style="color: #94A3B8; font-size: 11px;">Your data is encrypted and always secure</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bottom badge -->
                            <div style="background: rgba(5, 15, 44, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 12px; display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                                <svg viewBox="0 0 24 24" width="16" height="16" style="fill: #60A5FA;">
                                    <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                                </svg>
                                <span style="font-size: 11px; font-weight: 500; color: #60A5FA;">Enterprise-grade security for your data</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Right Column: Authentication Form Panel Subview Router
            with col_form:
                with st.container(key="form_panel_container"):
                    auth_mode = st.session_state.get("auth_mode", "login")
                    
                    if auth_mode == "login":
                        from views.auth.login import show_login_view
                        show_login_view()
                    elif auth_mode == "signup":
                        from views.auth.signup import show_signup_view
                        show_signup_view()
                    elif auth_mode == "forgot_password":
                        from views.auth.forgot_password import show_forgot_password_view
                        show_forgot_password_view()
                    elif auth_mode == "reset_password":
                        from views.auth.reset_password import show_reset_password_view
                        show_reset_password_view()
                    elif auth_mode == "otp_verification":
                        from views.auth.otp_verification import show_otp_verification_view
                        show_otp_verification_view()
                    elif auth_mode == "email_verification":
                        from views.auth.email_verification import show_email_verification_view
                        show_email_verification_view()
