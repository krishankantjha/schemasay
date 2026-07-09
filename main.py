import streamlit as st
import os

# Set wide layout config and page properties
st.set_page_config(
    page_title="SchemaSay Auth Gateway",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load styling rules from styles.css
if os.path.exists("styles.css"):
    with open("styles.css", "r", encoding="utf-8") as f:
        custom_css = f.read()
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Complete HTML block representing the pixel-perfect design
st.markdown(
    """
    <div class="page-wrapper">
        <div class="auth-container">
            
            <!-- LEFT BRANDING PANEL -->
            <div class="brand-panel">
                <div class="brand-header">
                    <div class="brand-logo-container">
                        <!-- Shield Database Icon -->
                        <svg viewBox="0 0 24 24" width="60" height="60" style="fill: none; stroke: #FFFFFF; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            <ellipse cx="12" cy="11" rx="5" ry="2.5" style="fill: rgba(255,255,255,0.1); stroke: #FFFFFF; stroke-width: 1.5;"/>
                            <path d="M7 14c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5" style="stroke: #FFFFFF; stroke-width: 1.5;"/>
                            <path d="M7 17c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5" style="stroke: #FFFFFF; stroke-width: 1.5;"/>
                        </svg>
                    </div>
                    <h1 class="brand-title">Welcome to <span>SchemaSay</span></h1>
                    <p class="brand-subtitle">Your AI-Powered SQL Analytics Platform</p>
                </div>
                
                <div class="features-list">
                    <!-- Feature 1 -->
                    <div class="feature-card">
                        <div class="feature-icon-wrapper">
                            <!-- Database Icon -->
                            <svg viewBox="0 0 24 24">
                                <path d="M12 2C6.48 2 2 4.02 2 6.5v11C2 20.0 6.48 22 12 22s10-2.0 10-4.5v-11C22 4.02 17.52 2 12 2zm0 3c4.1 0 7.3 1.2 7.8 2.2-.5 1-3.7 2.2-7.8 2.2S4.7 8.2 4.2 7.2C4.7 6.2 7.9 5 12 5z"/>
                            </svg>
                        </div>
                        <div class="feature-details">
                            <span class="feature-title">Connect to Any Database</span>
                            <span class="feature-desc">PostgreSQL, MySQL, SQL Server, SQLite & more</span>
                        </div>
                    </div>
                    
                    <!-- Feature 2 -->
                    <div class="feature-card">
                        <div class="feature-icon-wrapper">
                            <!-- Magic Wand Icon -->
                            <svg viewBox="0 0 24 24">
                                <path d="M7.5 5.6L10 7 8.6 4.5 10 2 7.5 3.4 5 2l1.4 2.5L5 7zm12 9.8l-2.5-1.4-1.4 2.5 1.4 2.5 2.5-1.4 2.5 1.4-1.4-2.5zM19.5 2l-2.5 1.4-1.4-2.5 1.4 2.5 2.5 1.4 2.5-1.4-1.4 2.5zM14.59 7.7l-9.8 9.8c-.39.39-.39 1.02 0 1.41l1.41 1.41c.39.39 1.02.39 1.41 0l9.8-9.8c.39-.39.39-1.02 0-1.41l-1.41-1.41c-.39-.39-1.03-.39-1.42 0z"/>
                            </svg>
                        </div>
                        <div class="feature-details">
                            <span class="feature-title">AI SQL Copilot</span>
                            <span class="feature-desc">Convert plain English to SQL in seconds</span>
                        </div>
                    </div>
                    
                    <!-- Feature 3 -->
                    <div class="feature-card">
                        <div class="feature-icon-wrapper">
                            <!-- Chart Line Icon -->
                            <svg viewBox="0 0 24 24">
                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
                            </svg>
                        </div>
                        <div class="feature-details">
                            <span class="feature-title">Visualize & Analyze</span>
                            <span class="feature-desc">Beautiful charts and actionable insights</span>
                        </div>
                    </div>
                    
                    <!-- Feature 4 -->
                    <div class="feature-card">
                        <div class="feature-icon-wrapper">
                            <!-- Shield Key Icon -->
                            <svg viewBox="0 0 24 24">
                                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-1 15.41L8.59 14l1.41-1.41 1 1 3.59-3.59 1.41 1.41L11 16.41z"/>
                            </svg>
                        </div>
                        <div class="feature-details">
                            <span class="feature-title">Secure & Private</span>
                            <span class="feature-desc">Your data is encrypted and always secure</span>
                        </div>
                    </div>
                </div>
                
                <div class="security-card">
                    <!-- Padlock Icon -->
                    <svg viewBox="0 0 24 24">
                        <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                    </svg>
                    <span class="security-text">Enterprise-grade security for your data</span>
                </div>
            </div>
            
            <!-- RIGHT FORM PANEL -->
            <div class="auth-panel">
                <div class="panel-header">
                    <div class="key-icon-wrapper">
                        <!-- Key Icon -->
                        <svg viewBox="0 0 24 24">
                            <path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
                        </svg>
                    </div>
                    <div>
                        <h2 class="panel-title">Access your SchemaSay workspace</h2>
                        <p class="panel-subtitle">Welcome back! Please login to continue</p>
                    </div>
                </div>
                
                <!-- Email Input Form Group -->
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <div class="input-wrapper">
                        <!-- Mail Icon -->
                        <svg class="input-icon" viewBox="0 0 24 24">
                            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                        </svg>
                        <input class="input-control" type="email" placeholder="Enter your email address" required />
                    </div>
                </div>
                
                <!-- Password Input Form Group -->
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <div class="input-wrapper">
                        <!-- Padlock Icon -->
                        <svg class="input-icon" viewBox="0 0 24 24">
                            <path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6-5c1.66 0 3 1.34 3 3v2H9V6c0-1.66 1.34-3 3-3z"/>
                        </svg>
                        <input class="input-control" type="password" placeholder="Enter your password" required />
                        <!-- Eye Visibility Icon -->
                        <svg class="toggle-password" viewBox="0 0 24 24">
                            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                        </svg>
                    </div>
                    <a class="forgot-password-link" href="#">Forgot your password?</a>
                </div>
                
                <!-- Login Button -->
                <button class="btn-login">
                    <!-- Key Icon -->
                    <svg viewBox="0 0 24 24">
                        <path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
                    </svg>
                    Login
                </button>
                
                <!-- Divider -->
                <div class="divider-container">
                    <div class="divider-line"></div>
                    <span class="divider-text">or continue with</span>
                    <div class="divider-line"></div>
                </div>
                
                <!-- Social Logins -->
                <div class="social-container">
                    <button class="social-button">
                        <img class="social-icon" src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" />
                        <span class="social-text">Continue with Google</span>
                    </button>
                    <button class="social-button">
                        <img class="social-icon" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" />
                        <span class="social-text">Continue with GitHub</span>
                    </button>
                    <button class="social-button">
                        <img class="social-icon" src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" />
                        <span class="social-text">Continue with Microsoft</span>
                    </button>
                </div>
                
                <!-- Account Toggle Link -->
                <div class="toggle-auth-wrapper">
                    <span class="toggle-auth-text">Don't have an account?</span>
                    <a class="toggle-auth-link" href="#">Sign up</a>
                </div>
            </div>
            
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
