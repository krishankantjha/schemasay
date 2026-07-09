import streamlit as st
from api_client import api_client

def show_auth_page():
    """
    Displays the login and registration screen with a product pitch sidebar.
    Uses session state to switch between login and signup forms on the right side.
    """
    # Force mockup visual styling (override Streamlit dark/light theme variables)
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Set page background gradient */
        div[data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #081C5A 0%, #0B2C82 50%, #123FA6 100%) !important;
            height: 100vh !important;
            width: 100% !important;
            overflow: hidden !important;
        }

        /* Collapse Streamlit default top/bottom padding to center card vertically */
        div[data-testid="block-container"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            height: 100vh !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Hide standard header, footer, and menu */
        #MainMenu, footer, header, [data-testid="stHeader"] {
            display: none !important;
        }

        .stApp {
            background: transparent !important;
        }

        /* Style the main auth container card using stable key class */
        .st-key-auth_container_card {
            background-color: #FFFFFF !important;
            border: 1px solid #E7EDF8 !important;
            border-radius: 30px !important;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2) !important;
            padding: 0 !important;
            overflow: hidden !important;
            max-width: 1040px !important;
            margin: 0 auto !important;
        }

        /* Make columns layout flush */
        div[data-testid="column"] {
            padding: 0 !important;
        }

        /* Left Column: branding sidebar panel */
        .st-key-auth_container_card div[data-testid="column"]:first-child {
            background: linear-gradient(135deg, #061543 0%, #0B2C82 100%) !important;
            color: #FFFFFF !important;
            border-radius: 30px 0 0 30px !important;
            overflow: hidden !important;
        }

        /* Right Column: authentication form panel */
        .st-key-auth_container_card div[data-testid="column"]:last-child {
            padding: 45px 50px !important;
            background-color: #FFFFFF !important;
            border-radius: 0 30px 30px 0 !important;
        }

        /* Force dark text for visibility in the white right column panel */
        .st-key-auth_container_card div[data-testid="column"]:last-child h3,
        .st-key-auth_container_card div[data-testid="column"]:last-child p,
        .st-key-auth_container_card div[data-testid="column"]:last-child span {
            color: #111827 !important;
        }

        /* Text Input controls overrides */
        div[data-testid="stTextInput"] label {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: #111827 !important;
            margin-bottom: 8px !important;
        }
        div[data-testid="stTextInput"] input {
            height: 52px !important;
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1.5px solid #D9E3F5 !important;
            border-radius: 12px !important;
            font-size: 14px !important;
            outline: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4169E1 !important;
            box-shadow: 0 0 0 3px rgba(65, 105, 225, 0.15) !important;
        }
        
        /* Inject background envelope icon in Email inputs */
        div[data-testid="stTextInput"]:has(input[placeholder*="email"]) input {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%236B7280"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 16px center !important;
            background-size: 20px 20px !important;
            padding-left: 48px !important;
        }
        
        /* Inject background user profile icon in Full Name inputs */
        div[data-testid="stTextInput"]:has(input[placeholder*="name"]) input {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%236B7280"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 16px center !important;
            background-size: 20px 20px !important;
            padding-left: 48px !important;
        }

        /* Inject background lock icon in Password inputs */
        div[data-testid="stTextInput"]:has(input[type="password"]) input {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%236B7280"><path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6-5c1.66 0 3 1.34 3 3v2H9V6c0-1.66 1.34-3 3-3z"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 16px center !important;
            background-size: 20px 20px !important;
            padding-left: 48px !important;
        }

        /* Style the Login / Submit button */
        div[data-testid="stButton"] button[kind="primary"] {
            height: 54px !important;
            background-color: #4169E1 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 6px rgba(65, 105, 225, 0.2) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #2F5DD7 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 12px rgba(65, 105, 225, 0.3) !important;
        }

        /* Style the Toggle Auth state buttons to look like clean blue text links */
        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: transparent !important;
            border: none !important;
            color: #4169E1 !important;
            box-shadow: none !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            margin: 0 auto !important;
            display: block !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            color: #2F5DD7 !important;
            text-decoration: underline !important;
            background-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
                st.markdown(
                    """
                    <div style="padding: 40px 30px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 520px;">
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

            # Right Column: Login or Sign Up Toggle Forms
            with col_form:
                if st.session_state["auth_mode"] == "login":
                    # Title of action
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
                    
                    st.markdown("<p style='text-align: right; margin-top: -0.5rem;'><a href='#' style='font-size: 12px; font-weight: 600; color: #4169E1; text-decoration: none;'>Forgot your password?</a></p>", unsafe_allow_html=True)
                    
                    st.write("")
                    if st.button("Login", key="login_btn", type="primary", use_container_width=True):
                        if not email or not password:
                            st.error("Please fill in all fields")
                        else:
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
                    
                    st.write("")
                    if st.button("Don't have an account? Sign up", key="toggle_to_signup", type="secondary", use_container_width=True):
                        st.session_state["auth_mode"] = "signup"
                        st.rerun()

                else:
                    # Sign Up view
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
                                response = api_client.register(reg_email, reg_password, reg_name)
                                
                            if response.status_code == 201:
                                st.success("Account created successfully. You can now log in.")
                                st.session_state["auth_mode"] = "login"
                                st.rerun()
                            else:
                                try:
                                    detail = response.json().get("detail", "Registration failed")
                                except ValueError:
                                    detail = f"Server Error ({response.status_code}): {response.text[:200]}"
                                st.error(detail)
                    
                    st.write("")
                    if st.button("Already have an account? Log in", key="toggle_to_login", type="secondary", use_container_width=True):
                        st.session_state["auth_mode"] = "login"
                        st.rerun()
