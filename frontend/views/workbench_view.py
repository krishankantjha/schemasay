"""
SchemaSay Views — SQL Workbench View

Renders the SQL Editor, execute actions, and query performance status blocks.
"""

import streamlit as st

def show_workbench_view():
    """Renders the SQL Workbench UI mockup."""
    with st.container(border=True):
        st.write("### SQL Query Workbench")
        st.write("Write, format, and execute custom SQL statements directly against your active database connection.")
        st.markdown("---")

        # 1. Dialect & Engine Selector
        col_eng, col_clear = st.columns([3, 1])
        with col_eng:
            active_engine = st.selectbox(
                "Active Source Connection",
                options=["postgresql_sales", "sqlite_mock", "mysql_prod"],
                format_func=lambda x: {
                    "postgresql_sales": "PostgreSQL (sales_ledger_db)",
                    "sqlite_mock": "SQLite (demo_sales_sqlite)",
                    "mysql_prod": "MySQL (production_warehouse)"
                }[x]
            )
        
        # 2. Text Editor
        sql_input = st.text_area(
            "SQL Query Editor",
            value="SELECT * FROM public.sales_metrics LIMIT 10;",
            height=220,
            placeholder="Type your SQL query here...",
            key="workbench_sql_editor"
        )

        # 3. Action Buttons row
        btn_col1, btn_col2, _ = st.columns([1, 1, 3])
        with btn_col1:
            st.button("Execute Query", type="primary", use_container_width=True)
        with btn_col2:
            if st.button("Clear Buffer", type="secondary", use_container_width=True):
                st.session_state.workbench_sql_editor = ""
                st.rerun()

        st.markdown("---")
        
        # 4. Results / Status Area mock
        st.write("#### Execution Feedback")
        st.info("Query compiled successfully in 140ms. Returning 10 rows from public.sales_metrics.")
        
        # Mock dataframe preview
        mock_data = [
            {"sale_id": 1001, "product_id": 405, "quantity": 3, "price": 49.99, "sale_date": "2026-07-08"},
            {"sale_id": 1002, "product_id": 204, "quantity": 1, "price": 120.00, "sale_date": "2026-07-08"},
            {"sale_id": 1003, "product_id": 312, "quantity": 5, "price": 15.50, "sale_date": "2026-07-09"},
            {"sale_id": 1004, "product_id": 405, "quantity": 2, "price": 49.99, "sale_date": "2026-07-09"}
        ]
        st.dataframe(mock_data, use_container_width=True)
