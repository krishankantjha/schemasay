"""
SchemaSay Views — Query History View

Displays historical prompts, target engines, executed SQLs, and re-run/delete handlers.
"""

import streamlit as st

def show_history_view():
    """Renders the previous executed prompts logs history list."""
    with st.container(border=True):
        st.write("### Query Logs & Execution History")
        st.write("Browse, audit, and re-run previous natural language queries executed on connected databases.")
        st.markdown("---")

        # Mock query logs data
        history_logs = [
            {
                "id": 1,
                "timestamp": "2026-07-11 15:30:14",
                "prompt": "Show top 5 sales transactions from July 8",
                "sql": "SELECT * FROM public.sales_metrics WHERE sale_date = '2026-07-08' ORDER BY price DESC LIMIT 5;",
                "db": "sales_ledger_db (PostgreSQL)"
            },
            {
                "id": 2,
                "timestamp": "2026-07-11 11:20:45",
                "prompt": "Total count of registered users in the platform",
                "sql": "SELECT COUNT(*) AS total_users FROM auth.users;",
                "db": "sales_ledger_db (PostgreSQL)"
            },
            {
                "id": 3,
                "timestamp": "2026-07-10 18:45:10",
                "prompt": "Find products list with price above 100",
                "sql": "SELECT * FROM public.products WHERE price > 100.00 ORDER BY price ASC;",
                "db": "demo_sales_sqlite (SQLite)"
            }
        ]

        # Draw each log block card
        for log in history_logs:
            with st.container(border=True):
                col_meta, col_actions = st.columns([4, 1.2])
                with col_meta:
                    st.markdown(f"**Prompt:** `{log['prompt']}`")
                    st.markdown(f"<span style='font-size:11px; color:var(--color-text-secondary);'>Ran on **{log['db']}** • {log['timestamp']}</span>", unsafe_allow_html=True)
                with col_actions:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        st.button("Re-run", key=f"hist_rerun_{log['id']}", use_container_width=True)
                    with btn_col2:
                        st.button("Delete", key=f"hist_del_{log['id']}", use_container_width=True)
                
                # SQL preview block
                st.code(log["sql"], language="sql")
                st.write("")
