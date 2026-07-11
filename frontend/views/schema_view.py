"""
SchemaSay Views — Schema Explorer View

Renders the database schemas hierarchy trees, table listings, and columns info.
"""

import streamlit as st

def show_schema_view():
    """Renders the database schema introspection catalog mockup."""
    with st.container(border=True):
        st.write("### Database Schema Explorer")
        st.write("Browse table columns, structural datatypes, primary key relationships, and index definitions.")
        st.markdown("---")

        # 1. Search filter
        search_query = st.text_input("🔍 Filter tables or columns...", placeholder="e.g. customer_id, orders")
        
        col_list, col_details = st.columns([1, 2])
        
        # 2. Table Sidebar list selection
        with col_list:
            st.write("**Tables**")
            selected_table = st.radio(
                "Select table to inspect:",
                options=["public.sales_metrics", "public.customers", "public.products", "public.orders", "auth.users"],
                label_visibility="collapsed"
            )
            
        # 3. Columns inspection preview details card
        with col_details:
            st.write(f"**Structure: `{selected_table}`**")
            
            # Show mock details based on selection
            columns_data = {
                "public.sales_metrics": [
                    {"column": "sale_id", "type": "INTEGER", "key": "PK", "nullable": "NO"},
                    {"column": "product_id", "type": "INTEGER", "key": "FK", "nullable": "NO"},
                    {"column": "quantity", "type": "INTEGER", "key": "", "nullable": "NO"},
                    {"column": "price", "type": "NUMERIC(10,2)", "key": "", "nullable": "NO"},
                    {"column": "sale_date", "type": "DATE", "key": "", "nullable": "NO"}
                ],
                "public.customers": [
                    {"column": "customer_id", "type": "INTEGER", "key": "PK", "nullable": "NO"},
                    {"column": "first_name", "type": "VARCHAR(50)", "key": "", "nullable": "NO"},
                    {"column": "last_name", "type": "VARCHAR(50)", "key": "", "nullable": "NO"},
                    {"column": "email", "type": "VARCHAR(100)", "key": "UQ", "nullable": "NO"}
                ],
                "public.products": [
                    {"column": "product_id", "type": "INTEGER", "key": "PK", "nullable": "NO"},
                    {"column": "product_name", "type": "VARCHAR(100)", "key": "", "nullable": "NO"},
                    {"column": "category", "type": "VARCHAR(50)", "key": "", "nullable": "YES"},
                    {"column": "price", "type": "NUMERIC(10,2)", "key": "", "nullable": "NO"}
                ],
                "public.orders": [
                    {"column": "order_id", "type": "INTEGER", "key": "PK", "nullable": "NO"},
                    {"column": "customer_id", "type": "INTEGER", "key": "FK", "nullable": "NO"},
                    {"column": "order_date", "type": "TIMESTAMP", "key": "", "nullable": "NO"},
                    {"column": "amount", "type": "NUMERIC(12,2)", "key": "", "nullable": "NO"}
                ],
                "auth.users": [
                    {"column": "id", "type": "UUID", "key": "PK", "nullable": "NO"},
                    {"column": "email", "type": "VARCHAR(255)", "key": "UQ", "nullable": "NO"},
                    {"column": "hashed_password", "type": "VARCHAR(255)", "key": "", "nullable": "NO"},
                    {"column": "created_at", "type": "TIMESTAMP WITH TIME ZONE", "key": "", "nullable": "NO"}
                ]
            }
            
            rows = columns_data.get(selected_table, [])
            st.dataframe(rows, use_container_width=True)
            
            # Show additional indexes info
            with st.expander("Show Database Indexes & Constraints"):
                if "sales_metrics" in selected_table:
                    st.code("CREATE UNIQUE INDEX sales_metrics_pkey ON sales_metrics (sale_id);\nCREATE INDEX idx_sales_product ON sales_metrics (product_id);")
                else:
                    st.code(f"CREATE UNIQUE INDEX {selected_table.split('.')[1]}_pkey ON {selected_table.split('.')[1]} (id);")
