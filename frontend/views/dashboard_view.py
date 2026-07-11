"""
SchemaSay Views — Main Dashboard View

Presents database metrics overview, execution statistics, system health, and quick actions.
"""

import streamlit as st

def show_dashboard_view():
    """Renders the central metrics overview dashboard dashboard layout cards."""
    st.write("### Workspace Overview")
    st.write("Monitor connected data warehouses, AI Copilot generation query stats, and system performance.")
    st.markdown("---")

    # 1. Metric Overview Cards row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.metric("Total AI Queries", "1,248", "+12% this week")
    with col2:
        with st.container(border=True):
            st.metric("Connected Sources", "3 Active", "PostgreSQL, SQLite, MySQL")
    with col3:
        with st.container(border=True):
            st.metric("Average Latency", "1.8s", "-240ms since sync")
    with col4:
        with st.container(border=True):
            st.metric("Sandbox Blocked", "4 queries", "AST safety triggers")

    st.write("")
    
    # 2. Main content grids (Left: Recent Queries summary table, Right: Quick Actions)
    layout_col1, layout_col2 = st.columns([2.2, 1])
    
    with layout_col1:
        with st.container(border=True):
            st.write("#### Recent Workspaces Activity")
            
            # Mock table activity logs
            mock_logs = [
                {"timestamp": "2 mins ago", "prompt": "Show sales metrics for Q1", "engine": "PostgreSQL", "status": "Success"},
                {"timestamp": "1 hr ago", "prompt": "Count users registered per country", "engine": "SQLite", "status": "Success"},
                {"timestamp": "4 hrs ago", "prompt": "DELETE FROM users; -- injection test", "engine": "PostgreSQL", "status": "Blocked"},
                {"timestamp": "1 day ago", "prompt": "Find top product categories by revenue", "engine": "PostgreSQL", "status": "Success"}
            ]
            
            # Draw table headers
            st.markdown(
                """
                <table style='width:100%; border-collapse:collapse; font-size:12px; margin-top:10px;'>
                    <tr style='border-bottom:1px solid var(--color-border); text-align:left; color:var(--color-text-secondary); font-weight:600;'>
                        <th style='padding:8px;'>Time</th>
                        <th style='padding:8px;'>Prompt Query</th>
                        <th style='padding:8px;'>Database</th>
                        <th style='padding:8px;'>Status</th>
                    </tr>
                """ + "".join([
                    f"<tr style='border-bottom:1px dashed var(--color-border);'>"
                    f"  <td style='padding:8px; color:var(--color-text-secondary);'>{row['timestamp']}</td>"
                    f"  <td style='padding:8px; font-weight:500; color:var(--color-text-primary);'>{row['prompt']}</td>"
                    f"  <td style='padding:8px; color:var(--color-text-secondary);'>{row['engine']}</td>"
                    f"  <td style='padding:8px;'><span style='padding:2px 6px; border-radius:4px; font-size:10px; font-weight:bold; "
                    f"    background-color:{'rgba(16,185,129,0.1)' if row['status']=='Success' else 'rgba(239,68,68,0.1)'}; "
                    f"    color:{'var(--color-success)' if row['status']=='Success' else 'var(--color-danger)'};'>"
                    f"    {row['status']}</span></td>"
                    f"</tr>" for row in mock_logs
                ]) + "</table>",
                unsafe_allow_html=True
            )

    with layout_col2:
        with st.container(border=True):
            st.write("#### Workspace Actions")
            st.write("Quickly navigate through analytical tools:")
            
            st.write("")
            
            # Simple navigation buttons that trigger sidebar query parameters redirects
            st.markdown(
                """
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <a href="?action=nav_schemasay_ai" target="_self" style="display:block; padding:10px; border-radius:8px; border:1px solid var(--color-border); text-decoration:none; color:var(--color-text-primary); transition:var(--transition-fast); background:rgba(255,255,255,0.02);">
                        <div style="font-weight:600; font-size:13px;">🤖 Ask SchemaSay AI</div>
                        <div style="font-size:11px; color:var(--color-text-secondary); margin-top:2px;">Translate natural language prompts to SQL queries.</div>
                    </a>
                    <a href="?action=nav_connections" target="_self" style="display:block; padding:10px; border-radius:8px; border:1px solid var(--color-border); text-decoration:none; color:var(--color-text-primary); transition:var(--transition-fast); background:rgba(255,255,255,0.02);">
                        <div style="font-weight:600; font-size:13px;">🔌 Setup Database Connection</div>
                        <div style="font-size:11px; color:var(--color-text-secondary); margin-top:2px;">Add credentials or upload spreadsheet datasets.</div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
