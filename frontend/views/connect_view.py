import streamlit as st
import io
from api_client import api_client
from utils.error_handler import parse_api_response
from state import KEY_TOKEN

def show_connection_manager():
    """
    Renders database connection listings, configuration editing forms, and CSV/Excel file uploads.
    Enforces standardized API error checks.
    """
    token = st.session_state.get(KEY_TOKEN)
    if not token:
        st.warning("Please log in to manage database connections.")
        return

    st.write("### Database Connection Manager")
    st.write("Configure connection credentials to live database servers or ingest flat spreadsheet files.")

    # 1. Initialize view tabs
    tab_list, tab_add, tab_upload = st.tabs(["Active Connections", "Configure Server Connection", "Upload Flat File"])

    # --- Tab: Active Connections ---
    with tab_list:
        st.write("#### Configured Database Sources")
        
        # Load connections
        with st.spinner("Fetching active database connections..."):
            response = api_client.get_connections(token)
            
        connections = parse_api_response(response, "fetch database connections")
        
        if connections is not None:
            if not connections:
                st.info("No connections configured yet. Use the 'Configure Server Connection' or 'Upload Flat File' tabs to get started.")
            else:
                for conn in connections:
                    with st.expander(f"Name: {conn['name']} (Engine: {conn['db_type'].upper()})"):
                        st.write(f"- **ID:** {conn['id']}")
                        st.write(f"- **Database Name:** {conn['database_name']}")
                        st.write(f"- **Host:** {conn['host'] or 'Local Host / Flat File'}")
                        if conn['port']:
                            st.write(f"- **Port:** {conn['port']}")
                        st.write(f"- **Username:** {conn['username'] or 'N/A'}")
                        st.write(f"- **Created At:** {conn['created_at']}")
                
                st.markdown("---")
                st.write("#### Remove a Connection")
                del_ids = [c["id"] for c in connections]
                del_names = {c["id"]: f"{c['name']} ({c['db_type'].upper()})" for c in connections}
                
                selected_del_id = st.selectbox(
                    "Select connection to delete", 
                    options=del_ids, 
                    format_func=lambda x: del_names[x]
                )
                
                if st.button("Delete Connection", key="del_conn_btn"):
                    with st.spinner("Deleting connection..."):
                        del_response = api_client.delete_connection(token, selected_del_id)
                        
                    data = parse_api_response(del_response, "delete connection")
                    if data:
                        st.success("Connection deleted successfully.")
                        st.cache_data.clear()
                        st.rerun()

    # --- Tab: Configure Server Connection ---
    with tab_add:
        st.write("#### Configure a Database Server")
        
        db_type = st.selectbox(
            "Database Engine Type",
            options=["postgresql", "mysql", "mssql", "sqlite"],
            format_func=lambda x: {
                "postgresql": "PostgreSQL",
                "mysql": "MySQL",
                "mssql": "Microsoft SQL Server",
                "sqlite": "Local SQLite Database File"
            }[x]
        )
        
        name = st.text_input("Connection Name", placeholder="e.g. Sales DB")
        
        # SQLite connections only need a file path — skip host, port, and credentials fields
        if db_type == "sqlite":
            database_name = st.text_input("Local File Path", placeholder="e.g. /data/sales.db")
            host = ""
            port = None
            username = ""
            password = ""
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                host = st.text_input("Server Host address", placeholder="e.g. 192.168.1.1 or db.sales.company.com")
            with col2:
                port = st.number_input("Port", min_value=1, max_value=65535, value=5432)
                
            col3, col4 = st.columns([1, 1])
            with col3:
                username = st.text_input("Username", placeholder="e.g. read_only_user")
            with col4:
                password = st.text_input("Password", type="password", placeholder="Secure login credential")
                
            database_name = st.text_input("Target Database Name", placeholder="e.g. core_sales_ledger")

        st.markdown("---")
        col_test, col_save = st.columns([1, 1])

        with col_test:
            if st.button("Test Parameters Connection"):
                if not name:
                    st.error("Please enter a name for this connection.")
                elif db_type != "sqlite" and (not host or not username or not password):
                    st.error("Please fill in host, username, and password fields to test.")
                elif not database_name:
                    st.error("Please fill in database name parameter.")
                else:
                    test_payload = {
                        "db_type": db_type,
                        "host": host,
                        "port": port,
                        "username": username,
                        "password": password,
                        "database_name": database_name
                    }
                    with st.spinner("Testing parameters connection..."):
                        test_response = api_client.test_connection(token, test_payload)
                        
                    data = parse_api_response(test_response, "test connection")
                    if data and data.get("success"):
                        st.success("Connection test succeeded!")

        with col_save:
            if st.button("Save Database Configuration"):
                if not name:
                    st.error("Please enter a name for this connection.")
                elif db_type != "sqlite" and (not host or not username or not password):
                    st.error("Please fill in host, username, and password fields to save.")
                elif not database_name:
                    st.error("Please fill in database name parameter.")
                else:
                    save_payload = {
                        "name": name,
                        "db_type": db_type,
                        "host": host,
                        "port": port,
                        "username": username,
                        "password": password,
                        "database_name": database_name
                    }
                    with st.spinner("Saving database configuration..."):
                        save_response = api_client.create_connection(token, save_payload)
                        
                    data = parse_api_response(save_response, "save connection")
                    if data:
                        st.success("Connection saved successfully.")
                        st.cache_data.clear()
                        st.rerun()

    # --- Tab: Upload CSV or Excel File ---
    with tab_upload:
        st.write("#### Upload Flat Spreadsheets")
        st.info("Uploaded CSV and Excel spreadsheets will be converted into local SQLite tables automatically.")
        
        upload_name = st.text_input("Connection Name", key="upload_name_input", placeholder="e.g. Sales Report 2026")
        uploaded_file = st.file_uploader("Select CSV or Excel Spreadsheet File", type=["csv", "xlsx", "xls"])
        
        if st.button("Upload and Process File"):
            if not upload_name:
                st.error("Please enter a name for this connection.")
            elif not uploaded_file:
                st.error("Please select a file to upload.")
            else:
                with st.spinner("Ingesting file and converting to SQLite..."):
                    response = api_client.upload_file_connection(
                        token=token,
                        name=upload_name,
                        file_name=uploaded_file.name,
                        file_bytes=uploaded_file.read()
                    )
                data = parse_api_response(response, "upload spreadsheet connection")
                if data:
                    st.success(f"Success | Ingested spreadsheet, cached tables, and registered SQLite database.")
                    st.cache_data.clear()
                    st.rerun()
