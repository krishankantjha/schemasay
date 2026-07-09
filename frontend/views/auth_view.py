import streamlit as st
from api_client import api_client

def show_auth_page():
    """
    Displays the login and registration screen with a product pitch sidebar.
    Uses session state to switch between login and signup forms on the right side.
    """
    # Initialize session state for switching auth modes
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    # Centered Main Container Wrapper
    col_padding1, col_container, col_padding2 = st.columns([0.1, 9.8, 0.1])
    
    with col_container:
        with st.container(border=True):
            col_brand, col_form = st.columns([1, 1.2])

            # Left Column: Product Branding & Features Pitch Sidebar
            with col_brand:
                st.markdown(
                    """
                    <div style="background: linear-gradient(135deg, #0B192C 0%, #1E3E62 100%); padding: 2.5rem 1.75rem; border-radius: 8px; color: white; min-height: 520px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <!-- Brand logo -->
                            <div style="text-align: center; margin-bottom: 2rem;">
                                <div style="font-size: 2.75rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));">🛡️</div>
                                <h2 style="color: white; margin: 0; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.025em;">Welcome to <span style="color: #60A5FA;">SchemaSay</span></h2>
                                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.25rem;">Your AI-Powered SQL Analytics Platform</p>
                            </div>
                            <!-- Pitch items -->
                            <div style="margin-top: 2rem; display: flex; flex-direction: column; gap: 1.5rem;">
                                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                                    <span style="font-size: 1.5rem;">🗄️</span>
                                    <div>
                                        <strong style="color: white; font-size: 0.9rem; display: block;">Connect to Any Database</strong>
                                        <span style="color: #94A3B8; font-size: 0.75rem;">PostgreSQL, MySQL, SQL Server, SQLite & more</span>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                                    <span style="font-size: 1.5rem;">🪄</span>
                                    <div>
                                        <strong style="color: white; font-size: 0.9rem; display: block;">AI SQL Copilot</strong>
                                        <span style="color: #94A3B8; font-size: 0.75rem;">Convert plain English to SQL in seconds</span>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                                    <span style="font-size: 1.5rem;">📊</span>
                                    <div>
                                        <strong style="color: white; font-size: 0.9rem; display: block;">Visualize & Analyze</strong>
                                        <span style="color: #94A3B8; font-size: 0.75rem;">Beautiful charts and actionable insights</span>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                                    <span style="font-size: 1.5rem;">🔒</span>
                                    <div>
                                        <strong style="color: white; font-size: 0.9rem; display: block;">Secure & Private</strong>
                                        <span style="color: #94A3B8; font-size: 0.75rem;">Your data is encrypted and always secure</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Bottom badge -->
                        <div style="margin-top: auto; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;">
                            <span style="font-size: 0.75rem; color: #60A5FA; font-weight: 500;">🔒 Enterprise-grade security for your data</span>
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
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.25rem; margin-top: 1rem;">
                            <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background-color: #EFF6FF; border-radius: 50%; color: #2563EB; font-size: 1.2rem;">🔑</div>
                            <div>
                                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1E293B;">Access your SchemaSay workspace</h3>
                                <p style="margin: 0; font-size: 0.8rem; color: #64748B;">Welcome back! Please login to continue</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    email = st.text_input("Email Address", key="login_email", placeholder="Enter your email address")
                    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                    
                    st.markdown("<p style='text-align: right; margin-top: -0.5rem; font-size: 0.8rem;'><a href='#' style='color: #2563EB; text-decoration: none;'>Forgot your password?</a></p>", unsafe_allow_html=True)
                    
                    st.write("")
                    if st.button("🔑 Login", key="login_btn", use_container_width=True):
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
                    
                    # Social logins divider
                    st.markdown(
                        """
                        <div style="display: flex; align-items: center; justify-content: center; margin: 1.25rem 0 1rem 0; color: #94A3B8; font-size: 0.75rem;">
                            <div style="border-top: 1px solid #E2E8F0; flex-grow: 1;"></div>
                            <span style="padding: 0 10px;">or continue with</span>
                            <div style="border-top: 1px solid #E2E8F0; flex-grow: 1;"></div>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.6rem; width: 100%; margin-bottom: 1rem;">
                            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.5rem; cursor: pointer; background: white;">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" width="16" height="16" />
                                <span style="font-size: 0.8rem; color: #475569; font-weight: 500;">Continue with Google</span>
                            </div>
                            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.5rem; cursor: pointer; background: white;">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="16" height="16" />
                                <span style="font-size: 0.8rem; color: #475569; font-weight: 500;">Continue with GitHub</span>
                            </div>
                            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.5rem; cursor: pointer; background: white;">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" width="16" height="16" />
                                <span style="font-size: 0.8rem; color: #475569; font-weight: 500;">Continue with Microsoft</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if st.button("Don't have an account? Sign up", key="toggle_to_signup", use_container_width=True):
                        st.session_state["auth_mode"] = "signup"
                        st.rerun()

                else:
                    # Sign Up view
                    st.markdown(
                        """
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.25rem; margin-top: 1rem;">
                            <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background-color: #EFF6FF; border-radius: 50%; color: #2563EB; font-size: 1.2rem;">👤</div>
                            <div>
                                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1E293B;">Create your account to get started</h3>
                                <p style="margin: 0; font-size: 0.8rem; color: #64748B;">Enter your details to create an account</p>
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
                        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.6rem 0.8rem; border-radius: 8px; margin-bottom: 1rem;">
                            <div style="display: flex; align-items: center; gap: 8px; color: #2563EB; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.2rem;">
                                <span>🛡️</span> Password Requirements
                            </div>
                            <ul style="margin: 0; padding-left: 1.1rem; font-size: 0.7rem; color: #64748B; line-height: 1.4;">
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
                    if st.button("Already have an account? Log in", key="toggle_to_login", use_container_width=True):
                        st.session_state["auth_mode"] = "login"
                        st.rerun()
