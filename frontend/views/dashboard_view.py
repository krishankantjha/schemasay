"""
SchemaSay Views — Main Dashboard View

Implements the unified, high-density analytical workspace displaying the
AI Copilot, SQL Workbench, Schema Explorer, Query Results grid, Charts,
Query History logs, and Business Insights cards in a structured grid layout.
Now fully connected to live backend FastAPI endpoints.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from api_client import api_client
from state import KEY_ACTIVE_CONNECTION_ID, KEY_TOKEN
from utils.caching import get_cached_connections, get_cached_schema
from utils.error_handler import parse_api_response

def show_dashboard_view():
    """Renders the comprehensive multi-column dashboard grid connected to the backend."""
    token = st.session_state.get(KEY_TOKEN)
    if not token:
        st.warning("Please log in to access the analytical workspace.")
        return
        
    # Resolve active database connection ID
    active_conn_id = st.session_state.get(KEY_ACTIVE_CONNECTION_ID)
    if not active_conn_id:
        conns = get_cached_connections(token)
        if conns:
            active_conn_id = conns[0]["id"]
            st.session_state[KEY_ACTIVE_CONNECTION_ID] = active_conn_id
            
    if not active_conn_id:
        st.warning("No active database connection found. Please configure a connection first under the Connections menu.")
        return

    # Initialize session values for query results
    if "dash_execution_rows" not in st.session_state:
        st.session_state["dash_execution_rows"] = []
    if "dash_generated_sql" not in st.session_state:
        st.session_state["dash_generated_sql"] = "SELECT * FROM orders LIMIT 10;"
    if "dash_insights" not in st.session_state:
        st.session_state["dash_insights"] = []
    if "dash_wb_logs" not in st.session_state:
        st.session_state["dash_wb_logs"] = "Ready to execute workbench query statements."

    # ── ROW 1: AI Copilot & SQL Workbench ─────────────────────────────────────
    row1_col1, row1_col2 = st.columns([1, 1.1])
    
    # --- Column 1: AI Copilot ---
    with row1_col1:
        with st.container(border=True, key="dash_ai_copilot_card"):
            st.markdown(
                """
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:16px;">🤖</span>
                        <strong style="font-family:var(--font-display); font-size:14px; color:var(--color-text-primary);">AI Copilot</strong>
                        <span style="font-size:11px; color:var(--color-text-secondary); margin-left:4px;">Ask anything about your data in plain English</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Input Prompt
            prompt_input = st.text_area(
                "Prompt Input",
                placeholder="e.g. Find total sales per month...",
                height=52,
                key="dash_prompt_input_text",
                label_visibility="collapsed"
            )
            
            # Generate button trigger
            col_gen, col_empty = st.columns([1.2, 2.5])
            with col_gen:
                if st.button("Generate SQL ⚡", type="primary", key="dash_gen_sql_btn", use_container_width=True):
                    if not prompt_input.strip():
                        st.error("Please enter a prompt first.")
                    else:
                        with st.spinner("Translating prompt to SQL..."):
                            try:
                                response = api_client.query_assistant(token, active_conn_id, prompt_input)
                                if response.status_code == 200:
                                    res_data = response.json()
                                    sql = res_data.get("sql", "")
                                    st.session_state["dash_generated_sql"] = sql
                                    
                                    # Fetch results
                                    rows = res_data.get("rows", [])
                                    st.session_state["dash_execution_rows"] = rows
                                    
                                    # Generate AI insights dynamically
                                    if rows:
                                        ins_payload = {
                                            "rows": rows,
                                            "columns": list(rows[0].keys()) if rows else [],
                                            "question": prompt_input
                                        }
                                        ins_res = api_client.generate_insight(token, ins_payload)
                                        if ins_res.status_code == 200:
                                            st.session_state["dash_insights"] = ins_res.json().get("insights", [])
                                    
                                    st.success("Query generated and executed successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Error ({response.status_code}): {response.text[:200]}")
                            except Exception as e:
                                st.error(f"Assistant connection failed: {str(e)}")
                                
            # SQL Preview Box
            sql_code = st.session_state["dash_generated_sql"]
            st.markdown(
                f"""
                <div class="sql-preview-container" style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; margin-top:10px;">
                    <div class="sql-preview-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span class="sql-preview-label" style="font-size:9px; font-weight:700; color:#64748B; text-transform:uppercase;">Generated SQL code</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.code(sql_code, language="sql")

    # --- Column 2: SQL Workbench ---
    with row1_col2:
        with st.container(border=True, key="dash_sql_workbench_card"):
            st.markdown(
                """
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:16px;">💻</span>
                        <strong style="font-family:var(--font-display); font-size:14px; color:var(--color-text-primary);">SQL Workbench Editor</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Code editor populated with generated SQL
            sql_editor_val = st.text_area(
                "SQL Editor",
                value=st.session_state["dash_generated_sql"],
                height=110,
                key="dash_sql_editor_area",
                label_visibility="collapsed"
            )
            
            # Action button controls row
            wb_col1, wb_col2, wb_col3, wb_col4 = st.columns([1.2, 0.5, 0.5, 1.2])
            with wb_col1:
                if st.button("▶ Run Query", type="primary", key="dash_run_query_btn", use_container_width=True):
                    with st.spinner("Executing statement..."):
                        try:
                            response = api_client.execute_raw_sql(token, active_conn_id, sql_editor_val)
                            if response.status_code == 200:
                                rows = response.json().get("rows", [])
                                st.session_state["dash_execution_rows"] = rows
                                st.session_state["dash_wb_logs"] = f"Success | Query returned {len(rows)} rows."
                                st.rerun()
                            else:
                                st.session_state["dash_wb_logs"] = f"Failed ({response.status_code}): {response.text[:200]}"
                        except Exception as e:
                            st.session_state["dash_wb_logs"] = f"Execution failed: {str(e)}"
            with wb_col2:
                # Format SQL trigger
                if st.button("🔄", key="dash_format_sql_btn", help="Format SQL query code", use_container_width=True):
                    with st.spinner("Formatting..."):
                        try:
                            fmt_res = api_client.format_sql(token, sql_editor_val)
                            if fmt_res.status_code == 200:
                                st.session_state["dash_generated_sql"] = fmt_res.json().get("formatted_sql", sql_editor_val)
                                st.rerun()
                        except Exception:
                            pass
            with wb_col3:
                # Clear trigger
                if st.button("🗑️", key="dash_clear_sql_btn", help="Clear Editor Buffer", use_container_width=True):
                    st.session_state["dash_generated_sql"] = ""
                    st.rerun()
            with wb_col4:
                # Save Query
                st.button("💾 Save Query", key="dash_save_sql_btn", use_container_width=True)
                
            st.caption(f"`Logs:` {st.session_state['dash_wb_logs']}")

    st.write("")
    
    # ── ROW 2: Schema Explorer, Results/Charts Workspace, & Query History/Insights ──
    row2_col1, row2_col2, row2_col3 = st.columns([1, 2.1, 1.1])
    
    # --- Column 1: Schema Explorer ---
    with row2_col1:
        with st.container(border=True, key="dash_schema_explorer_card"):
            st.markdown("<strong style='font-family:var(--font-display); font-size:13px; color:var(--color-text-primary); display:block; margin-bottom:8px;'>Schema Explorer</strong>", unsafe_allow_html=True)
            
            # Load real connection schema structure
            schema_data = get_cached_schema(token, active_conn_id)
            
            if schema_data is None:
                st.info("Schema reflections not synced yet. Sync connections schema metadata using the button below.")
            else:
                tables = schema_data.get("tables", [])
                st.markdown(
                    f"""
                    <div style="font-size:12px; margin-top:8px; padding-bottom: 5px;">
                        <span style="font-weight:600; color:var(--color-text-primary);">📁 active_schema</span>
                        <span style="font-size:9px; background:var(--color-border); padding:2px 6px; border-radius:10px; font-weight:bold; color:var(--color-text-secondary);">{len(tables)}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Render real tables and their column lists
                for table in tables:
                    table_name = table.get("name", "unknown_table")
                    cols = table.get("columns", [])
                    with st.expander(f"📄 {table_name}", expanded=False):
                        cols_html = ""
                        for col in cols:
                            key_indicator = "PK" if col.get("primary_key") else "FK" if col.get("foreign_key") else "col"
                            cols_html += f"""
                            <div style="display:flex; justify-content:space-between; font-size:11px; padding:3px 0; color:var(--color-text-secondary);">
                                <span>🔹 {col.get('name')}</span>
                                <span style="font-size:9px; color:var(--color-text-muted);">{key_indicator}</span>
                            </div>
                            """
                        st.markdown(cols_html, unsafe_allow_html=True)
            
            if st.button("Sync Schema 🔄", key="dash_refresh_schema_btn", use_container_width=True):
                with st.spinner("Syncing schema reflection..."):
                    try:
                        api_client.sync_schema(token, active_conn_id)
                        st.cache_data.clear()
                        st.success("Database schemas synced successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Sync failed: {str(e)}")

    # --- Column 2: Results & Visualizations Workspace ---
    with row2_col2:
        with st.container(border=True, key="dash_results_workspace_card"):
            tab_res, tab_vis, tab_ins = st.tabs(["Results Table", "Charts & Plots", "Insights"])
            
            execution_rows = st.session_state.get("dash_execution_rows", [])
            
            # --- Results Tab ---
            with tab_res:
                if not execution_rows:
                    st.info("No query execution results available. Run a query in the editor or Copilot above to view data.")
                else:
                    df = pd.DataFrame(execution_rows)
                    st.dataframe(df, use_container_width=True, height=260)
                    
                    # Real CSV download option
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Data as CSV",
                        data=csv_data,
                        file_name="query_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # --- Visualizations Tab ---
            with tab_vis:
                if not execution_rows:
                    st.info("Run a query to populate charts dynamically.")
                else:
                    df_chart = pd.DataFrame(execution_rows)
                    # Exclude non-numeric fields if possible
                    numeric_cols = df_chart.select_dtypes(include=[np.number]).columns.tolist()
                    all_cols = df_chart.columns.tolist()
                    
                    if len(all_cols) >= 1:
                        x_col = all_cols[0]
                        y_cols = numeric_cols if numeric_cols else all_cols[1:]
                        
                        v_col1, v_col2 = st.columns(2)
                        with v_col1:
                            st.write(f"**Line Chart ({x_col} vs Y)**")
                            if y_cols:
                                st.line_chart(df_chart, x=x_col, y=y_cols[0], height=180)
                            else:
                                st.line_chart(df_chart, height=180)
                        with v_col2:
                            st.write(f"**Bar Chart ({x_col} vs Y)**")
                            if y_cols:
                                st.bar_chart(df_chart, x=x_col, y=y_cols[0], height=180)
                            else:
                                st.bar_chart(df_chart, height=180)
                    else:
                        st.warning("Dataset structure does not support charting coordinates.")
                    
            # --- Insights Tab ---
            with tab_ins:
                insights = st.session_state.get("dash_insights", [])
                if not insights:
                    st.info("No insights compiled yet. Generate a query to get automated narrative insights.")
                else:
                    for ins in insights:
                        st.markdown(
                            f"""
                            <div style="background-color:rgba(59,130,246,0.04); border:1px solid rgba(59,130,246,0.15); padding:10px; border-radius:8px; margin-bottom:10px;">
                                <strong style="color:var(--color-primary); font-size:12px;">✨ AI Insight</strong>
                                <p style="font-size:11px; color:var(--color-text-secondary); margin:4px 0 0 0;">{ins}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    # --- Column 3: Query History & Insights ---
    with row2_col3:
        # 1. Query History Card
        with st.container(border=True, key="dash_query_history_card"):
            st.markdown(
                """
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <strong style="font-family:var(--font-display); font-size:13px; color:var(--color-text-primary);">Query History</strong>
                    <a href="?action=nav_history" target="_self" style="font-size:10px; color:var(--color-primary); text-decoration:none; font-weight:600;">View All</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Fetch real history logs
            try:
                hist_res = api_client.get_query_history(token, page=1, limit=3, connection_id=active_conn_id)
                if hist_res.status_code == 200:
                    history_list = hist_res.json()
                else:
                    history_list = []
            except Exception:
                history_list = []
                
            if not history_list:
                st.caption("No query logs found.")
            else:
                for h_item in history_list:
                    # Clean prompt text preview length
                    p_text = h_item.get("question", "raw sql execution")
                    p_preview = p_text[:28] + "..." if len(p_text) > 28 else p_text
                    
                    st.markdown(
                        f"""
                        <div style="padding:6px; border-bottom:1px dashed var(--color-border); font-size:11px;">
                            <div style="display:flex; align-items:center; gap:6px;">
                                <span>🕒</span>
                                <span style="font-weight:600; color:var(--color-text-primary);">{p_preview}</span>
                            </div>
                            <div style="color:var(--color-text-secondary); font-size:9px; margin-top:2px; padding-left:18px;">
                                SQL: <code>{h_item.get('sql_query', '')[:30]}...</code>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
        st.write("")
        
        # 2. AI Business Insights Card
        with st.container(border=True, key="dash_ai_insights_card"):
            st.markdown("<strong style='font-family:var(--font-display); font-size:13px; color:var(--color-text-primary); display:block; margin-bottom:8px;'>✨ Analytical Summary</strong>", unsafe_allow_html=True)
            
            insights_summary = st.session_state.get("dash_insights", [])
            if not insights_summary:
                st.markdown(
                    """
                    <div style="font-size:11px; color:var(--color-text-secondary); line-height:1.4;">
                        No analytical summaries compiled. Once you generate a prompt, automated business summaries will appear here.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                bullets = ""
                for index, item in enumerate(insights_summary[:3]):
                    bullets += f"""
                    <div style="display:flex; gap:6px; align-items:start; margin-bottom: 6px;">
                        <span style="color:var(--color-primary);">🔹</span>
                        <span>{item[:80]}...</span>
                    </div>
                    """
                st.markdown(bullets, unsafe_allow_html=True)
