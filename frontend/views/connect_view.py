import streamlit as st
import pandas as pd
from api_client import api_client

def show_connection_manager():
    """
    Renders the Database Connections Manager screen using Streamlit.
    Provides panels to view connections, test/save new servers, upload files,
    and monitor query execution history logs.
    """
    st.subheader("Database Connection Manager")
    
    token = st.session_state.get("token")
    if not token:
        st.error("Session expired. Please log in again.")
        return

    # Setup distinct tabs for different manager operations
    tab_list, tab_add, tab_upload, tab_history = st.tabs([
        "Saved Connections", 
        "Connect Database Server", 
        "Upload Spreadsheet", 
        "Execution History"
    ])

    # Tab 1: List and Delete Connections
    with tab_list:
        with st.spinner("Loading connections..."):
            response = api_client.get_connections(token)
            
        if response.status_code == 200:
            connections = response.json()
            if not connections:
                st.info("No database connections saved yet. Add a database or upload a file to begin.")
            else:
                # Convert connection records to a display DataFrame
                conn_data = []
                for c in connections:
                    conn_data.append({
                        "ID": c["id"],
                        "Name": c["name"],
                        "Type": c["db_type"].upper(),
                        "Host": c["host"] or "Local / Uploaded",
                        "Database/Path": c["database_name"],
                        "Username": c["username"] or "N/A"
                    })
                
                st.dataframe(pd.DataFrame(conn_data), use_container_width=True)
                
                # Delete connection action UI
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
                        
                    if del_response.status_code == 200:
                        st.success("Connection deleted successfully.")
                        st.rerun()
                    else:
                        st.error(del_response.json().get("detail", "Failed to delete connection"))
        else:
            st.error("Failed to load database connections.")

    # Tab 2: Add Live Database Server Connection
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
        
        # Display inputs dynamically depending on type selection
        if db_type == "sqlite":
            database_name = st.text_input("Absolute File Path", placeholder="C:/databases/my_data.db")
            host = None
            port = None
            username = None
            password = None
        else:
            host = st.text_input("Host Address", placeholder="127.0.0.1")
            default_port = {"postgresql": 5432, "mysql": 3306, "mssql": 1433}[db_type]
            port = st.number_input("Port", min_value=1, max_value=65535, value=default_port)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            database_name = st.text_input("Database Name")

        col1, col2 = st.columns(2)
        
        # Test Connection Trigger
        with col1:
            if st.button("Test Connection"):
                if not name or not database_name:
                    st.error("Name and database path/name are required.")
                elif db_type != "sqlite" and (not host or not username or not password):
                    st.error("Host, Username, and Password are required for server databases.")
                else:
                    test_payload = {
                        "db_type": db_type,
                        "host": host,
                        "port": port,
                        "username": username,
                        "password": password,
                        "database_name": database_name
                    }
                    with st.spinner("Testing database connectivity..."):
                        test_response = api_client.test_connection(token, test_payload)
                        
                    if test_response.status_code == 200:
                        st.success("Connection test succeeded!")
                    else:
                        detail = test_response.json().get("detail", "Connection test failed")
                        st.error(detail)
                        
        # Save Connection Trigger
        with col2:
            if st.button("Save Connection"):
                if not name or not database_name:
                    st.error("Name and database path/name are required.")
                elif db_type != "sqlite" and (not host or not username or not password):
                    st.error("Host, Username, and Password are required for server databases.")
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
                        
                    if save_response.status_code == 201:
                        st.success("Connection saved successfully.")
                        st.rerun()
                    else:
                        detail = save_response.json().get("detail", "Failed to save connection")
                        st.error(detail)

    # Tab 3: Upload CSV or Excel file
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
                    
                if response.status_code == 201:
                    st.success("File uploaded and connection created successfully!")
                    st.rerun()
                else:
                    detail = response.json().get("detail", "File upload failed")
                    st.error(detail)

    # Tab 4: Execution History Audit Logs
    with tab_history:
        st.write("#### Query Execution History")
        with st.spinner("Loading query history logs..."):
            history_response = api_client.get_query_history(token)
            
        if history_response.status_code == 200:
            history_logs = history_response.json()
            if not history_logs:
                st.info("No query logs generated yet. Queries run in later phases will be audited here.")
            else:
                log_rows = []
                for log in history_logs:
                    log_rows.append({
                        "Time": datetime_str := log["created_at"].replace("T", " ")[:19],
                        "Question": log["question"],
                        "Generated SQL": log["sql_query"],
                        "Status": log["status"].upper(),
                        "Duration (ms)": log["execution_duration_ms"] or "N/A",
                        "Errors": log["error_message"] or "None"
                    })
                st.dataframe(pd.DataFrame(log_rows), use_container_width=True)
        else:
            st.error("Failed to load query execution logs.")
