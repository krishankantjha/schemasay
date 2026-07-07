import streamlit as st
import plotly.express as px
import pandas as pd
import html
import re
from typing import Dict, Any, List

def sanitize_html(val: Any) -> str:
    """
    Escapes HTML control characters to prevent stored XSS or injections in SVG/HTML renderers.
    """
    if val is None:
        return ""
    return html.escape(str(val))

def format_axis_label(col: str) -> str:
    """
    Formats database column names (like sum_revenue_usd) into clean, human-readable labels (like Sum Revenue (USD)).
    """
    if not col:
        return ""
    # Split by underscore
    parts = str(col).split("_")
    formatted_parts = []
    for part in parts:
        part_lower = part.lower()
        if part_lower in ["usd", "eur", "gbp", "jpy", "cad", "aud", "inr"]:
            formatted_parts.append(f"({part.upper()})")
        elif part_lower in ["id"]:
            formatted_parts.append("ID")
        else:
            formatted_parts.append(part.capitalize())
    label = " ".join(formatted_parts)
    label = re.sub(r"\s+\(([^)]+)\)", r" (\1)", label)
    return label

def render_chart(columns: List[str], rows: List[Dict[str, Any]], chart_config: Any):
    """
    Renders an interactive Plotly chart and a source data table in Streamlit
    incorporating responsive configurations, date aggregation, and axis formatting.
    """
    if not columns or not rows:
        st.info("ℹ️ No records found matching the query criteria. Try adjusting filters or table queries.")
        return

    # Extract configs safely from dict or model instances
    chart_type = chart_config.get("chart_type", "table") if isinstance(chart_config, dict) else getattr(chart_config, "chart_type", "table")
    x_axis = chart_config.get("x_axis") if isinstance(chart_config, dict) else getattr(chart_config, "x_axis", None)
    y_axis = chart_config.get("y_axis") if isinstance(chart_config, dict) else getattr(chart_config, "y_axis", None)
    color_axis = chart_config.get("color_axis") if isinstance(chart_config, dict) else getattr(chart_config, "color_axis", None)

    # Load records into DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Sample dataset if extremely large to prevent browser hang
    if len(df) > 5000:
        df = df.sample(n=5000, random_state=42)
        st.warning("⚠️ Large dataset detected. The visualization displays a representative sample of 5,000 rows to maintain rendering performance.")

    # Sort Line Chart chronologically and aggregate duplicate keys prior to plotting
    if chart_type == "line" and x_axis and x_axis in df.columns:
        try:
            # Parse temporal values cleanly
            sort_series = pd.to_datetime(df[x_axis], errors="coerce")
            if not sort_series.isna().all():
                df["_sort_key"] = sort_series
                df = df.sort_values("_sort_key").drop(columns=["_sort_key"])
        except Exception:
            df = df.sort_values(x_axis)
        
        # Aggregate duplicate dates by summing targets
        if y_axis and y_axis in df.columns:
            try:
                if color_axis and color_axis in df.columns:
                    df = df.groupby([x_axis, color_axis], as_index=False)[y_axis].sum()
                else:
                    df = df.groupby(x_axis, as_index=False)[y_axis].sum()
            except Exception:
                pass

    # Prevent browser freezes from high-cardinality color groupings
    if color_axis and color_axis in df.columns:
        if df[color_axis].dropna().nunique() > 15:
            color_axis = None

    # Sanitize every database column name and rename DataFrame schema
    sanitized_cols = {col: sanitize_html(col) for col in df.columns}
    df = df.rename(columns=sanitized_cols)

    # Sanitize visual layout mappings to match escaped columns
    x_axis = sanitize_html(x_axis) if x_axis else None
    y_axis = sanitize_html(y_axis) if y_axis else None
    color_axis = sanitize_html(color_axis) if color_axis else None

    # Define clean label mappings (fully sanitized and human-readable)
    labels_config = {}
    if x_axis:
        labels_config[x_axis] = format_axis_label(x_axis)
    if y_axis:
        labels_config[y_axis] = format_axis_label(y_axis)

    # Set up multi-tab layout interface
    tab_chart, tab_table = st.tabs(["📊 Interactive Visualization", "📋 Source Data Table"])

    with tab_chart:
        if chart_type == "table" or not x_axis:
            st.info("No matching visual format for this query. Displaying tabular grid.")
            st.dataframe(df, use_container_width=True)
        else:
            try:
                fig = None
                if chart_type == "line":
                    title = f"Line Trend: {format_axis_label(y_axis)} over {format_axis_label(x_axis)}"
                    fig = px.line(
                        df, 
                        x=x_axis, 
                        y=y_axis, 
                        color=color_axis,
                        title=sanitize_html(title),
                        labels=labels_config
                    )
                elif chart_type == "bar":
                    title = f"Bar Comparison: {format_axis_label(y_axis)} by {format_axis_label(x_axis)}"
                    fig = px.bar(
                        df, 
                        x=x_axis, 
                        y=y_axis, 
                        title=sanitize_html(title),
                        labels=labels_config
                    )
                elif chart_type == "scatter":
                    title = f"Scatter Correlation: {format_axis_label(y_axis)} vs {format_axis_label(x_axis)}"
                    fig = px.scatter(
                        df, 
                        x=x_axis, 
                        y=y_axis, 
                        color=color_axis,
                        title=sanitize_html(title),
                        labels=labels_config
                    )
                elif chart_type == "pie":
                    title = f"Proportion Share: {format_axis_label(y_axis)} distribution by {format_axis_label(x_axis)}"
                    fig = px.pie(
                        df, 
                        names=x_axis, 
                        values=y_axis, 
                        title=sanitize_html(title),
                        labels=labels_config
                    )
                elif chart_type == "histogram":
                    title = f"Frequency Distribution: {format_axis_label(x_axis)}"
                    fig = px.histogram(
                        df, 
                        x=x_axis, 
                        title=sanitize_html(title),
                        labels=labels_config
                    )

                if fig:
                    # Enforce premium styling options with responsive config
                    fig.update_layout(
                        margin=dict(l=20, r=20, t=50, b=20),
                        hovermode="x unified" if chart_type != "pie" else None,
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    
                    if chart_type != "pie":
                        fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)")
                        fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)")

                    st.plotly_chart(
                        fig, 
                        use_container_width=True, 
                        config={"responsive": True, "displayModeBar": "hover"}
                    )
                else:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to render Plotly visualization chart: {str(e)}")
                st.dataframe(df, use_container_width=True)

    with tab_table:
        st.dataframe(df, use_container_width=True)
