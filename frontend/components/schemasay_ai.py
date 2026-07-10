"""
SchemaSay Components — SchemaSay AI Panel

Fully interactive and production-ready natural language SQL generator.
Decoupled and driven purely via centralized state manager and simulated AI generation service.
"""

import html
import streamlit as st
from services.mock_ai import generate_sql
from utils.validation import validate_prompt
from utils.helpers import clear_prompt

# Suggestion query prompts
SUGGESTIONS = {
    "Sales Trend": "Show total sales per month for the last year",
    "Top Customers": "Show top 10 customers by total sales",
    "Low Stock": "Show products with low stock less than 20",
    "Profit Trends": "Show monthly profit trends"
}

def render_ai_copilot_panel():
    """
    Renders the SchemaSay AI panel inside the card slot.
    Coordinates inputs, suggestion chips, loading animation states,
    validation parameters, mock SQL generators, and copy utilities.
    """
    # ── 1. Synchronize URL suggestions clicks to prompt state ────────────────
    if "prompt" in st.query_params:
        st.session_state.prompt_text = st.query_params["prompt"]
        st.query_params.pop("prompt", None)
        st.rerun()

    # Determine interactive state properties
    is_loading = st.session_state.get("sql_generation_status") == "loading"
    prompt_val = st.session_state.get("prompt_text", "")
    char_count = len(prompt_val)
    max_char = 200

    # ── 2. Header and description HTML ────────────────────────────────────────
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

    status_badge_label = "Running" if is_loading else "Ready"
    
    header_html = f"""
    <div class="copilot-header">
        <div class="copilot-title-group">
            {sparkle_icon}
            <span class="copilot-title-text">SchemaSay AI</span>
            <span class="copilot-status-badge" style="background-color: {'rgba(59, 130, 246, 0.08)' if is_loading else 'rgba(16, 185, 129, 0.08)'}; color: {'var(--color-primary)' if is_loading else 'var(--color-success)'};">
                <span class="copilot-pulse-dot" style="background-color: {'var(--color-primary)' if is_loading else 'var(--color-success)'};"></span>
                {status_badge_label}
            </span>
        </div>
        <div style="display:flex; align-items:center; gap: 8px;">
            <span style="font-size: 9px; color: var(--color-text-secondary); font-weight: 500;">{char_count}/{max_char}</span>
            {settings_icon}
        </div>
    </div>
    <div class="copilot-desc">Ask anything about your database query tables in standard natural English.</div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # ── 3. Prompt textarea container ──────────────────────────────────────────
    st.markdown('<div class="copilot-prompt-wrapper">', unsafe_allow_html=True)
    
    # Input is bound to st.session_state.prompt_text
    prompt_text = st.text_area(
        label="Ask anything about your data",
        value=prompt_val,
        placeholder="e.g., Show monthly revenue statistics...",
        key="prompt_text_area_widget",
        disabled=is_loading
    )
    # Save input values dynamically on keyboard typing
    if prompt_text != st.session_state.prompt_text:
        st.session_state.prompt_text = prompt_text[:max_char]
        
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. Suggestion chips ───────────────────────────────────────────────────
    chips_html = '<div class="suggestion-chips-container">'
    for label, val in SUGGESTIONS.items():
        escaped_val = html.escape(val)
        disabled_attr = 'style="pointer-events: none; opacity: 0.5;"' if is_loading else ''
        chips_html += f'<a class="suggestion-chip" href="?prompt={escaped_val}" target="_self" {disabled_attr}>{label}</a>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)

    # ── 5. Action controls buttons ────────────────────────────────────────────
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        generate_clicked = st.button("Generate SQL", type="primary", use_container_width=True, disabled=is_loading)
    with col_btn2:
        clear_clicked = st.button("Clear", use_container_width=True, disabled=is_loading)

    # Handle clear prompt command
    if clear_clicked:
        clear_prompt()
        st.rerun()

    # Handle mock SQL generation trigger
    if generate_clicked:
        is_valid, error_msg = validate_prompt(st.session_state.prompt_text)
        if not is_valid:
            st.session_state.error_message = error_msg
            st.session_state.sql_generation_status = "error"
        else:
            st.session_state.error_message = ""
            st.session_state.sql_generation_status = "loading"
            st.rerun()

    # Process mock loading execution sequence
    if st.session_state.get("sql_generation_status") == "loading":
        with st.spinner("Translating natural prompt into SQL structure..."):
            try:
                # Simulated timeout test trigger
                if "timeout" in st.session_state.prompt_text.lower():
                    import time
                    time.sleep(2.0)
                    raise TimeoutError("Simulated backend translation query request timeout.")
                # Simulated failure test trigger
                elif "fail" in st.session_state.prompt_text.lower() or "error" in st.session_state.prompt_text.lower():
                    raise Exception("Simulated backend internal server parser exception.")
                
                # Default successful mock translation
                res_sql = generate_sql(st.session_state.prompt_text)
                st.session_state.generated_sql = res_sql
                st.session_state.sql_generation_status = "success"
                
                # Append to recent history
                if st.session_state.prompt_text not in st.session_state.recent_prompts:
                    st.session_state.recent_prompts.append(st.session_state.prompt_text)
                    
            except Exception as e:
                st.session_state.error_message = str(e)
                st.session_state.sql_generation_status = "error"
        st.rerun()

    # Render error messages if any inside the card
    err_msg = st.session_state.get("error_message", "")
    if err_msg:
        st.error(err_msg)

    # ── 6. Generated SQL block code previews ──────────────────────────────────
    sql_val = st.session_state.get("generated_sql") or "-- Generated SQL statements will render here..."
    escaped_for_js = sql_val.replace("'", "\\'").replace("\n", "\\n")
    safe_sql = html.escape(sql_val)
    
    preview_html = f"""
    <div class="sql-preview-container">
        <div class="sql-preview-header">
            <span class="sql-preview-label">Generated SQL Statement</span>
            <a class="sql-preview-copy-btn" onclick="navigator.clipboard.writeText('{escaped_for_js}'); alert('SQL Copied to Clipboard!');" href="javascript:void(0);">Copy Code</a>
        </div>
        <pre class="sql-preview-code">{safe_sql}</pre>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
