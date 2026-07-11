"""
SchemaSay Views — Settings View

Renders account details, analytical thresholds, and platform config values.
"""

import streamlit as st

def show_settings_view():
    """Renders the settings manager views panel."""
    with st.container(border=True):
        st.write("### Workspace Settings")
        st.write("Configure default analytics parameters, security thresholds, and workspace profiles.")
        st.markdown("---")

        # Tab sections
        tab_profile, tab_security, tab_limits = st.tabs(["Account Profile", "API Keys & Access Tokens", "Platform Execution Limits"])

        with tab_profile:
            st.write("#### Profile Settings")
            st.text_input("Display Name", value="John Doe")
            st.text_input("Corporate Email Address", value="john.doe@example.com", disabled=True)
            st.selectbox("Default Dialect Dialect", options=["PostgreSQL", "MySQL", "SQLite", "MSSQL"])
            st.button("Save Profile Settings", key="save_profile_settings_btn")

        with tab_security:
            st.write("#### API Credentials")
            st.text_input("OpenAI API Key Token", type="password", value="sk-proj-....................")
            st.text_input("FastAPI JWT Token Timeout", value="86400 (24 hours)")
            st.button("Rotate Workspace Encryption Credentials", key="rotate_credentials_btn")

        with tab_limits:
            st.write("#### Analytics Guardrails")
            st.number_value = st.number_input("Maximum DataFrame Sample Size", min_value=100, max_value=50000, value=5000)
            st.number_input("API Rate Limit Gate (reqs/min)", min_value=5, max_value=120, value=30)
            st.number_input("Sandboxed Engine Timeout (seconds)", min_value=5, max_value=180, value=30)
            st.button("Save Analytics Constraints", key="save_limits_btn")
