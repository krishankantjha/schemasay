"""
SchemaSay Components — Left Navigation Sidebar

Modular sidebar rendering class returning high-fidelity HTML structures
and vector icons matching our design tokens.
"""

def render_sidebar() -> str:
    """
    Renders the unified sidebar, including:
      - Logo Section (Brand + Hamburger)
      - Primary Navigation Menu (Dashboard active, others inactive)
      - Dividers
      - Secondary Navigation Menu (Settings, Help)
      - Logout CTA button
      - Bottom Quick Tip Container Card with indicators
    """
    # Standardized consistent SVG Icons parameters
    # Size: 18x18, Stroke Width: 2, Color: CurrentColor
    
    logo_svg = (
        '<svg class="sidebar-logo-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 2L2 7l10 5 10-5-10-5z"></path>'
        '<path d="M2 17l10 5 10-5"></path>'
        '<path d="M2 12l10 5 10-5"></path>'
        '</svg>'
    )
    
    hamburger_svg = (
        '<svg class="sidebar-menu-toggle" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="3" y1="12" x2="21" y2="12"></line>'
        '<line x1="3" y1="6" x2="21" y2="6"></line>'
        '<line x1="3" y1="18" x2="21" y2="18"></line>'
        '</svg>'
    )
    
    dashboard_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="7" height="9"></rect>'
        '<rect x="14" y="3" width="7" height="5"></rect>'
        '<rect x="14" y="12" width="7" height="9"></rect>'
        '<rect x="3" y="16" width="7" height="5"></rect>'
        '</svg>'
    )
    
    connections_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>'
        '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>'
        '<path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path>'
        '</svg>'
    )
    
    upload_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>'
        '<polyline points="17 8 12 3 7 8"></polyline>'
        '<line x1="12" y1="3" x2="12" y2="15"></line>'
        '</svg>'
    )
    
    schema_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="3"></circle>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
        '</svg>'
    )
    
    copilot_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>'
        '</svg>'
    )
    
    workbench_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="16 18 22 12 16 6"></polyline>'
        '<polyline points="8 6 2 12 8 18"></polyline>'
        '</svg>'
    )
    
    history_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<polyline points="12 6 12 12 16 14"></polyline>'
        '</svg>'
    )
    
    visualizations_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 3v18h18"></path>'
        '<rect x="7" y="9" width="4" height="8" rx="1"></rect>'
        '<rect x="15" y="5" width="4" height="12" rx="1"></rect>'
        '</svg>'
    )
    
    results_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>'
        '<line x1="3" y1="9" x2="21" y2="9"></line>'
        '<line x1="9" y1="21" x2="9" y2="9"></line>'
        '</svg>'
    )
    
    insights_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>'
        '<line x1="12" y1="22.08" x2="12" y2="12"></line>'
        '</svg>'
    )
    
    settings_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="3"></circle>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>'
        '</svg>'
    )
    
    help_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>'
        '<line x1="12" y1="17" x2="12.01" y2="17"></line>'
        '</svg>'
    )
    
    logout_svg = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>'
        '<polyline points="16 17 21 12 16 7"></polyline>'
        '<line x1="21" y1="12" x2="9" y2="12"></line>'
        '</svg>'
    )
    
    lightbulb_svg = (
        '<svg class="quick-tip-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A5 5 0 0 0 8 8c0 1 .3 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"></path>'
        '<line x1="9" y1="18" x2="15" y2="18"></line>'
        '<line x1="10" y1="22" x2="14" y2="22"></line>'
        '</svg>'
    )

    sidebar_html = f"""
    <div class="sidebar-inner">
        <!-- Logo Section -->
        <div class="sidebar-logo-container">
            <a href="#" class="sidebar-logo-brand">
                {logo_svg}
                <span class="sidebar-logo-text">Schema<span class="sidebar-logo-accent">Say</span></span>
            </a>
            {hamburger_svg}
        </div>

        <!-- Primary Navigation Menu -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="#" class="nav-item active">
                    <span class="nav-item-icon">{dashboard_svg}</span>
                    <span>Dashboard</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{connections_svg}</span>
                    <span>Connections</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{upload_svg}</span>
                    <span>Upload File</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{schema_svg}</span>
                    <span>Schema Explorer</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{copilot_svg}</span>
                    <span>AI Copilot</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{workbench_svg}</span>
                    <span>SQL Workbench</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{history_svg}</span>
                    <span>Query History</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{visualizations_svg}</span>
                    <span>Visualizations</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{results_svg}</span>
                    <span>Results</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{insights_svg}</span>
                    <span>Insights</span>
                </a>
            </li>
        </ul>

        <div class="sidebar-divider"></div>

        <!-- Secondary Navigation Menu -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{settings_svg}</span>
                    <span>Settings</span>
                </a>
            </li>
            <li>
                <a href="#" class="nav-item">
                    <span class="nav-item-icon">{help_svg}</span>
                    <span>Help</span>
                </a>
            </li>
        </ul>

        <div class="sidebar-divider"></div>

        <!-- Logout CTA -->
        <ul class="sidebar-menu-list">
            <li>
                <a href="#" class="nav-item logout-item">
                    <span class="nav-item-icon">{logout_svg}</span>
                    <span>Logout</span>
                </a>
            </li>
        </ul>

        <!-- Bottom Quick Tip Card -->
        <div class="quick-tip-card">
            {lightbulb_svg}
            <div class="quick-tip-title">Quick Tip</div>
            <div class="quick-tip-desc">Use natural language in AI Copilot to generate complex SQL queries instantly.</div>
            <div class="quick-tip-pagination">
                <span class="pagination-dot active"></span>
                <span class="pagination-dot"></span>
                <span class="pagination-dot"></span>
                <span class="pagination-dot"></span>
            </div>
        </div>
    </div>
    """
    
    return sidebar_html
