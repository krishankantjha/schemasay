"""
SchemaSay Views — Main Dashboard View

Implements the unified, high-density analytical workspace displaying the
AI Copilot, SQL Workbench, Schema Explorer, Query Results grid, Charts,
Query History logs, and Business Insights cards in a structured grid layout.
"""

import streamlit as st
import pandas as pd
import numpy as np

def show_dashboard_view():
    """Renders the comprehensive multi-column dashboard grid."""
    
    # ── ROW 1: AI Copilot & SQL Workbench ─────────────────────────────────────
    row1_col1, row1_col2 = st.columns([1, 1.1])
    
    # --- Column 1: AI Copilot ---
    with row1_col1:
        with st.container(border=True, key="dash_ai_copilot_card"):
            # Header
            st.markdown(
                """
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:16px;">🤖</span>
                        <strong style="font-family:var(--font-display); font-size:14px; color:var(--color-text-primary);">AI Copilot</strong>
                        <span style="font-size:11px; color:var(--color-text-secondary); margin-left:4px;">Ask anything about your data in natural language</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Input Prompt
            prompt_input = st.text_area(
                "Prompt Input",
                value="Show total sales per month for the last year",
                height=52,
                key="dash_prompt_input",
                label_visibility="collapsed"
            )
            
            # Action buttons
            col_gen, col_empty = st.columns([1, 2.5])
            with col_gen:
                st.button("Generate SQL ⚡", type="primary", key="dash_gen_sql_btn", use_container_width=True)
                
            # SQL Preview Box
            st.markdown(
                """
                <div class="sql-preview-container" style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; margin-top:10px;">
                    <div class="sql-preview-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span class="sql-preview-label" style="font-size:9px; font-weight:700; color:#64748B; text-transform:uppercase;">SQL Preview</span>
                        <a href="#" class="sql-preview-copy-btn" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:4px; color:#475569; font-size:9px; font-weight:600; padding:2px 6px; text-decoration:none;">Copy SQL</a>
                    </div>
                    <pre class="sql-preview-code" style="font-family:var(--font-mono); font-size:11px; color:#0F172A; margin:0; white-space:pre-wrap; line-height:1.4;">SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(total_amount) AS total_sales
FROM orders
WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
GROUP BY 1
ORDER BY 1;</pre>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --- Column 2: SQL Workbench ---
    with row1_col2:
        with st.container(border=True, key="dash_sql_workbench_card"):
            # Header
            st.markdown(
                """
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:16px;">💻</span>
                        <strong style="font-family:var(--font-display); font-size:14px; color:var(--color-text-primary);">SQL Workbench</strong>
                    </div>
                    <a href="#" style="font-size:11px; color:var(--color-primary); text-decoration:none; font-weight:600;">{} Format SQL</a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Code editor
            st.text_area(
                "SQL Editor",
                value="""1  SELECT DATE_TRUNC('month', order_date) AS month,
2         SUM(total_amount) AS total_sales
3  FROM orders
4  WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
5  GROUP BY 1
6  ORDER BY 1;""",
                height=110,
                key="dash_sql_editor",
                label_visibility="collapsed"
            )
            
            # Action button controls row
            wb_col1, wb_col2, wb_col3, wb_col4 = st.columns([1.2, 0.5, 0.5, 1.2])
            with wb_col1:
                st.button("▶ Run Query", type="primary", key="dash_run_query_btn", use_container_width=True)
            with wb_col2:
                st.button("📤", key="dash_upload_sql_btn", use_container_width=True)
            with wb_col3:
                st.button("🔄", key="dash_refresh_sql_btn", use_container_width=True)
            with wb_col4:
                st.button("💾 Save Query", key="dash_save_sql_btn", use_container_width=True)

    st.write("")
    
    # ── ROW 2: Schema Explorer, Results/Charts Workspace, & Query History/Insights ──
    row2_col1, row2_col2, row2_col3 = st.columns([1, 2.1, 1.1])
    
    # --- Column 1: Schema Explorer ---
    with row2_col1:
        with st.container(border=True, key="dash_schema_explorer_card"):
            st.markdown("<strong style='font-family:var(--font-display); font-size:13px; color:var(--color-text-primary); display:block; margin-bottom:8px;'>Schema Explorer</strong>", unsafe_allow_html=True)
            
            # Search tables
            st.text_input("Search tables...", label_visibility="collapsed", placeholder="Search tables or columns...", key="dash_schema_search")
            
            # Render schema folder hierarchy
            st.markdown(
                """
                <div style="font-size:12px; margin-top:8px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:4px 0;">
                        <span style="font-weight:600; color:var(--color-text-primary);">📁 public</span>
                        <span style="font-size:9px; background:var(--color-border); padding:2px 6px; border-radius:10px; font-weight:bold; color:var(--color-text-secondary);">12</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Orders table expandable fields list
            with st.expander("📄 orders", expanded=True):
                st.markdown(
                    """
                    <div style="font-size:11px; padding-left:10px; display:flex; flex-direction:column; gap:6px; color:var(--color-text-secondary);">
                        <div style="display:flex; justify-content:space-between;"><span>🔹 order_id</span><span style="font-size:9px; color:var(--color-text-muted);">PK</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>📅 customer_id</span><span style="font-size:9px; color:var(--color-text-muted);">FK</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>📅 order_date</span><span style="font-size:9px; color:var(--color-text-muted);">date</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>💰 total_amount</span><span style="font-size:9px; color:var(--color-text-muted);">numeric</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>📄 status</span><span style="font-size:9px; color:var(--color-text-muted);">varchar</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            # Other mock tables
            with st.expander("📄 customers", expanded=False):
                st.write("")
            with st.expander("📄 products", expanded=False):
                st.write("")
            with st.expander("📄 order_items", expanded=False):
                st.write("")
            with st.expander("📄 categories", expanded=False):
                st.write("")
                
            st.button("Refresh Schema 🔄", key="dash_refresh_schema_btn", use_container_width=True)

    # --- Column 2: Results & Visualizations Workspace ---
    with row2_col2:
        with st.container(border=True, key="dash_results_workspace_card"):
            tab_res, tab_vis, tab_ins = st.tabs(["Results", "Visualizations", "Insights"])
            
            # --- Results Tab ---
            with tab_res:
                col_res_search, col_res_export = st.columns([2, 1.5])
                with col_res_search:
                    st.text_input("Search results...", label_visibility="collapsed", placeholder="Search results...", key="dash_res_search")
                with col_res_export:
                    exp_col1, exp_col2 = st.columns([2, 1])
                    with exp_col1:
                        st.button("📥 Download", key="dash_download_res_btn", use_container_width=True)
                    with exp_col2:
                        st.button("⚙️", key="dash_settings_res_btn", use_container_width=True)
                
                # Draw table data
                mock_table = [
                    {"month": "2024-01-01", "total_sales": "98,420.50", "order_count": "1,243", "avg_order_value": "79.23", "new_customers": "342"},
                    {"month": "2024-02-01", "total_sales": "110,250.75", "order_count": "1,512", "avg_order_value": "72.88", "new_customers": "421"},
                    {"month": "2024-03-01", "total_sales": "125,630.20", "order_count": "1,785", "avg_order_value": "70.41", "new_customers": "512"},
                    {"month": "2024-04-01", "total_sales": "132,980.60", "order_count": "1,958", "avg_order_value": "67.98", "new_customers": "480"},
                    {"month": "2024-05-01", "total_sales": "142,770.90", "order_count": "2,104", "avg_order_value": "67.83", "new_customers": "567"}
                ]
                
                st.dataframe(mock_table, use_container_width=True)
                
                # Mock pagination controls
                pg_col1, pg_col2, pg_col3, pg_col4 = st.columns([2, 1.2, 0.8, 1])
                with pg_col1:
                    st.markdown("<span style='font-size:11px; color:var(--color-text-secondary); line-height:32px;'>Showing 1 to 5 of 12 results</span>", unsafe_allow_html=True)
                with pg_col2:
                    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
                    p_col1.button("◀", key="dash_page_prev", use_container_width=True)
                    p_col2.button("1", key="dash_page_1", type="primary", use_container_width=True)
                    p_col3.button("2", key="dash_page_2", use_container_width=True)
                    p_col4.button("▶", key="dash_page_next", use_container_width=True)
                with pg_col4:
                    st.selectbox("per_page", options=["5 / page", "10 / page", "25 / page"], key="dash_per_page_select", label_visibility="collapsed")
            
            # --- Visualizations Tab ---
            with tab_vis:
                st.write("#### Analytics Visualizations Preview")
                
                # Renders small mock charts side by side
                vc1, vc2 = st.columns(2)
                
                # Mock dataset
                chart_dates = pd.date_range(start="2026-07-01", periods=10)
                revenue_vals = [1200, 1500, 1100, 1800, 2200, 1900, 2400, 2600, 2100, 2800]
                units_vals = [40, 52, 38, 60, 75, 63, 80, 88, 70, 95]
                chart_df = pd.DataFrame({"Date": chart_dates, "Revenue": revenue_vals, "Units": units_vals})
                
                with vc1:
                    st.write("**Line Chart (Revenue)**")
                    st.line_chart(chart_df, x="Date", y="Revenue", height=120)
                with vc2:
                    st.write("**Bar Chart (Units)**")
                    st.bar_chart(chart_df, x="Date", y="Units", height=120)
                    
            # --- Insights Tab ---
            with tab_ins:
                st.write("#### AI Insights Alert Logs")
                st.markdown(
                    """
                    <div style="background-color:rgba(16,185,129,0.04); border:1px solid rgba(16,185,129,0.15); padding:10px; border-radius:8px; margin-bottom:10px;">
                        <strong style="color:var(--color-success); font-size:12px;">📈 Revenue Acceleration Detected</strong>
                        <p style="font-size:11px; color:var(--color-text-secondary); margin:4px 0 0 0;">Sales metrics show a 12% revenue growth rate starting July 8. spike is highly correlated with zones campaign.</p>
                    </div>
                    <div style="background-color:rgba(245,158,11,0.04); border:1px solid rgba(245,158,11,0.15); padding:10px; border-radius:8px;">
                        <strong style="color:var(--color-warning); font-size:12px;">⚠️ Unusual Cart Abandonment Spike</strong>
                        <p style="font-size:11px; color:var(--color-text-secondary); margin:4px 0 0 0;">A 4.2x increase in abandoned carts was identified on July 9. Recommend checking checkout api logs.</p>
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
            
            st.text_input("Search queries...", label_visibility="collapsed", placeholder="Search queries...", key="dash_hist_search")
            
            # Mock historical prompts list
            st.markdown(
                """
                <div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">
                    <div style="padding:6px; border-bottom:1px dashed var(--color-border); font-size:11px;">
                        <div style="display:flex; align-items:center; gap:6px;">
                            <span>🕒</span>
                            <span style="font-weight:600; color:var(--color-text-primary);">Show total sales per month for...</span>
                        </div>
                        <div style="color:var(--color-text-secondary); font-size:10px; margin-top:2px; padding-left:18px;">Just now</div>
                    </div>
                    <div style="padding:6px; border-bottom:1px dashed var(--color-border); font-size:11px;">
                        <div style="display:flex; align-items:center; gap:6px;">
                            <span>⚡</span>
                            <span style="font-weight:600; color:var(--color-text-primary);">Top 10 customers by total sales</span>
                        </div>
                        <div style="color:var(--color-text-secondary); font-size:10px; margin-top:2px; padding-left:18px;">Yesterday</div>
                    </div>
                    <div style="padding:6px; font-size:11px;">
                        <div style="display:flex; align-items:center; gap:6px;">
                            <span>🟢</span>
                            <span style="font-weight:600; color:var(--color-text-primary);">Products with low stock</span>
                        </div>
                        <div style="color:var(--color-text-secondary); font-size:10px; margin-top:2px; padding-left:18px;">2 days ago</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.write("")
        
        # 2. AI Business Insights Card
        with st.container(border=True, key="dash_ai_insights_card"):
            st.markdown("<strong style='font-family:var(--font-display); font-size:13px; color:var(--color-text-primary); display:block; margin-bottom:8px;'>✨ AI Business Insights</strong>", unsafe_allow_html=True)
            
            st.markdown(
                """
                <div style="display:flex; flex-direction:column; gap:8px; font-size:11px; color:var(--color-text-secondary); line-height:1.4;">
                    <div style="display:flex; gap:6px; align-items:start;">
                        <span style="color:var(--color-primary);">📈</span>
                        <span>Sales show a steady upward trend with a 45% increase from Jan to May.</span>
                    </div>
                    <div style="display:flex; gap:6px; align-items:start;">
                        <span style="color:var(--color-warning);">⭐️</span>
                        <span>May has the highest sales of $142,770.90.</span>
                    </div>
                    <div style="display:flex; gap:6px; align-items:start;">
                        <span style="color:var(--color-success);">💵</span>
                        <span>Average order value is consistent between $67 - $79.</span>
                    </div>
                    <div style="display:flex; gap:6px; align-items:start;">
                        <span style="color:var(--color-primary);">👥</span>
                        <span>New customer acquisition is growing month over month.</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
