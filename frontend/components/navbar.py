"""
SchemaSay Components — Top Navigation Bar

Modular navbar rendering helper returning high-fidelity HTML markup
and vector action icons matching our design tokens.
Now fully interactive, supporting notifications lists, profile dropdowns, and theme toggling.
"""

import streamlit as st
from services.notification_service import get_notifications, get_unread_count

def render_navbar(title: str = "Dashboard", display_name: str = "John Doe", initials: str = "JD") -> str:
    """
    Renders the top navigation bar, including:
      - Left: Page Title, Page Breadcrumb, and Connection Status pill
      - Center: Inline Search block (rendered if st.session_state.search_open is True)
      - Right: Search triggers, Notifications bell with unread badge, Theme toggle (Moon/Sun),
               User profile initials, chevron, and active dropdown list panels.
    """
    email = st.session_state.get("user_information", {}).get("email", "john.doe@example.com")
    
    # ── SVG Vector Icons ──────────────────────────────────────────────────────
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
    
    sun_svg = (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="5"></circle>'
        '<line x1="12" y1="1" x2="12" y2="3"></line>'
        '<line x1="12" y1="21" x2="12" y2="23"></line>'
        '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>'
        '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>'
        '<line x1="1" y1="12" x2="3" y2="12"></line>'
        '<line x1="21" y1="12" x2="23" y2="12"></line>'
        '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>'
        '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>'
        '</svg>'
    )
    
    chevron_svg = (
        '<svg class="navbar-user-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="6 9 12 15 18 9"></polyline>'
        '</svg>'
    )

    # ── State Checks ──────────────────────────────────────────────────────────
    theme_svg = sun_svg if st.session_state.get("theme") == "dark" else moon_svg
    
    # ── Notification Badge ────────────────────────────────────────────────────
    unread_count = get_unread_count()
    badge_html = f'<span class="navbar-notification-badge"></span>' if unread_count > 0 else ""
    
    # ── Center Search Block ───────────────────────────────────────────────────
    search_bar_html = ""
    if st.session_state.get("search_open", False):
        search_bar_html = """
        <div class="navbar-search-container">
            <input type="text" placeholder="Search prompts..." class="navbar-search-input" autofocus />
        </div>
        """
        
    # ── Notification Dropdown List overlay HTML ────────────────────────────────
    notifications_dropdown_html = ""
    if st.session_state.get("notifications_open", False):
        items_html = ""
        notifications = get_notifications()
        if not notifications:
            items_html = '<div class="notification-item" style="text-align:center; font-size:11px; color:var(--color-text-secondary);">No notifications found</div>'
        else:
            for n in notifications:
                unread_class = "unread" if n.get("unread", False) else ""
                items_html += f"""
                <div class="notification-item {unread_class}">
                    <span class="notification-text">{n['text']}</span>
                    <span class="notification-time">{n['time']}</span>
                </div>
                """
        notifications_dropdown_html = f"""
        <div class="navbar-dropdown-panel notifications-dropdown">
            <div class="dropdown-header">
                <span>Alerts ({unread_count} unread)</span>
                <a href="?action=mark_read" class="mark-read-btn" target="_self">Mark read</a>
            </div>
            <div class="dropdown-body">
                {items_html}
            </div>
        </div>
        """
        
    # ── User Profile Dropdown Menu overlay HTML ────────────────────────────────
    profile_dropdown_html = ""
    if st.session_state.get("profile_open", False):
        profile_dropdown_html = f"""
        <div class="navbar-dropdown-panel profile-dropdown">
            <div class="profile-dropdown-user">
                <div class="profile-dropdown-name">{display_name}</div>
                <div class="profile-dropdown-email">{email}</div>
            </div>
            <div class="dropdown-divider"></div>
            <a href="?action=nav_settings" class="dropdown-item" target="_self">Account Settings</a>
            <a href="?action=nav_help" class="dropdown-item" target="_self">Help Guides</a>
            <div class="dropdown-divider"></div>
            <a href="?action=logout" class="dropdown-item logout-item" target="_self">Logout Account</a>
        </div>
        """

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
                <span>{st.session_state.get("connection_status", "Connected to PostgreSQL")}</span>
            </div>
        </div>

        <!-- Center Section: Inline Search Modal -->
        <div class="navbar-center">
            {search_bar_html}
        </div>

        <!-- Right Section: Action Controls & User Profiles -->
        <div class="navbar-right" style="position: relative;">
            <div class="navbar-controls">
                <a href="?action=toggle_search" class="navbar-icon-btn" title="Search" target="_self">
                    {search_svg}
                </a>
                <a href="?action=toggle_notifications" class="navbar-icon-btn" title="Notifications" target="_self">
                    {bell_svg}
                    {badge_html}
                </a>
                <a href="?action=toggle_theme" class="navbar-icon-btn" title="Toggle Theme" target="_self">
                    {theme_svg}
                </a>
            </div>
            <a href="?action=toggle_profile" class="navbar-user-profile" target="_self">
                <div class="navbar-user-avatar">{initials}</div>
                <span class="navbar-user-name">{display_name}</span>
                {chevron_svg}
            </a>
            {notifications_dropdown_html}
            {profile_dropdown_html}
        </div>
    </div>
    """
    
    return navbar_html
