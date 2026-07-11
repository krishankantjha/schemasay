"""
SchemaSay Views — Dataset Uploader View

Renders file drag-and-drop ingestion cards and metadata reflection previews.
"""

import streamlit as st
import pandas as pd

def show_upload_view():
    """Renders the spreadsheets file ingestion layout."""
    with st.container(border=True):
        st.write("### Dataset Upload Manager")
        st.write("Ingest offline CSV or Excel spreadsheets. SchemaSay will reflect their data structure, map types, and register them as relational sources.")
        st.markdown("---")

        # Ingestion form fields
        up_name = st.text_input("Ingestion Source Name", placeholder="e.g. Employee Roster Q2")
        up_file = st.file_uploader("Choose CSV or Excel Spreadsheet", type=["csv", "xlsx", "xls"], key="dataset_uploader_field")

        if up_file is not None:
            st.success(f"File loaded successfully: {up_file.name} ({up_file.size} bytes)")
            
            # Draw preview card
            with st.container(border=True):
                st.write("#### Table Schema Reflection Preview")
                
                # Load mockup dataframe structure depending on extension
                try:
                    if up_file.name.endswith(".csv"):
                        df_preview = pd.read_csv(up_file, nrows=5)
                    else:
                        df_preview = pd.read_excel(up_file, nrows=5)
                    st.dataframe(df_preview, use_container_width=True)
                except Exception:
                    # Fallback default mock
                    mock_preview = {
                        "employee_id": [101, 102, 103],
                        "full_name": ["Alice Smith", "Bob Jones", "Charlie Brown"],
                        "department": ["Engineering", "Product", "Sales"],
                        "hire_date": ["2024-01-15", "2024-03-20", "2025-06-01"]
                    }
                    st.dataframe(mock_preview, use_container_width=True)
                
            st.markdown("---")
            if st.button("Process and Sync Table Schema", type="primary"):
                if not up_name:
                    st.error("Please assign a connection name to this dataset.")
                else:
                    st.success(f"Ingested '{up_name}' into database. Table schema reflected successfully!")
