import streamlit as st
from api_client import api_client
from views.auth_view import show_auth_page
from views.connect_view import show_connection_manager
from views.query_view import show_query_assistant_panel

st.set_page_config(
    page_title="SchemaSay",
    layout="wide"
)

st.title("SchemaSay")
st.subheader("Your AI-Powered SQL Analytics Platform")

st.write("---")

# Verify user session status
if "token" not in st.session_state:
    show_auth_page()
else:
    token = st.session_state["token"]
    
    # Query backend user profile
    with st.spinner("Verifying secure session..."):
        response = api_client.get_me(token)
    
    if response.status_code == 200:
        # Successful validation
        user_data = response.json()
        display_name = user_data.get("full_name") or user_data.get("email")
        
        # Configure Sidebar Navigation Panel
        st.sidebar.title("SchemaSay")
        st.sidebar.write(f"Logged in as: **{display_name}**")
        st.sidebar.markdown("---")
        
        page = st.sidebar.radio(
            "Navigation Menu",
            options=["Query Assistant", "Database Connections"]
        )
        
        st.sidebar.markdown("---")
        
        # Active Database Source Selector
        st.sidebar.write("### Database Source")
        conn_response = api_client.get_connections(token)
        if conn_response.status_code == 200:
            connections = conn_response.json()
            if not connections:
                st.sidebar.info("No databases connected yet. Go to 'Database Connections' to add one.")
                st.session_state["active_connection_id"] = None
            else:
                conn_options = {c["id"]: f"{c['name']} ({c['db_type'].upper()})" for c in connections}
                conn_ids = list(conn_options.keys())
                
                # Check if session state holds a valid active connection, default to first item
                current_active = st.session_state.get("active_connection_id")
                default_idx = conn_ids.index(current_active) if current_active in conn_ids else 0
                
                selected_id = st.sidebar.selectbox(
                    "Active Source",
                    options=conn_ids,
                    format_func=lambda x: conn_options[x],
                    index=default_idx
                )
                st.session_state["active_connection_id"] = selected_id
                
                # Force resync schemas
                if st.sidebar.button("Sync Schema", key="sync_schema_sidebar_btn"):
                    with st.spinner("Reflecting database schema..."):
                        sync_res = api_client.sync_schema(token, selected_id)
                    if sync_res.status_code == 200:
                        st.sidebar.success("Schema synchronized successfully!")
                        st.rerun()
                    else:
                        st.sidebar.error("Failed to sync schema.")
                
                # Render Schema Explorer tree
                st.sidebar.write("#### Schema Explorer")
                schema_response = api_client.get_schema(token, selected_id)
                if schema_response.status_code == 200:
                    schema_cache = schema_response.json()
                    if not schema_cache:
                        st.sidebar.warning("Schema cache empty. Click 'Sync Schema' to reflect tables.")
                    else:
                        # Group columns by table name
                        tables_map = {}
                        for col in schema_cache:
                            t_name = col["table_name"]
                            if t_name not in tables_map:
                                tables_map[t_name] = []
                            tables_map[t_name].append(f"{col['column_name']} ({col['data_type']})")
                        
                        # Render each table in a collapsible expander
                        for t_name, cols in tables_map.items():
                            with st.sidebar.expander(f"Table: {t_name}"):
                                for c_desc in cols:
                                    st.write(f"- {c_desc}")
                else:
                    st.sidebar.error("Failed to load schema cache.")
        else:
            st.sidebar.error("Failed to load connections.")
            
        st.sidebar.markdown("---")
        # Logout handles local state and issues backend revocation
        if st.sidebar.button("Log Out"):
            with st.spinner("Logging out..."):
                api_client.logout(token)
            st.session_state.pop("token", None)
            st.session_state.pop("refresh_token", None)
            st.success("Session terminated.")
            st.rerun()

        # Render corresponding page based on active page selection
        if page == "Database Connections":
            show_connection_manager()
        else:
            show_query_assistant_panel()
            
    elif response.status_code == 401 and "refresh_token" in st.session_state:
        # Access token expired, attempt to rotate credentials using refresh token
        with st.spinner("Session expired. Attempting secure renewal..."):
            refresh_response = api_client.refresh(st.session_state["refresh_token"])
            
        if refresh_response.status_code == 200:
            res_data = refresh_response.json()
            st.session_state["token"] = res_data["access_token"]
            st.session_state["refresh_token"] = res_data["refresh_token"]
            st.rerun()
        else:
            # Session expired and cannot be renewed
            st.session_state.pop("token", None)
            st.session_state.pop("refresh_token", None)
            st.error("Session has expired. Please log in again.")
            st.rerun()
    else:
        # Any other error, clear credentials
        st.session_state.pop("token", None)
        st.session_state.pop("refresh_token", None)
        st.error("Authentication check failed. Please log in again.")
        st.rerun()
