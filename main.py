import streamlit as st
import os

# 1. Set Streamlit Page Configurations
st.set_page_config(
    page_title="SchemaSay Workspace",
    layout="wide"
)

# 2. Inject Reusable Design System and Application Shell CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Top Navigation Bar Structure (HTML)
st.markdown(
    """
    <div class="header-navbar">
        <div class="header-logo-section">
            <span class="header-menu-toggle">☰</span>
            <span class="header-logo-text">Schema<span class="header-logo-accent">Say</span></span>
        </div>
        <div class="header-spacer"></div>
        <div class="header-user-section">
            <span class="header-theme-toggle">🌙</span>
            <div class="header-avatar">JD</div>
            <span class="header-username">John Doe</span>
            <span class="header-dropdown-arrow">▼</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Left Sidebar Navigation Panel Structure (HTML)
st.sidebar.markdown(
    """
    <div class="sidebar-links-wrapper">
        <div class="sidebar-link active"><span class="sidebar-link-icon">🏠</span> Dashboard</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">📁</span> Connections</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">📤</span> Upload File</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">🔍</span> Schema Explorer</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">💬</span> AI Copilot</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">💻</span> SQL Workbench</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">📜</span> Query History</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">📊</span> Visualizations</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">📋</span> Results</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">💡</span> Insights</div>
        <div class="sidebar-link-divider"></div>
        <div class="sidebar-link"><span class="sidebar-link-icon">⚙️</span> Settings</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">❓</span> Help</div>
        <div class="sidebar-link sidebar-link-logout"><span class="sidebar-link-icon">🚪</span> Logout</div>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Proportional Three-Column Content Wrapper Grid
col_left, col_center, col_right = st.columns([1.2, 3.2, 1.3], gap="medium")

# Column 1: Schema Explorer placeholder card
with col_left:
    st.markdown(
        """
        <div class="placeholder-card card-tall">
            <div class="placeholder-title">Schema Explorer</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Column 2: Center Workspace Canvas (AI Copilot & SQL Workbench top, Results bottom)
with col_center:
    col_top1, col_top2 = st.columns([1, 1.1], gap="medium")
    with col_top1:
        st.markdown(
            """
            <div class="placeholder-card card-medium">
                <div class="placeholder-title">AI Copilot</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_top2:
        st.markdown(
            """
            <div class="placeholder-card card-medium">
                <div class="placeholder-title">SQL Workbench</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <div class="placeholder-card card-large">
            <div class="placeholder-title">Results Area</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Column 3: Right Stacked Panels (Query History & Insights)
with col_right:
    st.markdown(
        """
        <div class="placeholder-card card-medium-alt">
            <div class="placeholder-title">Query History</div>
        </div>
        <div class="placeholder-card card-small-alt">
            <div class="placeholder-title">Business Insights</div>
        </div>
        """,
        unsafe_allow_html=True
    )
