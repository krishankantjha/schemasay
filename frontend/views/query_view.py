import streamlit as st
import os
import uuid
from api_client import api_client
from components.chart_renderer import render_chart
from utils.error_handler import parse_api_response
from utils.caching import get_cached_schema, get_cached_connections
from state import (
    KEY_TOKEN, KEY_ACTIVE_CONNECTION_ID, KEY_WORKBENCH_SQL,
    KEY_QUERY_HISTORY, KEY_ACTIVE_TAB, KEY_HISTORY_PAGE
)
from components.insight_card import render_insight_card

def show_query_assistant_panel():
    """
    Renders the premium three-column workspace dashboard.
    - Left Column: Schema Explorer tree view card.
    - Center Column: Side-by-side AI Copilot and SQL Workbench panel, with bottom results/visualization tabs.
    - Right Column: Compact query history feed and AI business insights.
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

    # Check query results in session state
    if "last_query_results" not in st.session_state:
        st.session_state["last_query_results"] = None
    if "last_query_columns" not in st.session_state:
        st.session_state["last_query_columns"] = []
    if "last_query_duration" not in st.session_state:
        st.session_state["last_query_duration"] = 0.0
    if "last_query_chart_config" not in st.session_state:
        st.session_state["last_query_chart_config"] = {}
    if "last_query_insight" not in st.session_state:
        st.session_state["last_query_insight"] = ""
    if "last_query_sql" not in st.session_state:
        st.session_state["last_query_sql"] = ""

    # Split dashboard main area into 3 columns
    col_schema, col_workspace, col_context = st.columns([1.2, 3.2, 1.3], gap="medium")

    # ----------------------------------------------------
    # COLUMN 1: SCHEMA EXPLORER
    # ----------------------------------------------------
    with col_schema:
        st.markdown(
            """
            <div class="workspace-card" style="min-height: 80vh;">
                <div style="font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
                    📂 Schema Explorer
                </div>
            """,
            unsafe_allow_html=True
        )
        
        schema_cache = get_cached_schema(token, active_conn_id)
        if schema_cache is not None:
            if not schema_cache:
                st.info("No schema cached. Sync from sidebar.")
            else:
                schema_search = st.text_input(
                    "Search tables/cols",
                    key="workspace_schema_search",
                    placeholder="Search...",
                    label_visibility="collapsed"
                ).strip().lower()

                tables_map = {}
                for col in schema_cache:
                    t_name = col["table_name"]
                    if t_name not in tables_map:
                        tables_map[t_name] = []
                    pk_suffix = " 🔑" if col.get("is_primary_key") else ""
                    tables_map[t_name].append(f"{col['column_name']} ({col['data_type']}){pk_suffix}")

                matching_tables = {}
                for t_name, cols in tables_map.items():
                    t_match = not schema_search or schema_search in t_name.lower()
                    filtered_cols = [c for c in cols if not schema_search or schema_search in c.lower()]
                    if t_match or filtered_cols:
                        matching_tables[t_name] = cols if t_match else filtered_cols

                if not matching_tables:
                    st.info("No matches.")
                else:
                    for t_name, cols in matching_tables.items():
                        col_count = len(cols)
                        with st.expander(f"📁 {t_name} ({col_count})", expanded=False):
                            for c_desc in cols:
                                st.markdown(f"<div style='font-family: monospace; font-size: 11px; color: #64748B; padding: 2px 8px;'># {c_desc}</div>", unsafe_allow_html=True)
        else:
            st.error("Failed to load schema cache.")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # COLUMN 2: WORKSPACE (AI COPILOT & SQL WORKBENCH)
    # ----------------------------------------------------
    with col_workspace:
        w_top1, w_top2 = st.columns([1, 1.1], gap="medium")

        # Top Left Card: AI Copilot
        with w_top1:
            st.markdown(
                """
                <div class="workspace-card" style="min-height: 320px;">
                    <div style="font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        🤖 AI Copilot
                    </div>
                    <div style="font-size: 12px; color: #64748B; margin-bottom: 12px;">
                        Ask questions in plain English to generate SQL automatically.
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            copilot_question = st.text_input(
                "Ask plain English question",
                placeholder="e.g. Show total sales per month...",
                key="workspace_copilot_prompt",
                label_visibility="collapsed"
            )
            
            st.write("")
            if st.button("Generate SQL ✨", key="workspace_generate_sql_btn", use_container_width=True):
                if not copilot_question.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("AI is analyzing schema and compiling query..."):
                        response = api_client.query_assistant(token, active_conn_id, copilot_question)
                    
                    data = parse_api_response(response, "query AI assistant")
                    if data:
                        generated_sql = data["sql"]
                        st.session_state[KEY_WORKBENCH_SQL] = generated_sql
                        
                        # Save results to session state immediately
                        st.session_state["last_query_results"] = data.get("results") or []
                        st.session_state["last_query_columns"] = list(data["results"][0].keys()) if data.get("results") else []
                        st.session_state["last_query_duration"] = data.get("execution_duration_ms") or 0.0
                        st.session_state["last_query_chart_config"] = data.get("chart_config") or {}
                        st.session_state["last_query_sql"] = generated_sql
                        
                        # Generate insights automatically
                        if data.get("results"):
                            with st.spinner("Interpreting insights..."):
                                insight_payload = {
                                    "question": copilot_question,
                                    "sql_query": generated_sql,
                                    "columns": st.session_state["last_query_columns"],
                                    "rows": st.session_state["last_query_results"]
                                }
                                insight_res = api_client.generate_insight(token, insight_payload)
                                insight_data = parse_api_response(insight_res, "generate AI insights")
                                if insight_data and insight_data.get("success"):
                                    st.session_state["last_query_insight"] = insight_data["insight"]
                        
                        # Invalidate history session cache to load new records
                        st.session_state.pop(KEY_QUERY_HISTORY, None)
                        st.success("Query compiled & executed!")
                        st.rerun()

            # Display last generated SQL statement
            if st.session_state.get(KEY_WORKBENCH_SQL):
                st.markdown("<div style='margin-top: 10px; font-size: 11px; font-weight: 600; color: #64748B;'>Generated SQL:</div>", unsafe_allow_html=True)
                st.code(st.session_state[KEY_WORKBENCH_SQL], language="sql")
            
            st.markdown("</div>", unsafe_allow_html=True)

        # Top Right Card: SQL Workbench
        with w_top2:
            st.markdown(
                """
                <div class="workspace-card" style="min-height: 320px;">
                    <div style="font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        💻 SQL Workbench
                    </div>
                    <div style="font-size: 12px; color: #64748B; margin-bottom: 12px;">
                        Write and execute manual SQL statements directly.
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            default_sql = st.session_state.get(KEY_WORKBENCH_SQL, "SELECT * FROM <table_name> LIMIT 10")
            
            sql_input = st.text_area(
                "SQL Workbench Editor Input",
                value=default_sql,
                height=150,
                key="workbench_sql_text_area",
                label_visibility="collapsed"
            )
            
            col_actions1, col_actions2 = st.columns([1, 1.2])
            with col_actions1:
                if st.button("Format SQL 🛠️", key="workspace_format_sql_btn", use_container_width=True):
                    with st.spinner("Formatting..."):
                        format_res = api_client.format_sql(token, sql_input)
                    if format_res.status_code == 200:
                        formatted_sql = format_res.json()["formatted_sql"]
                        st.session_state[KEY_WORKBENCH_SQL] = formatted_sql
                        st.session_state["workbench_sql_text_area"] = formatted_sql
                        st.rerun()
                    else:
                        st.error("Failed to format SQL.")

            with col_actions2:
                if st.button("Run Query ▶️", key="workspace_run_query_btn", use_container_width=True):
                    if not sql_input.strip():
                        st.warning("Please enter SQL.")
                    else:
                        with st.spinner("Executing query on target database connection..."):
                            response = api_client.execute_raw_sql(token, active_conn_id, sql_input)
                        
                        data = parse_api_response(response, "execute raw SQL query")
                        if data:
                            results = data.get("rows") or []
                            columns = data.get("columns") or []
                            duration = data.get("execution_time_ms") or 0.0
                            chart_config = data.get("chart_config") or {}
                            
                            st.session_state["last_query_results"] = results
                            st.session_state["last_query_columns"] = columns
                            st.session_state["last_query_duration"] = duration
                            st.session_state["last_query_chart_config"] = chart_config
                            st.session_state["last_query_sql"] = sql_input
                            st.session_state["last_query_insight"] = ""
                            
                            st.session_state[KEY_WORKBENCH_SQL] = sql_input
                            
                            # Generate AI insights automatically for manual raw runs as well
                            if results:
                                with st.spinner("Analyzing data anomalies..."):
                                    insight_payload = {
                                        "question": "Manual SQL Editor Query",
                                        "sql_query": sql_input,
                                        "columns": columns,
                                        "rows": results
                                    }
                                    insight_res = api_client.generate_insight(token, insight_payload)
                                    insight_data = parse_api_response(insight_res, "generate AI insights")
                                    if insight_data and insight_data.get("success"):
                                        st.session_state["last_query_insight"] = insight_data["insight"]

                            # Invalidate history cache
                            st.session_state.pop(KEY_QUERY_HISTORY, None)
                            st.success("Query completed successfully!")
                            st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        # Bottom Area: Multi-tab Results Grid & Charts
        st.write("")
        st.markdown(
            """
            <div class="workspace-card" style="min-height: 400px;">
                <div style="font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
                    📊 Workspace Canvas
                </div>
            """,
            unsafe_allow_html=True
        )

        results = st.session_state.get("last_query_results")
        columns = st.session_state.get("last_query_columns", [])
        duration = st.session_state.get("last_query_duration", 0.0)
        chart_config = st.session_state.get("last_query_chart_config", {})
        insight_text = st.session_state.get("last_query_insight", "")

        if results is None:
            st.info("Execute a query or generate SQL via the Copilot to inspect tabular rows, Plotly charts, and business insights.")
        else:
            # Metric indicators
            st.markdown(
                f"""
                <div class="kpi-row">
                    <div class="kpi-card">
                        <p class="kpi-title">Total Records</p>
                        <p class="kpi-value">{len(results):,}</p>
                    </div>
                    <div class="kpi-card">
                        <p class="kpi-title">Columns Count</p>
                        <p class="kpi-value">{len(columns)}</p>
                    </div>
                    <div class="kpi-card">
                        <p class="kpi-title">Runtime Duration</p>
                        <p class="kpi-value">{duration:.1f} ms</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Segmented tabs layout
            tab_data, tab_charts, tab_text = st.tabs(["📋 Source Data", "📊 Visualizations", "💡 Narrative Insights"])
            
            with tab_data:
                if not results:
                    st.info("Empty database response dataset.")
                else:
                    # Render searchable, sortable Streamlit dataframe
                    st.dataframe(results, use_container_width=True)

            with tab_charts:
                if not results:
                    st.info("No chart records available.")
                else:
                    render_chart(columns, results, chart_config)

            with tab_text:
                if not insight_text:
                    st.info("No insights compiled. Execute an AI query or valid statement.")
                else:
                    render_insight_card(insight_text)

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # COLUMN 3: CONTEXT PANELS (HISTORY & INSIGHTS CARD)
    # ----------------------------------------------------
    with col_context:
        # Card 1: Compact Paginated History list
        st.markdown(
            """
            <div class="workspace-card" style="min-height: 380px;">
                <div style="font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    📝 Query History
                </div>
            """,
            unsafe_allow_html=True
        )

        current_page = st.session_state.get(KEY_HISTORY_PAGE, 1)
        limit = 5
        
        hist_res = api_client.get_query_history(token, page=current_page, limit=limit, connection_id=active_conn_id)
        if hist_res.status_code == 200:
            hist_logs = hist_res.json()
            if not hist_logs:
                st.info("No query logs.")
            else:
                for idx, log in enumerate(hist_logs):
                    q_text = log.get("question") or ""
                    if q_text == "Manual SQL Editor Query" or not q_text.strip():
                        q_preview = f"SQL: {log.get('sql_query')[:22]}..."
                    else:
                        q_preview = q_text[:22] + "..." if len(q_text) > 22 else q_text

                    hist_btn_key = f"workspace_hist_btn_{log['id']}_{idx}"
                    current_sql = st.session_state.get(KEY_WORKBENCH_SQL, "")

                    has_custom_sql = (
                        current_sql.strip()
                        and current_sql != "SELECT * FROM <table_name> LIMIT 10"
                        and current_sql != log.get("sql_query")
                    )

                    st.markdown(f"<div style='font-size: 11px; font-weight: 500; color: #0F172A; margin-top: 8px; margin-bottom: 2px;'>{q_preview}</div>", unsafe_allow_html=True)
                    
                    if has_custom_sql:
                        confirm_overwrite = st.checkbox("Confirm Overwrite", key=f"overwrite_chk_workspace_{log['id']}_{idx}")
                        if st.button("Restore", key=hist_btn_key, use_container_width=True):
                            if confirm_overwrite:
                                st.session_state[KEY_WORKBENCH_SQL] = log.get("sql_query")
                                st.session_state["workbench_sql_text_area"] = log.get("sql_query")
                                st.session_state[KEY_ACTIVE_TAB] = "SQL Workbench" if q_text == "Manual SQL Editor Query" or not q_text.strip() else "AI Copilot"
                                st.success("Restored!")
                                st.rerun()
                            else:
                                st.warning("Check box.")
                    else:
                        if st.button("Restore Query", key=hist_btn_key, use_container_width=True):
                            st.session_state[KEY_WORKBENCH_SQL] = log.get("sql_query")
                            st.session_state["workbench_sql_text_area"] = log.get("sql_query")
                            st.session_state[KEY_ACTIVE_TAB] = "SQL Workbench" if q_text == "Manual SQL Editor Query" or not q_text.strip() else "AI Copilot"
                            st.success("Restored!")
                            st.rerun()

                # Small pagination arrows layout
                st.write("")
                col_p, col_n = st.columns([1, 1])
                with col_p:
                    if current_page > 1:
                        if st.button("« Prev", key="workspace_history_prev_btn", use_container_width=True):
                            st.session_state[KEY_HISTORY_PAGE] = current_page - 1
                            st.rerun()
                with col_n:
                    if len(hist_logs) == limit:
                        if st.button("Next »", key="workspace_history_next_btn", use_container_width=True):
                            st.session_state[KEY_HISTORY_PAGE] = current_page + 1
                            st.rerun()
        else:
            st.error("Failed to load logs.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Card 2: AI Business Insights narrative summary block
        st.markdown(
            """
            <div class="workspace-card" style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.03) 0%, rgba(29, 78, 216, 0.05) 100%); border-color: rgba(37, 99, 235, 0.15); min-height: 280px;">
                <div style="font-size: 14px; font-weight: 700; color: #2563EB; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    💡 Insights Summary
                </div>
            """,
            unsafe_allow_html=True
        )
        
        if insight_text:
            st.markdown(
                f"""
                <p style="font-size: 12px; line-height: 1.5; color: #475569; margin: 0; font-family: sans-serif; white-space: pre-wrap;">
                    {insight_text[:300]}...
                </p>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <p style="font-size: 12px; line-height: 1.5; color: #94A3B8; margin: 0; font-style: italic;">
                    No query insights generated. Run a statement or query in the center workspace panel to load statistical anomalies logs.
                </p>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
