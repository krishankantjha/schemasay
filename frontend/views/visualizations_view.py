"""
SchemaSay Views — Visualizations View

Renders dynamic charts, diagrams, and metrics plots using placeholder datasets.
"""

import streamlit as st
import pandas as pd
import numpy as np

def show_visualizations_view():
    """Renders the graphical reporting visualization dashboard widgets."""
    with st.container(border=True):
        st.write("### Graphical Reporting & Analytics")
        st.write("Construct interactive visualizations dynamically matching output datasets.")
        st.markdown("---")

        # 1. Config selection row
        col_source, col_x, col_y = st.columns(3)
        with col_source:
            st.selectbox("Data Source", options=["Sales metrics summary (Q1)", "Users demographics"])
        with col_x:
            st.selectbox("X-Axis Field", options=["sale_date", "region", "product_id"])
        with col_y:
            st.selectbox("Y-Axis Field", options=["total_revenue", "quantity", "price"])

        # 2. Charts rows
        st.write("")
        chart_col1, chart_col2 = st.columns(2)
        
        # Prepare mock pandas dataframe
        dates = pd.date_range(start="2026-07-01", periods=10)
        revenue = [1200, 1500, 1100, 1800, 2200, 1900, 2400, 2600, 2100, 2800]
        units = [40, 52, 38, 60, 75, 63, 80, 88, 70, 95]
        
        df = pd.DataFrame({"Date": dates, "Revenue ($)": revenue, "Units Sold": units})
        
        with chart_col1:
            with st.container(border=True):
                st.write("##### Total Revenue Over Time (Line Chart)")
                st.line_chart(df, x="Date", y="Revenue ($)")
                
        with chart_col2:
            with st.container(border=True):
                st.write("##### Units Sold per Day (Bar Chart)")
                st.bar_chart(df, x="Date", y="Units Sold")

        st.write("")
        chart_col3, chart_col4 = st.columns(2)
        
        with chart_col3:
            with st.container(border=True):
                st.write("##### Regional Revenue Allocation (Pie/Area Chart)")
                region_df = pd.DataFrame({
                    "Region": ["North", "South", "East", "West"],
                    "Revenue": [45000, 32000, 58000, 49000]
                })
                # Area chart fallback for Streamlit native charts
                st.area_chart(region_df, x="Region", y="Revenue")
                
        with chart_col4:
            with st.container(border=True):
                st.write("##### Quantity vs Price Correlation (Scatter Plot)")
                scatter_df = pd.DataFrame({
                    "Price": [10.0, 15.5, 20.0, 35.0, 49.9, 89.9, 120.0, 150.0],
                    "Quantity Sold": [150, 120, 95, 80, 65, 40, 30, 15]
                })
                st.scatter_chart(scatter_df, x="Price", y="Quantity Sold")
