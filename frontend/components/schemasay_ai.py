"""
SchemaSay Components — SchemaSay AI Panel

Fully functional AI natural language query translator.
Connects directly to the versioned FastAPI backend.
"""

import html
import streamlit as st
from api_client import api_client
from state import KEY_TOKEN, KEY_ACTIVE_CONNECTION_ID
from utils.caching import get_cached_connections
from utils.sanitize import escape_html

# Suggestion query prompts matching seeded demo dataset
SUGGESTIONS = {
    "Sales Trend": "Show total sales per month for the last year",
    "Top Customers": "Show top 10 customers by total sales",
    "Low Stock": "Show products with low stock less than 20",
    "Profit Trends": "Show monthly profit trends"
}

def render_ai_copilot_panel():
    """
    Renders the functional SchemaSay AI container inside the first card:
      - Header status badges
      - Prompt input area with suggestion chips
      - Generate/Clear action triggers
      - Backend POST translation query client integration
      - Dark code block preview with direct Copy-to-Clipboard execution
    """
    token = st.session_state.get(KEY_TOKEN)
    
    # State initializations
    if "prompt_input" not in st.session_state:
        st.session_state.prompt_input = ""
    if "generated_sql" not in st.session_state:
        st.session_state.generated_sql = ""

    # Synchronize session state prompt value with query param clicks
    if "prompt" in st.query_params:
        clicked_prompt = st.query_params["prompt"]
        if clicked_prompt != st.session_state.prompt_input:
            st.session_state.prompt_input = clicked_prompt
            st.query_params.pop("prompt", None)

    # 1. Header & Description Layout HTML
    sparkle_icon = (
        '<svg class="copilot-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>'
        '</svg>'
    )
    
    settings_icon = (
        '<svg class="copilot-settings-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="3"></circle>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
        '</svg>'
    )

    header_html = f"""
    <div class="copilot-header">
        <div class="copilot-title-group">
            {sparkle_icon}
            <span class="copilot-title-text">SchemaSay AI</span>
            <span class="copilot-status-badge">
                <span class="copilot-pulse-dot"></span>
                Ready
            </span>
        </div>
        {settings_icon}
    </div>
    <div class="copilot-desc">Ask anything about your database query tables in standard natural English.</div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. Text Input Area wrapped in CSS wrapper class
    st.markdown('<div class="copilot-prompt-wrapper">', unsafe_allow_html=True)
    prompt_text = st.text_area(
        label="Ask anything about your data",
        value=st.session_state.prompt_input,
        placeholder="e.g., Show monthly revenue statistics...",
        key="prompt_input_field"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Suggestion Chips HTML links
    chips_html = '<div class="suggestion-chips-container">'
    for label, val in SUGGESTIONS.items():
        escaped_val = html.escape(val)
        chips_html += f'<a class="suggestion-chip" href="?prompt={escaped_val}" target="_self">{label}</a>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)

    # 4. Action buttons columns
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        generate_clicked = st.button("Generate SQL", type="primary", use_container_width=True)
    with col_btn2:
        clear_clicked = st.button("Clear", use_container_width=True)

    # Handle clear trigger
    if clear_clicked:
        st.session_state.prompt_input = ""
        st.session_state.generated_sql = ""
        st.query_params.pop("prompt", None)
        st.rerun()

    # Handle backend generate SQL call
    if generate_clicked and prompt_text:
        # Check active connection fallback
        active_conn_id = st.session_state.get(KEY_ACTIVE_CONNECTION_ID)
        if not active_conn_id:
            conns = get_cached_connections(token)
            if conns:
                active_conn_id = conns[0]["id"]
                st.session_state[KEY_ACTIVE_CONNECTION_ID] = active_conn_id
        
        if not active_conn_id:
            st.error("Please configure and select a database connection source first.")
        else:
            with st.spinner("Translating prompt into SQL query..."):
                response = api_client.query_assistant(token, active_conn_id, prompt_text)
                
            if response.status_code == 200:
                res_data = response.json()
                st.session_state.generated_sql = res_data.get("sql_query") or ""
            else:
                try:
                    detail = response.json().get("detail", "Error translating query.")
                except Exception:
                    detail = "Backend connection error."
                st.error(detail)

    # 5. Generated SQL Code block preview
    sql_val = st.session_state.generated_sql or "-- Generated SQL statements will render here..."
    safe_sql = escape_html(sql_val)
    escaped_for_js = sql_val.replace("'", "\\'").replace("\n", "\\n")
    
    preview_html = f"""
    <div class="sql-preview-container">
        <div class="sql-preview-header">
            <span class="sql-preview-label">Generated SQL Statement</span>
            <a class="sql-preview-copy-btn" onclick="navigator.clipboard.writeText('{escaped_for_js}')" href="javascript:void(0);">Copy Code</a>
        </div>
        <pre class="sql-preview-code">{safe_sql}</pre>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
