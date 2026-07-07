import streamlit as st
import pandas as pd
from api_client import api_client

def show_query_assistant_panel():
    """
    Renders the tabbed Query Assistant panel in the Streamlit main screen.
    Includes the conversational AI Copilot and the manual SQL Workbench.
    """
    token = st.session_state.get("token")
    active_conn_id = st.session_state.get("active_connection_id")

    if not token:
        st.warning("Please log in to use the Query Assistant.")
        return

    if not active_conn_id:
        st.info("Select an active database connection source from the sidebar menu to begin querying your data.")
        return

    # Render workspace header
    st.write(f"### Query Assistant")
    
    # 1. Initialize active tabs
    tab_copilot, tab_workbench = st.tabs(["AI Copilot", "SQL Workbench"])

    # ----------------------------------------------------
    # TAB 1: AI COPILOT
    # ----------------------------------------------------
    with tab_copilot:
        st.write("##### AI Conversational Search")
        st.write("Ask questions in plain English to automatically generate and execute SQL queries on your database.")

        # Query and load query history (page 1, limit 50) from the backend database to initialize history
        history_response = api_client.get_query_history(token, page=1, limit=50)
        history_logs = []
        if history_response.status_code == 200:
            all_logs = history_response.json()
            # Filter logs specific to the active connection, excluding raw workbench statements
            history_logs = [
                log for log in all_logs
                if log.get("connection_id") == active_conn_id and log.get("question") != "Manual SQL Editor Query"
            ]

        # Display query audit log history in chat format (oldest first at top, newest at bottom)
        for log in reversed(history_logs):
            with st.chat_message("user"):
                st.write(log["question"])
            with st.chat_message("assistant"):
                st.write("Generated SQL:")
                st.code(log["sql_query"], language="sql")
                if log["status"] == "success":
                    st.success(f"Success | Returned in {log['execution_duration_ms']}ms")
                else:
                    st.error(f"Failed | Error: {log['error_message']}")

        # Input box for capturing new natural language queries
        user_question = st.chat_input("Ask a question about your database...", key="copilot_chat_input")
        if user_question:
            # Render user message
            with st.chat_message("user"):
                st.write(user_question)

            # Send payload request to backend
            with st.spinner("AI is analyzing schema and compiling query..."):
                response = api_client.query_assistant(token, active_conn_id, user_question)

            # Render assistant message response
            with st.chat_message("assistant"):
                if response.status_code == 200:
                    data = response.json()
                    generated_sql = data["sql"]
                    
                    # Store generated SQL in session state so it pre-populates the SQL Workbench tab
                    st.session_state["workbench_sql_input"] = generated_sql
                    
                    st.write("Generated SQL:")
                    st.code(generated_sql, language="sql")

                    if data["success"]:
                        st.success(f"Success | Returned {len(data['results'])} rows in {data['execution_duration_ms']:.1f}ms")
                        df = pd.DataFrame(data["results"])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error(f"Failed | Error: {data['error']}")
                else:
                    # Capture and display detailed error message from backend HTTPException
                    try:
                        error_detail = response.json().get("detail", "An unexpected error occurred.")
                        st.error(f"Failed | Error: {error_detail}")
                    except Exception:
                        st.error("Failed to query the AI assistant. Verify API settings.")

    # ----------------------------------------------------
    # TAB 2: SQL WORKBENCH
    # ----------------------------------------------------
    with tab_workbench:
        st.write("##### SQL Sandbox Workbench")
        st.write("Write and execute manual SQL queries. Crucial mutating queries are automatically blocked.")

        # Pre-populate workspace editor with the last query generated in the AI tab
        default_sql = st.session_state.get("workbench_sql_input", "SELECT * FROM <table_name> LIMIT 10")
        
        # SQL Editor Text Area
        sql_input = st.text_area(
            "SQL Query Editor",
            value=default_sql,
            height=180,
            key="workbench_sql_text_area"
        )

        if st.button("Run Query", key="run_workbench_query_btn"):
            if not sql_input.strip():
                st.warning("Please enter a SQL query to execute.")
            else:
                with st.spinner("Executing query on target database connection..."):
                    response = api_client.execute_raw_sql(token, active_conn_id, sql_input)

                if response.status_code == 200:
                    data = response.json()
                    
                    if data["success"]:
                        st.success(f"Success | Returned {len(data['results'])} rows in {data['execution_duration_ms']:.1f}ms")
                        df = pd.DataFrame(data["results"])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error(f"Failed | Error: {data['error']}")
                else:
                    # Capture and display detailed error message from backend safety rejections or database drivers
                    try:
                        error_detail = response.json().get("detail", "An unexpected error occurred.")
                        st.error(f"Failed | Error: {error_detail}")
                    except Exception:
                        st.error("Failed to execute raw SQL query. Verify query syntax and database timeouts.")
