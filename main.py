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

# Column 1: Schema Explorer tall card
with col_left:
    st.markdown(
        """
        <div class="workspace-card card-tall" style="display: flex; flex-direction: column;">
            <div class="card-header-row" style="margin-bottom: 12px;">
                <div class="card-header-title">Schema Explorer</div>
            </div>
            <div class="schema-search-container" style="margin-bottom: 12px;">
                <input type="text" class="schema-search-input" placeholder="Search tables or columns..." />
            </div>
            <div class="schema-tree-scroll" style="flex-grow: 1; overflow-y: auto;">
                <!-- Schema level node -->
                <div class="schema-tree-node schema-level-1">
                    <span class="schema-arrow">▼</span>
                    <span class="schema-icon">🗄️</span>
                    <span class="schema-node-name">public</span>
                    <span class="schema-badge">12</span>
                </div>
                
                <!-- Expanded Table level node -->
                <div class="schema-tree-node schema-level-2 active-table">
                    <span class="schema-arrow">▼</span>
                    <span class="schema-icon">📋</span>
                    <span class="schema-node-name">orders</span>
                </div>
                
                <!-- Columns -->
                <div class="schema-tree-node schema-level-3">
                    <span class="schema-pk-icon">🔑</span>
                    <span class="schema-node-name">order_id</span>
                    <span class="schema-type-label">INT</span>
                </div>
                <div class="schema-tree-node schema-level-3">
                    <span class="schema-bullet">•</span>
                    <span class="schema-node-name">customer_id</span>
                    <span class="schema-type-label">INT</span>
                </div>
                <div class="schema-tree-node schema-level-3">
                    <span class="schema-bullet">•</span>
                    <span class="schema-node-name">order_date</span>
                    <span class="schema-type-label">DATE</span>
                </div>
                <div class="schema-tree-node schema-level-3">
                    <span class="schema-bullet">•</span>
                    <span class="schema-node-name">total_amount</span>
                    <span class="schema-type-label">NUMERIC</span>
                </div>
                <div class="schema-tree-node schema-level-3">
                    <span class="schema-bullet">•</span>
                    <span class="schema-node-name">status</span>
                    <span class="schema-type-label">VARCHAR</span>
                </div>

                <!-- Collapsed Sibling Tables -->
                <div class="schema-tree-node schema-level-2">
                    <span class="schema-arrow">▶</span>
                    <span class="schema-icon">📋</span>
                    <span class="schema-node-name">customers</span>
                </div>
                <div class="schema-tree-node schema-level-2">
                    <span class="schema-arrow">▶</span>
                    <span class="schema-icon">📋</span>
                    <span class="schema-node-name">products</span>
                </div>
                <div class="schema-tree-node schema-level-2">
                    <span class="schema-arrow">▶</span>
                    <span class="schema-icon">📋</span>
                    <span class="schema-node-name">order_items</span>
                </div>
                <div class="schema-tree-node schema-level-2">
                    <span class="schema-arrow">▶</span>
                    <span class="schema-icon">📋</span>
                    <span class="schema-node-name">categories</span>
                </div>
            </div>
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
            <div class="workspace-card" style="min-height: 330px; margin-bottom: 0;">
                <div class="card-header-row" style="margin-bottom: 12px;">
                    <div class="card-header-title">
                        <span class="sparkle-icon">✦</span> AI Copilot
                    </div>
                </div>
                <div class="copilot-input-container">
                    <input type="text" class="copilot-input-box" value="Show total sales per month for the last year" readonly />
                    <button class="copilot-generate-btn">
                        Generate SQL <span class="btn-paper-plane">✈</span>
                    </button>
                </div>
                <div class="sql-preview-block">
                    <div class="code-line-numbers">
                        <div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div>
                    </div>
                    <div class="code-content">
                        <div><span class="sql-keyword">SELECT</span> <span class="sql-function">DATE_TRUNC</span>(<span class="sql-string">'month'</span>, order_date) <span class="sql-keyword">AS</span> month,</div>
                        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sql-function">SUM</span>(total_amount) <span class="sql-keyword">AS</span> total_sales</div>
                        <div><span class="sql-keyword">FROM</span> orders</div>
                        <div><span class="sql-keyword">WHERE</span> order_date &gt;= <span class="sql-function">DATE_TRUNC</span>(<span class="sql-string">'year'</span>, <span class="sql-keyword">CURRENT_DATE</span>) - <span class="sql-keyword">INTERVAL</span> <span class="sql-string">'1 year'</span></div>
                        <div><span class="sql-keyword">GROUP BY</span> <span class="sql-number">1</span>,</div>
                        <div><span class="sql-keyword">ORDER BY</span> <span class="sql-number">1</span>;</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_top2:
        st.markdown(
            """
            <div class="workspace-card" style="min-height: 330px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div class="card-header-row" style="margin-bottom: 12px;">
                        <div class="card-header-title">SQL Workbench</div>
                        <button class="workbench-format-btn">{} Format SQL</button>
                    </div>
                    <div class="workbench-editor-container">
                        <div class="code-line-numbers">
                            <div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div>
                        </div>
                        <div class="code-content">
                            <div><span class="sql-keyword">SELECT</span> <span class="sql-function">DATE_TRUNC</span>(<span class="sql-string">'month'</span>, order_date) <span class="sql-keyword">AS</span> month,</div>
                            <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sql-function">SUM</span>(total_amount) <span class="sql-keyword">AS</span> total_sales</div>
                            <div><span class="sql-keyword">FROM</span> orders</div>
                            <div><span class="sql-keyword">WHERE</span> order_date &gt;= <span class="sql-function">DATE_TRUNC</span>(<span class="sql-string">'year'</span>, <span class="sql-keyword">CURRENT_DATE</span>)</div>
                            <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <span class="sql-keyword">INTERVAL</span> <span class="sql-string">'1 year'</span></div>
                            <div><span class="sql-keyword">GROUP BY</span> <span class="sql-number">1</span>; <span class="sql-keyword">ORDER BY</span> <span class="sql-number">1</span>;</div>
                        </div>
                    </div>
                </div>
                <div class="workbench-toolbar" style="margin-top: 12px;">
                    <button class="toolbar-btn-run">▶ Run Query</button>
                    <div class="toolbar-center-group">
                        <button class="toolbar-btn-icon">↕</button>
                        <button class="toolbar-btn-icon">↻</button>
                    </div>
                    <button class="toolbar-btn-save">💾 Save Query</button>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <div class="workspace-card card-large" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="tabs-header-bar" style="margin-bottom: 12px;">
                    <div class="tab-item active">Results</div>
                    <div class="tab-item">Visualizations</div>
                    <div class="tab-item">Insights</div>
                </div>
                <div class="results-search-row" style="margin-bottom: 12px;">
                    <input type="text" class="results-search-input" placeholder="🔍 Search results..." />
                </div>
                <div class="table-container">
                    <table class="data-table data-table-striped">
                        <thead>
                            <tr>
                                <th class="table-th-sortable table-th-sorted-asc">month</th>
                                <th class="table-th-sortable">total_sales</th>
                                <th class="table-th-sortable">order_count</th>
                                <th class="table-th-sortable">avg_order_value</th>
                                <th class="table-th-sortable">new_customers</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2024-01-01</td>
                                <td>98,420.50</td>
                                <td>1,243</td>
                                <td>79.23</td>
                                <td>342</td>
                            </tr>
                            <tr>
                                <td>2024-02-01</td>
                                <td>110,250.75</td>
                                <td>1,512</td>
                                <td>72.88</td>
                                <td>421</td>
                            </tr>
                            <tr>
                                <td>2024-03-01</td>
                                <td>125,630.20</td>
                                <td>1,785</td>
                                <td>70.41</td>
                                <td>512</td>
                            </tr>
                            <tr>
                                <td>2024-04-01</td>
                                <td>132,980.60</td>
                                <td>1,958</td>
                                <td>67.98</td>
                                <td>480</td>
                            </tr>
                            <tr>
                                <td>2024-05-01</td>
                                <td>142,770.90</td>
                                <td>2,104</td>
                                <td>67.83</td>
                                <td>567</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="table-pagination-bar" style="margin-top: 12px;">
                <div>Showing 1 to 5 of 12 results</div>
                <div class="pagination-right-group">
                    <div class="pagination-buttons">
                        <button class="pagination-btn-nav">&lt;</button>
                        <button class="pagination-btn-num active">1</button>
                        <button class="pagination-btn-num">2</button>
                        <button class="pagination-btn-num">3</button>
                        <button class="pagination-btn-nav">&gt;</button>
                    </div>
                    <div class="pagination-dropdown-wrapper">
                        <select class="pagination-select">
                            <option>5 / page</option>
                            <option>10 / page</option>
                            <option>25 / page</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Column 3: Right Stacked Panels (Query History, Insights, KPIs, Activity)
with col_right:
    # 1. Query History Card
    st.markdown(
        """
        <div class="workspace-card card-medium-alt" style="display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 20px;">
            <div>
                <div class="card-header-row" style="margin-bottom: 12px;">
                    <div class="card-header-title">Query History</div>
                </div>
                <div class="history-search-row" style="margin-bottom: 12px;">
                    <input type="text" class="history-search-input" placeholder="🔍 Search queries..." />
                </div>
                <div class="history-feed-scroll">
                    <!-- Item 1 -->
                    <div class="history-item-row">
                        <div class="history-item-badge badge-warning-bullet"></div>
                        <div class="history-item-content">
                            <div class="history-item-title">Show total sales per month for...</div>
                            <div class="history-item-meta">Just now &nbsp;•&nbsp; <span class="badge-postgres-sm">PG</span></div>
                        </div>
                        <div class="history-item-actions">
                            <span class="history-action-icon">⎋</span>
                        </div>
                    </div>
                    <!-- Item 2 -->
                    <div class="history-item-row">
                        <div class="history-item-badge badge-danger-bullet"></div>
                        <div class="history-item-content">
                            <div class="history-item-title">Top 10 customers by total sales</div>
                            <div class="history-item-meta">Yesterday &nbsp;•&nbsp; <span class="badge-postgres-sm">PG</span></div>
                        </div>
                        <div class="history-item-actions">
                            <span class="history-action-icon">⎋</span>
                        </div>
                    </div>
                    <!-- Item 3 -->
                    <div class="history-item-row">
                        <div class="history-item-badge badge-success-bullet"></div>
                        <div class="history-item-content">
                            <div class="history-item-title">Products with low stock</div>
                            <div class="history-item-meta">Yesterday &nbsp;•&nbsp; <span class="badge-mysql-sm">MY</span></div>
                        </div>
                        <div class="history-item-actions">
                            <span class="history-action-icon">⎋</span>
                        </div>
                    </div>
                    <!-- Item 4 -->
                    <div class="history-item-row">
                        <div class="history-item-badge badge-info-bullet"></div>
                        <div class="history-item-content">
                            <div class="history-item-title">Monthly profit trends</div>
                            <div class="history-item-meta">2 days ago &nbsp;•&nbsp; <span class="badge-sqlite-sm">SL</span></div>
                        </div>
                        <div class="history-item-actions">
                            <span class="history-action-icon">⎋</span>
                        </div>
                    </div>
                    <!-- Item 5 -->
                    <div class="history-item-row">
                        <div class="history-item-badge badge-primary-bullet"></div>
                        <div class="history-item-content">
                            <div class="history-item-title">Total orders by status</div>
                            <div class="history-item-meta">3 days ago &nbsp;•&nbsp; <span class="badge-postgres-sm">PG</span></div>
                        </div>
                        <div class="history-item-actions">
                            <span class="history-action-icon">⎋</span>
                        </div>
                    </div>
                </div>
            </div>
            <button class="history-view-all-btn">View All History</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2. AI Business Insights Card
    st.markdown(
        """
        <div class="workspace-card card-small-alt" style="display: flex; flex-direction: column; margin-bottom: 20px;">
            <div class="card-header-row" style="margin-bottom: 12px;">
                <div class="card-header-title">
                    <span class="sparkle-icon">✦</span> AI Business Insights
                </div>
            </div>
            <div class="insights-scroll-content" style="flex-grow: 1; overflow-y: auto;">
                <div class="insight-bullet-item">
                    <span class="insight-bullet-sparkle">✦</span>
                    <div class="insight-bullet-text">Sales show a steady upward trend with a 45% increase from Jan to May.</div>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-bullet-sparkle">✦</span>
                    <div class="insight-bullet-text">May has the highest sales of $142,770.90.</div>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-bullet-sparkle">✦</span>
                    <div class="insight-bullet-text">Average order value is consistent between $67 - $79.</div>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-bullet-sparkle">✦</span>
                    <div class="insight-bullet-text">New customer acquisition is growing month over month.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. KPI Summary Section (Added for Phase 5)
    st.markdown(
        """
        <div class="workspace-card" style="margin-bottom: 20px; padding: var(--spacing-4);">
            <div class="card-header-row" style="margin-bottom: 12px;">
                <div class="card-header-title">KPI Summary</div>
            </div>
            <div class="kpi-grid">
                <div class="kpi-summary-box">
                    <div class="kpi-label">Total Records</div>
                    <div class="kpi-value">12,483</div>
                    <div class="kpi-trend trend-up">▲ 12%</div>
                </div>
                <div class="kpi-summary-box">
                    <div class="kpi-label">Execution Time</div>
                    <div class="kpi-value">48 ms</div>
                    <div class="kpi-trend trend-down">▼ 8%</div>
                </div>
                <div class="kpi-summary-box">
                    <div class="kpi-label">Rows Returned</div>
                    <div class="kpi-value">5,102</div>
                    <div class="kpi-trend trend-neutral">■ 0%</div>
                </div>
                <div class="kpi-summary-box">
                    <div class="kpi-label">Success Rate</div>
                    <div class="kpi-value">99.4%</div>
                    <div class="kpi-trend trend-up">▲ 0.2%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. Recent Activity Timeline (Added for Phase 5)
    st.markdown(
        """
        <div class="workspace-card" style="padding: var(--spacing-4);">
            <div class="card-header-row" style="margin-bottom: 12px;">
                <div class="card-header-title">Recent Activity</div>
            </div>
            <div class="activity-timeline-wrapper">
                <div class="timeline-track-line"></div>
                <!-- Step 1 -->
                <div class="timeline-event-item">
                    <div class="timeline-bullet bullet-success"></div>
                    <div class="timeline-event-details">
                        <div class="timeline-event-title">PostgreSQL Database Connected</div>
                        <div class="timeline-event-time">5 mins ago</div>
                    </div>
                </div>
                <!-- Step 2 -->
                <div class="timeline-event-item">
                    <div class="timeline-bullet bullet-info"></div>
                    <div class="timeline-event-details">
                        <div class="timeline-event-title">Schema Cache Parsed (12 tables)</div>
                        <div class="timeline-event-time">10 mins ago</div>
                    </div>
                </div>
                <!-- Step 3 -->
                <div class="timeline-event-item">
                    <div class="timeline-bullet bullet-primary"></div>
                    <div class="timeline-event-details">
                        <div class="timeline-event-title">Sales trend SQL query run</div>
                        <div class="timeline-event-time">1 hour ago</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
