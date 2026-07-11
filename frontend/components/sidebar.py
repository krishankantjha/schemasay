"""
SchemaSay Components — Left Navigation Sidebar

Modular sidebar rendering class returning high-fidelity HTML structures
and vector icons matching our design tokens.
Now fully dynamic, supporting clickable Quick Tip pagination rotation.
"""

import streamlit as st

# Reusable list of platform tips
TIPS = [
    "Use natural language in SchemaSay AI to generate complex SQL queries instantly.",
    "Select your database connection source from the top navbar to start browsing tables.",
    "Click Format SQL in the Workbench to clean up raw SQL queries automatically.",
    "Save your favorite SQL queries to access them quickly from your Query History."
]

def render_sidebar(active_tip: int = 0) -> str:
    """
    Renders the unified sidebar, including:
      - Logo Section (Brand + Hamburger link trigger)
      - Primary Navigation Menu (Dashboard active, others inactive)
      - Dividers
      - Secondary Navigation Menu (Settings, Help)
      - Logout CTA button
      - Bottom Quick Tip Container Card with indicators
    """
    # Collapse state toggle check
    is_collapsed = st.session_state.get("sidebar_collapsed", False)
    collapsed_class = "collapsed" if is_collapsed else ""
    
    # Active navigation page state checks
    active_page = st.session_state.get("selected_sidebar_item", "dashboard")

    from components.icons import (
        LOGO_SVG, HAMBURGER_SVG, DASHBOARD_SVG, CONNECTIONS_SVG, UPLOAD_SVG,
        SCHEMA_SVG, COPILOT_SVG, WORKBENCH_SVG, HISTORY_SVG, VISUALIZATIONS_SVG,
        RESULTS_SVG, INSIGHTS_SVG, SETTINGS_SVG, HELP_SVG, LOGOUT_SVG, LIGHTBULB_SVG
    )
    logo_svg = LOGO_SVG
    hamburger_svg = HAMBURGER_SVG
    dashboard_svg = DASHBOARD_SVG
    connections_svg = CONNECTIONS_SVG
    upload_svg = UPLOAD_SVG
    schema_svg = SCHEMA_SVG
    copilot_svg = COPILOT_SVG
    workbench_svg = WORKBENCH_SVG
    history_svg = HISTORY_SVG
    visualizations_svg = VISUALIZATIONS_SVG
    results_svg = RESULTS_SVG
    insights_svg = INSIGHTS_SVG
    settings_svg = SETTINGS_SVG
    help_svg = HELP_SVG
    logout_svg = LOGOUT_SVG
    lightbulb_svg = LIGHTBULB_SVG

    # Normalize active index
    tip_count = len(TIPS)
    active_idx = active_tip % tip_count
    tip_text = TIPS[active_idx]
    
    # Calculate next slide target
    next_idx = (active_idx + 1) % tip_count
    
    # Generate pagination dots HTML
    dots_html = ""
    for i in range(tip_count):
        active_class = "active" if i == active_idx else ""
        dots_html += f'<a class="pagination-dot {active_class}" href="?action=tip_{i}" target="_self"></a>'

    sidebar_html = f"""
    <div class="sidebar-inner {collapsed_class}">
        <!-- Logo Section -->
        <div class="sidebar-logo-container">
            <a href="?action=nav_dashboard" class="sidebar-logo-brand" target="_self">
                {logo_svg}
                <span class="sidebar-logo-text">Schema<span class="sidebar-logo-accent">Say</span></span>
            </a>
            <a href="?action=toggle_sidebar" class="sidebar-menu-toggle" target="_self" style="text-decoration:none;">{hamburger_svg}</a>
        </div>

        <!-- Primary Navigation Menu -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="?action=nav_dashboard" class="nav-item {'active' if active_page == 'dashboard' else ''}" target="_self">
                    <span class="nav-item-icon">{dashboard_svg}</span>
                    <span>Dashboard</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_connections" class="nav-item {'active' if active_page == 'connections' else ''}" target="_self">
                    <span class="nav-item-icon">{connections_svg}</span>
                    <span>Connections</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_upload" class="nav-item {'active' if active_page == 'upload' else ''}" target="_self">
                    <span class="nav-item-icon">{upload_svg}</span>
                    <span>Upload File</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_schema" class="nav-item {'active' if active_page == 'schema' else ''}" target="_self">
                    <span class="nav-item-icon">{schema_svg}</span>
                    <span>Schema Explorer</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_schemasay_ai" class="nav-item {'active' if active_page == 'schemasay_ai' else ''}" target="_self">
                    <span class="nav-item-icon">{copilot_svg}</span>
                    <span>SchemaSay AI</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_workbench" class="nav-item {'active' if active_page == 'workbench' else ''}" target="_self">
                    <span class="nav-item-icon">{workbench_svg}</span>
                    <span>SQL Workbench</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_history" class="nav-item {'active' if active_page == 'history' else ''}" target="_self">
                    <span class="nav-item-icon">{history_svg}</span>
                    <span>Query History</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_visualizations" class="nav-item {'active' if active_page == 'visualizations' else ''}" target="_self">
                    <span class="nav-item-icon">{visualizations_svg}</span>
                    <span>Visualizations</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_results" class="nav-item {'active' if active_page == 'results' else ''}" target="_self">
                    <span class="nav-item-icon">{results_svg}</span>
                    <span>Results</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_insights" class="nav-item {'active' if active_page == 'insights' else ''}" target="_self">
                    <span class="nav-item-icon">{insights_svg}</span>
                    <span>Insights</span>
                </a>
            </li>
        </ul>

        <div class="sidebar-divider"></div>

        <!-- Secondary Navigation Menu -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="?action=nav_settings" class="nav-item {'active' if active_page == 'settings' else ''}" target="_self">
                    <span class="nav-item-icon">{settings_svg}</span>
                    <span>Settings</span>
                </a>
            </li>
            <li>
                <a href="?action=nav_help" class="nav-item {'active' if active_page == 'help' else ''}" target="_self">
                    <span class="nav-item-icon">{help_svg}</span>
                    <span>Help</span>
                </a>
            </li>
        </ul>

        <div class="sidebar-divider"></div>

        <!-- Logout CTA -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="?action=logout" class="nav-item logout-item" target="_self">
                    <span class="nav-item-icon">{logout_svg}</span>
                    <span>Logout</span>
                </a>
            </li>
        </ul>

        <!-- Bottom Quick Tip Card -->
        <div class="quick-tip-card">
            <div class="quick-tip-header">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="quick-tip-icon">{lightbulb_svg}</span>
                    <span class="quick-tip-title">Quick Tip</span>
                </div>
            </div>
            <div class="quick-tip-desc">{tip_text}</div>
            <div class="quick-tip-footer">
                <div class="quick-tip-pagination">
                    {dots_html}
                </div>
                <a class="tip-nav-btn" href="?action=tip_{next_idx}" target="_self">Next ➜</a>
            </div>
        </div>
    </div>
    """
    
    return sidebar_html
