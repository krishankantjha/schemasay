import streamlit as st
from api_client import api_client
from state import (
    KEY_ACTIVE_CONNECTION_ID, KEY_WORKBENCH_SQL, KEY_QUERY_HISTORY,
    KEY_ACTIVE_TAB, KEY_HISTORY_PAGE, KEY_TOKEN, KEY_REFRESH_TOKEN, clear_session_state
)
from utils.caching import get_cached_connections, get_cached_schema

def render_sidebar_view() -> str:
    """
    Renders the unified, clean sidebar panel.
    Handles connection selections, auto introspection triggers, searchable schema
    explorers with column counts, and paginated query histories.
    """
    token = st.session_state.get(KEY_TOKEN)
    if not token:
        return "Query Assistant"

    # Fetch user profile
    with st.spinner("Checking profile..."):
        user_res = api_client.get_me(token)
    
    display_name = "User"
    if user_res.status_code == 200:
        user_data = user_res.json()
        display_name = user_data.get("full_name") or user_data.get("email")

    st.sidebar.title("SchemaSay")
    st.sidebar.write(f"Logged in as: **{display_name}**")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation Menu",
        options=["Query Assistant", "Database Connections"]
    )

    st.sidebar.markdown("---")

    # Active Connection Configuration Selector
    st.sidebar.write("### Database Source")
    connections = get_cached_connections(token)
    
    if connections is None:
        st.sidebar.error("Failed to load databases.")
        return page

    if not connections:
        st.sidebar.info("No databases connected yet. Go to 'Database Connections' to add one.")
        st.session_state[KEY_ACTIVE_CONNECTION_ID] = None
        return page

    conn_options = {c["id"]: f"{c['name']} ({c['db_type'].upper()})" for c in connections}
    conn_ids = list(conn_options.keys())

    # Selected ID selector
    current_active = st.session_state.get(KEY_ACTIVE_CONNECTION_ID)
    default_idx = conn_ids.index(current_active) if current_active in conn_ids else 0

    selected_id = st.sidebar.selectbox(
        "Active Source",
        options=conn_ids,
        format_func=lambda x: conn_options[x],
        index=default_idx
    )

    if st.session_state.get(KEY_ACTIVE_CONNECTION_ID) != selected_id:
        st.session_state[KEY_ACTIVE_CONNECTION_ID] = selected_id
        # Reset query history when the active connection changes
        st.session_state.pop(KEY_QUERY_HISTORY, None)
        st.session_state[KEY_HISTORY_PAGE] = 1

    # Force reflection schema updates
    if st.sidebar.button("Sync Schema", key="sync_schema_sidebar_btn"):
        with st.spinner("Reflecting database schema..."):
            sync_res = api_client.sync_schema(token, selected_id)
        if sync_res.status_code == 200:
            st.sidebar.success("Schema synchronized successfully!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.sidebar.error("Failed to sync schema.")

    # 1. Searchable Schema Explorer
    st.sidebar.write("#### Schema Explorer")
    schema_cache = get_cached_schema(token, selected_id)

    if schema_cache is not None:
        if not schema_cache:
            # Guard flag to ensure auto-sync only runs once per session per connection, preventing rerun loops
            sync_flag_key = f"schema_sync_attempted_{selected_id}"
            if not st.session_state.get(sync_flag_key):
                st.session_state[sync_flag_key] = True
                st.sidebar.info("Auto-reflecting database schema...")
                with st.spinner("Introspecting schema..."):
                    sync_res = api_client.sync_schema(token, selected_id)
                if sync_res.status_code == 200:
                    st.sidebar.success("Schema synchronized successfully!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.sidebar.warning("Schema cache empty. Synchronize schema manually.")
            else:
                st.sidebar.warning("Schema cache empty. Synchronize schema manually.")
        else:
            schema_search = st.sidebar.text_input("Search tables/columns", key="schema_search_input", placeholder="Filter...").strip().lower()

            tables_map = {}
            for col in schema_cache:
                t_name = col["table_name"]
                if t_name not in tables_map:
                    tables_map[t_name] = []
                tables_map[t_name].append(f"{col['column_name']} ({col['data_type']})")

            matching_tables = {}
            for t_name, cols in tables_map.items():
                # Matches if search is empty, or table name matches, or column name matches
                t_match = not schema_search or schema_search in t_name.lower()
                filtered_cols = [c for c in cols if not schema_search or schema_search in c.lower()]
                
                if t_match or filtered_cols:
                    matching_tables[t_name] = cols if t_match else filtered_cols

            if not matching_tables:
                st.sidebar.info("No matching tables or columns found.")
            else:
                for t_name, cols in matching_tables.items():
                    col_count = len(cols)
                    with st.sidebar.expander(f"Table: {t_name} ({col_count} cols)"):
                        for c_desc in cols:
                            st.write(f"- {c_desc}")
    else:
        st.sidebar.error("Failed to load schema cache.")

    # 2. Paginated Sidebar History
    st.sidebar.markdown("---")
    st.sidebar.write("#### Query History")
    
    current_page = st.session_state.get(KEY_HISTORY_PAGE, 1)
    limit = 5
    
    hist_res = api_client.get_query_history(token, page=current_page, limit=limit, connection_id=selected_id)
    if hist_res.status_code == 200:
        hist_logs = hist_res.json()
        if not hist_logs:
            st.sidebar.info("No query logs on this page.")
        else:
            for idx, log in enumerate(hist_logs):
                q_text = log.get("question") or ""
                if q_text == "Manual SQL Editor Query" or not q_text.strip():
                    q_preview = f"SQL: {log.get('sql_query')[:20]}..."
                else:
                    q_preview = q_text[:25] + "..." if len(q_text) > 25 else q_text

                hist_btn_key = f"sidebar_hist_btn_{log['id']}_{idx}"
                current_sql = st.session_state.get(KEY_WORKBENCH_SQL, "")

                # Warn user if overwriting custom edits
                has_custom_sql = (
                    current_sql.strip()
                    and current_sql != "SELECT * FROM <table_name> LIMIT 10"
                    and current_sql != log.get("sql_query")
                )

                if has_custom_sql:
                    st.sidebar.write(f"*{q_preview}*")
                    confirm_overwrite = st.sidebar.checkbox("Confirm Overwrite", key=f"overwrite_chk_{log['id']}_{idx}")
                    if st.sidebar.button("Restore Query", key=hist_btn_key):
                        if confirm_overwrite:
                            st.session_state[KEY_WORKBENCH_SQL] = log.get("sql_query")
                            st.session_state["workbench_sql_text_area"] = log.get("sql_query")
                            # If manual query, restore to Workbench tab, otherwise Copilot tab
                            st.session_state[KEY_ACTIVE_TAB] = "SQL Workbench" if q_text == "Manual SQL Editor Query" or not q_text.strip() else "AI Copilot"
                            st.sidebar.success("Query restored!")
                            st.rerun()
                        else:
                            st.sidebar.warning("Confirmation check required.")
                else:
                    if st.sidebar.button(q_preview, key=hist_btn_key):
                        st.session_state[KEY_WORKBENCH_SQL] = log.get("sql_query")
                        st.session_state["workbench_sql_text_area"] = log.get("sql_query")
                        st.session_state[KEY_ACTIVE_TAB] = "SQL Workbench" if q_text == "Manual SQL Editor Query" or not q_text.strip() else "AI Copilot"
                        st.sidebar.success("Query restored!")
                        st.rerun()

            # Pagination control buttons layout
            st.sidebar.write("")
            col_prev, col_num, col_next = st.sidebar.columns([2, 2, 2])
            
            with col_prev:
                if current_page > 1:
                    if st.button("« Prev", key="history_prev_page_btn"):
                        st.session_state[KEY_HISTORY_PAGE] = current_page - 1
                        st.rerun()
            with col_num:
                st.write(f"Page {current_page}")
            with col_next:
                # Show "Next" only if a full page was returned, indicating more records likely exist
                if len(hist_logs) == limit:
                    if st.button("Next »", key="history_next_page_btn"):
                        st.session_state[KEY_HISTORY_PAGE] = current_page + 1
                        st.rerun()
    else:
        st.sidebar.error("Failed to load query logs.")

    st.sidebar.markdown("---")
    
    # Log out
    if st.sidebar.button("Log Out"):
        with st.spinner("Logging out..."):
            api_client.logout(token)
        clear_session_state()
        st.cache_data.clear()
        st.success("Session terminated.")
        st.rerun()

    return page
