import streamlit as st
from api_client import api_client
from components.chart_renderer import render_chart
from utils.error_handler import parse_api_response
from state import (
    KEY_TOKEN, KEY_ACTIVE_CONNECTION_ID, KEY_WORKBENCH_SQL,
    KEY_QUERY_HISTORY, KEY_ACTIVE_TAB
)

def show_query_assistant_panel():
    """
    Renders the Query Assistant panel with conversational AI Copilot and SQL Workbench.
    Enforces state persistence and automatic tab switching when restoring or editing queries.
    """
    token = st.session_state.get(KEY_TOKEN)
    active_conn_id = st.session_state.get(KEY_ACTIVE_CONNECTION_ID)

    if not token:
        st.warning("Please log in to use the Query Assistant.")
        return

    if not active_conn_id:
        # Friendly empty state for missing connection
        st.info("Select an active database connection source from the sidebar menu to begin querying your data.")
        return

    st.write("### Query Assistant")

    # Centralized tab control segmented navigation
    view_mode = st.radio(
        "Workspace Navigation",
        options=["AI Copilot", "SQL Workbench"],
        key=KEY_ACTIVE_TAB,
        horizontal=True
    )

    st.write("---")

    # ----------------------------------------------------
    # VIEW: AI COPILOT
    # ----------------------------------------------------
    if view_mode == "AI Copilot":
        st.write("##### AI Conversational Search")
        st.write("Ask questions in plain English to automatically generate and execute SQL queries on your database.")

        # Load cached query history
        history_logs = st.session_state.get(KEY_QUERY_HISTORY, [])
        filtered_history_logs = [
            log for log in history_logs
            if log.get("connection_id") == active_conn_id and log.get("question") != "Manual SQL Editor Query"
        ]

        if not filtered_history_logs:
            st.info("Ask your first question using the chat input box below.")
        else:
            # Display query audit log history in chat format
            for log in reversed(filtered_history_logs):
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
                data = parse_api_response(response, "query AI assistant")
                if data:
                    generated_sql = data["sql"]
                    st.session_state[KEY_WORKBENCH_SQL] = generated_sql
                    
                    st.write("Generated SQL:")
                    st.code(generated_sql, language="sql")

                    if data["success"]:
                        st.success(f"Success | Returned {len(data['results'])} rows in {data['execution_duration_ms']:.1f}ms")
                        results = data.get("results") or []
                        columns = list(results[0].keys()) if results else []
                        chart_config = data.get("chart_config") or {}
                        
                        if not results:
                            st.info("No records were returned by this query on the database.")
                        else:
                            render_chart(columns, results, chart_config)
                        
                        # Fetch and render AI business intelligence narrative insights
                        with st.spinner("AI is interpreting results and drafting business insights..."):
                            insight_payload = {
                                "question": user_question,
                                "sql_query": generated_sql,
                                "columns": columns,
                                "rows": results
                            }
                            insight_res = api_client.generate_insight(token, insight_payload)
                            
                            insight_data = parse_api_response(insight_res, "generate AI insights")
                            if insight_data and insight_data.get("success"):
                                insight_text = insight_data["insight"]
                                from components.insight_card import render_insight_card
                                render_insight_card(insight_text)
                    else:
                        st.error(f"Failed | Error: {data['error']}")

            # Invalidate query history session cache
            st.session_state.pop(KEY_QUERY_HISTORY, None)
            st.rerun()

        # Render Edit in SQL Workbench shortcut button
        last_generated_sql = st.session_state.get(KEY_WORKBENCH_SQL)
        if last_generated_sql and last_generated_sql != "SELECT * FROM <table_name> LIMIT 10":
            st.markdown("---")
            if st.button("Edit Last Query in SQL Workbench", key="edit_in_workbench_shortcut_btn"):
                st.session_state["workbench_sql_text_area"] = last_generated_sql
                # Switch tab to SQL Workbench automatically
                st.session_state[KEY_ACTIVE_TAB] = "SQL Workbench"
                st.rerun()

    # ----------------------------------------------------
    # VIEW: SQL WORKBENCH
    # ----------------------------------------------------
    else:
        st.write("##### SQL Sandbox Workbench")
        st.write("Write and execute manual SQL queries. Crucial mutating queries are automatically blocked.")

        default_sql = st.session_state.get(KEY_WORKBENCH_SQL, "SELECT * FROM <table_name> LIMIT 10")
        
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

                data = parse_api_response(response, "execute raw SQL query")
                if data:
                    rows = data.get("rows") or []
                    duration = data.get("execution_time_ms") or 0.0
                    columns = data.get("columns") or []
                    chart_config = data.get("chart_config") or {}
                    
                    st.success(f"Success | Returned {len(rows)} rows in {duration:.1f}ms")
                    
                    if not rows:
                        st.info("No records were returned by this query on the database.")
                    else:
                        render_chart(columns, rows, chart_config)
                    
                    st.session_state[KEY_WORKBENCH_SQL] = sql_input
                    # Invalidate history cache
                    st.session_state.pop(KEY_QUERY_HISTORY, None)
