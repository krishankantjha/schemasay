"""
SchemaSay Views — Query Results View

Presents database results tables, pagination elements, and data exporting panels.
"""

import streamlit as st

def show_results_view():
    """Renders the paginated query results preview grid."""
    with st.container(border=True):
        st.write("### Execution Results")
        st.write("View, sort, filter, and export datasets returned from executed workbench statements.")
        st.markdown("---")

        # 1. Filter, Search, and Export Toolbar Row
        col_search, col_sort, col_export = st.columns([2, 1, 1])
        with col_search:
            st.text_input("🔍 Search within results...", placeholder="Filter values...")
        with col_sort:
            st.selectbox("Sort By Column", options=["sale_id", "price", "sale_date"])
        with col_export:
            st.write("") # label spacing
            st.selectbox("Export File As", options=["CSV Spreadsheet", "Excel Document", "JSON Array"])

        # 2. Results Data Grid table
        st.markdown("##### Query: `SELECT * FROM public.sales_metrics ORDER BY sale_id ASC;`")
        
        mock_dataset = [
            {"sale_id": 1001, "product_id": 405, "quantity": 3, "price": 49.99, "sale_date": "2026-07-08", "region": "North"},
            {"sale_id": 1002, "product_id": 204, "quantity": 1, "price": 120.00, "sale_date": "2026-07-08", "region": "West"},
            {"sale_id": 1003, "product_id": 312, "quantity": 5, "price": 15.50, "sale_date": "2026-07-09", "region": "East"},
            {"sale_id": 1004, "product_id": 405, "quantity": 2, "price": 49.99, "sale_date": "2026-07-09", "region": "North"},
            {"sale_id": 1005, "product_id": 108, "quantity": 10, "price": 8.99, "sale_date": "2026-07-10", "region": "South"},
            {"sale_id": 1006, "product_id": 204, "quantity": 2, "price": 120.00, "sale_date": "2026-07-10", "region": "West"},
            {"sale_id": 1007, "product_id": 312, "quantity": 4, "price": 15.50, "sale_date": "2026-07-11", "region": "East"}
        ]
        
        st.dataframe(mock_dataset, use_container_width=True)

        # 3. Pagination controls row
        page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
        with page_col1:
            st.button("⬅️ Previous", disabled=True, key="res_prev_btn")
        with page_col2:
            st.markdown("<p style='text-align:center; font-size:12px; color:var(--color-text-secondary); line-height:32px;'>Showing 1-7 of 7 entries (Page 1 of 1)</p>", unsafe_allow_html=True)
        with page_col3:
            st.button("Next ➡️", disabled=True, key="res_next_btn")
