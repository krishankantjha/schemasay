"""
SchemaSay Components — Top Navigation Bar

Modular navbar rendering helper returning high-fidelity HTML markup
and vector action icons matching our design tokens.
"""

def render_navbar(title: str = "Dashboard", display_name: str = "John Doe", initials: str = "JD") -> str:
    """
    Renders the top navigation bar, including:
      - Left: Page Title, Page Breadcrumb, and Connection Status pill
      - Center: Empty spacer
      - Right: Search, Notifications (with red badge), Theme toggle (Moon), User profile initials + name
    """
    # Standardized consistent SVG Icons parameters
    # Size: 16x16, Stroke Width: 2, Color: CurrentColor
    
    search_svg = (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="11" cy="11" r="8"></circle>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"></line>'
        '</svg>'
    )
    
    bell_svg = (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>'
        '<path d="M13.73 21a2 2 0 0 1-3.46 0"></path>'
        '</svg>'
    )
    
    moon_svg = (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>'
        '</svg>'
    )
    
    chevron_svg = (
        '<svg class="navbar-user-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="6 9 12 15 18 9"></polyline>'
        '</svg>'
    )

    navbar_html = f"""
    <div class="navbar-outer">
        <!-- Left Section: Title & Connection Badge -->
        <div class="navbar-left">
            <div class="navbar-title-group">
                <span class="navbar-title">{title}</span>
                <span class="navbar-breadcrumb">Home / {title}</span>
            </div>
            <div class="navbar-conn-badge">
                <span class="conn-status-dot"></span>
                <span>Connected to PostgreSQL</span>
            </div>
        </div>

        <!-- Center Section: Reserved Spacer -->
        <div></div>

        <!-- Right Section: Action Controls & User Profiles -->
        <div class="navbar-right">
            <div class="navbar-controls">
                <div class="navbar-icon-btn" title="Search">
                    {search_svg}
                </div>
                <div class="navbar-icon-btn" title="Notifications">
                    {bell_svg}
                    <span class="navbar-notification-badge"></span>
                </div>
                <div class="navbar-icon-btn" title="Toggle Theme">
                    {moon_svg}
                </div>
            </div>
            <div class="navbar-user-profile">
                <div class="navbar-user-avatar">{initials}</div>
                <span class="navbar-user-name">{display_name}</span>
                {chevron_svg}
            </div>
        </div>
    </div>
    """
    
    return navbar_html
