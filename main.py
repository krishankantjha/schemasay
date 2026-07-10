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

# 4. Left Sidebar Navigation Panel Structure
active_view = st.sidebar.selectbox(
    "Navigation Screen",
    ["Dashboard", "Database Connections", "Spreadsheet Upload", "Settings & Profile"],
    index=0
)

st.sidebar.markdown(
    """
    <div class="sidebar-links-wrapper">
        <div class="sidebar-link-divider"></div>
        <div class="sidebar-link"><span class="sidebar-link-icon">⚙️</span> Settings</div>
        <div class="sidebar-link"><span class="sidebar-link-icon">❓</span> Help</div>
        <div class="sidebar-link sidebar-link-logout"><span class="sidebar-link-icon">🚪</span> Logout</div>
    </div>
    """,
    unsafe_allow_html=True
)

if active_view == "Settings & Profile":
    st.markdown(
        """
        <div class="settings-page-header" style="padding: 0 var(--spacing-6); margin-bottom: 24px;">
            <h1 class="font-h1" style="color: var(--color-text-primary); margin: 0;">Settings</h1>
            <p class="text-subtitle" style="margin: 4px 0 0 0;">Manage your personal profile, account settings, and application preferences.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col_settings_nav, col_settings_content = st.columns([1, 2.8], gap="medium")
    with col_settings_nav:
        settings_section = st.radio(
            "Settings Sub-Navigation",
            ["Profile", "Account", "Security", "Appearance", "Notifications", "API Keys", "Help & About"],
            label_visibility="collapsed"
        )
    with col_settings_content:
        if settings_section == "Profile":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Profile Settings</h3>
                    <div style="display: flex; align-items: center; gap: var(--spacing-5); margin-bottom: var(--spacing-6);">
                        <div class="settings-profile-avatar">JD</div>
                        <div>
                            <button class="btn-base btn-primary btn-sm">Change Photo</button>
                            <p class="text-caption" style="margin: 6px 0 0 0;">JPG, GIF or PNG. Max size of 800K</p>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-4); margin-bottom: var(--spacing-5);">
                        <div class="form-group">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-input" value="John Doe" />
                        </div>
                        <div class="form-group">
                            <label class="form-label">Email Address</label>
                            <input type="email" class="form-input" value="john.doe@schemasay.com" />
                        </div>
                        <div class="form-group">
                            <label class="form-label">Phone Number</label>
                            <input type="text" class="form-input" value="+1 (555) 019-2834" />
                        </div>
                        <div class="form-group">
                            <label class="form-label">Company Name</label>
                            <input type="text" class="form-input" value="SchemaSay Inc." />
                        </div>
                        <div class="form-group">
                            <label class="form-label">Job Title</label>
                            <input type="text" class="form-input" value="Senior Data Analyst" />
                        </div>
                        <div class="form-group">
                            <label class="form-label">Location</label>
                            <input type="text" class="form-input" value="San Francisco, CA" />
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: var(--spacing-6);">
                        <label class="form-label">Personal Bio</label>
                        <textarea class="form-textarea" rows="4">Senior Data Analyst specializing in database operations, sales trends analytics, and SQL query formatting optimizations.</textarea>
                    </div>
                    <div style="display: flex; gap: var(--spacing-3); justify-content: flex-end;">
                        <button class="btn-base btn-outline">Cancel</button>
                        <button class="btn-base btn-primary">Save Changes</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        elif settings_section == "Account":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Account Settings</h3>
                    <div class="form-group" style="margin-bottom: var(--spacing-4);">
                        <label class="form-label">Username</label>
                        <input type="text" class="form-input" value="johndoe_analyst" />
                    </div>
                    <div class="form-group" style="margin-bottom: var(--spacing-4);">
                        <label class="form-label">Secondary Email</label>
                        <input type="email" class="form-input" value="john.backup@gmail.com" />
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--spacing-4); margin-bottom: var(--spacing-6);">
                        <div class="form-group">
                            <label class="form-label">Language</label>
                            <select class="form-select">
                                <option>English (US)</option>
                                <option>Spanish</option>
                                <option>French</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Timezone</label>
                            <select class="form-select">
                                <option>UTC -08:00 (PST)</option>
                                <option>UTC +00:00 (GMT)</option>
                                <option>UTC +05:30 (IST)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Date Format</label>
                            <select class="form-select">
                                <option>YYYY-MM-DD</option>
                                <option>MM/DD/YYYY</option>
                                <option>DD-MM-YYYY</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; gap: var(--spacing-3); justify-content: flex-end;">
                        <button class="btn-base btn-outline">Reset</button>
                        <button class="btn-base btn-primary">Save Settings</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif settings_section == "Security":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Security Credentials</h3>
                    
                    <!-- Change Password -->
                    <div style="border-bottom: 1px solid var(--color-divider); padding-bottom: var(--spacing-5); margin-bottom: var(--spacing-5);">
                        <div class="form-group" style="margin-bottom: var(--spacing-4);">
                            <label class="form-label">Current Password</label>
                            <input type="password" class="form-input" placeholder="••••••••" />
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-4); margin-bottom: var(--spacing-4);">
                            <div class="form-group">
                                <label class="form-label">New Password</label>
                                <input type="password" class="form-input" placeholder="••••••••" />
                            </div>
                            <div class="form-group">
                                <label class="form-label">Confirm New Password</label>
                                <input type="password" class="form-input" placeholder="••••••••" />
                            </div>
                        </div>
                        <div style="margin-bottom: var(--spacing-4);">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                                <span class="text-caption">Password Strength</span>
                                <span class="text-caption" style="color: var(--color-success); font-weight: 600;">Strong</span>
                            </div>
                            <div style="height: 4px; background-color: var(--color-divider); border-radius: var(--radius-pill); overflow: hidden;">
                                <div style="width: 85%; height: 100%; background-color: var(--color-success);"></div>
                            </div>
                        </div>
                        <button class="btn-base btn-primary btn-sm">Update Password</button>
                    </div>

                    <!-- Two-Factor Authentication -->
                    <div style="border-bottom: 1px solid var(--color-divider); padding-bottom: var(--spacing-5); margin-bottom: var(--spacing-5); display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 class="font-h4" style="margin: 0 0 4px 0;">Two-Factor Authentication (2FA)</h4>
                            <p class="text-caption" style="margin: 0;">Add an extra layer of protection to your analyst account credentials.</p>
                        </div>
                        <label class="toggle-switch-wrapper">
                            <input type="checkbox" checked />
                            <span class="toggle-switch-slider"></span>
                        </label>
                    </div>

                    <!-- Active Sessions -->
                    <div>
                        <h4 class="font-h4" style="margin: 0 0 12px 0;">Logged Devices & Active Sessions</h4>
                        <div style="display: flex; flex-direction: column; gap: var(--spacing-3); margin-bottom: var(--spacing-5);">
                            <div style="display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-3); background-color: var(--color-bg-app); border: var(--border-width) var(--border-style) var(--color-border); border-radius: var(--radius-md);">
                                <div>
                                    <div class="text-body" style="font-weight: 600;">Chrome on Windows 11 (Current Session)</div>
                                    <div class="text-caption">San Francisco, CA &nbsp;•&nbsp; IP: 192.168.1.42</div>
                                </div>
                                <span class="badge-base badge-success">Active</span>
                            </div>
                            <div style="display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-3); background-color: var(--color-bg-app); border: var(--border-width) var(--border-style) var(--color-border); border-radius: var(--radius-md);">
                                <div>
                                    <div class="text-body" style="font-weight: 600;">Safari on Apple iPhone 15</div>
                                    <div class="text-caption">San Francisco, CA &nbsp;•&nbsp; IP: 172.56.21.9</div>
                                </div>
                                <button class="btn-base btn-outline btn-sm">Revoke</button>
                            </div>
                        </div>
                        <button class="btn-base btn-danger btn-sm">Logout All Devices</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif settings_section == "Appearance":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Interface Appearance</h3>
                    
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-5); margin-bottom: var(--spacing-6);">
                        <div class="form-group">
                            <label class="form-label">Application Theme</label>
                            <select class="form-select">
                                <option>Light Slate Theme (Mockup Default)</option>
                                <option>Enterprise Dark Theme</option>
                                <option>System Default Settings</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Layout Line Density</label>
                            <select class="form-select">
                                <option>Standard spacing (mockup geometric)</option>
                                <option>Data-Dense (compact views)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Sidebar Navigation Alignment</label>
                            <select class="form-select">
                                <option>Left-hand fixed panel</option>
                                <option>Collapsible overlay navigation</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">System Font Size</label>
                            <select class="form-select">
                                <option>13px (Default standard)</option>
                                <option>12px (Small readability)</option>
                                <option>14px (Large scale)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Layout density preview block -->
                    <div>
                        <h4 class="font-h4" style="margin: 0 0 12px 0;">Visual Layout Preview</h4>
                        <div style="border: var(--border-width) var(--border-style) var(--color-border); border-radius: var(--radius-md); padding: var(--spacing-4); background-color: var(--color-bg-app); display: flex; align-items: center; gap: var(--spacing-4);">
                            <div style="width: 40px; height: 40px; background-color: var(--color-primary-light); color: var(--color-primary); border-radius: var(--radius-circle); display: flex; align-items: center; justify-content: center; font-weight: 700;">Aa</div>
                            <div>
                                <div class="text-body" style="font-weight: 600;">Geometric Layout Scale Preview</div>
                                <p class="text-caption" style="margin: 4px 0 0 0;">This preview demonstrates the selected theme values, density gaps, and Outfit fonts scaling.</p>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif settings_section == "Notifications":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Notification Preferences</h3>
                    <div style="display: flex; flex-direction: column; gap: var(--spacing-5);">
                        <div class="settings-toggle-row">
                            <div>
                                <h4 class="font-h4" style="margin: 0 0 4px 0;">Email Notifications</h4>
                                <p class="text-caption" style="margin: 0;">Receive daily transaction logs, backup registers, and query logs.</p>
                            </div>
                            <label class="toggle-switch-wrapper">
                                <input type="checkbox" checked />
                                <span class="toggle-switch-slider"></span>
                            </label>
                        </div>
                        <div class="settings-toggle-row">
                            <div>
                                <h4 class="font-h4" style="margin: 0 0 4px 0;">Push Notifications</h4>
                                <p class="text-caption" style="margin: 0;">Receive real-time notifications on browser query outcomes.</p>
                            </div>
                            <label class="toggle-switch-wrapper">
                                <input type="checkbox" />
                                <span class="toggle-switch-slider"></span>
                            </label>
                        </div>
                        <div class="settings-toggle-row">
                            <div>
                                <h4 class="font-h4" style="margin: 0 0 4px 0;">AI Business Insights Alerts</h4>
                                <p class="text-caption" style="margin: 0;">Alert when the background pipeline extracts fresh business trends.</p>
                            </div>
                            <label class="toggle-switch-wrapper">
                                <input type="checkbox" checked />
                                <span class="toggle-switch-slider"></span>
                            </label>
                        </div>
                        <div class="settings-toggle-row">
                            <div>
                                <h4 class="font-h4" style="margin: 0 0 4px 0;">Schema Updates Notification</h4>
                                <p class="text-caption" style="margin: 0;">Alert when database schemas sync columns, primary keys, or tables.</p>
                            </div>
                            <label class="toggle-switch-wrapper">
                                <input type="checkbox" checked />
                                <span class="toggle-switch-slider"></span>
                            </label>
                        </div>
                        <div class="settings-toggle-row">
                            <div>
                                <h4 class="font-h4" style="margin: 0 0 4px 0;">Security Alerts</h4>
                                <p class="text-caption" style="margin: 0;">Crucial email warnings when fresh devices login or tokens regenerate.</p>
                            </div>
                            <label class="toggle-switch-wrapper">
                                <input type="checkbox" checked disabled />
                                <span class="toggle-switch-slider"></span>
                            </label>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif settings_section == "API Keys":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <div class="card-header-row" style="margin-bottom: 20px;">
                        <h3 class="font-h3" style="margin: 0;">API Access Tokens</h3>
                        <button class="btn-base btn-primary btn-sm">+ Create Token Key</button>
                    </div>
                    
                    <p class="text-caption" style="margin-bottom: var(--spacing-5);">Expose backend ingestion and query formatting routes to CLI and scripts via secure token headers.</p>
                    
                    <div class="table-container" style="margin-bottom: var(--spacing-5);">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Token Name</th>
                                    <th>Token Value</th>
                                    <th>Created Date</th>
                                    <th>Last Used</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td style="font-weight: 600;">cli_data_ingest_key</td>
                                    <td><code class="text-code" style="background-color: var(--color-bg-app); padding: 2px 6px; border-radius: 4px;">sch_live_••••a83b</code></td>
                                    <td>2026-07-08</td>
                                    <td>10 mins ago</td>
                                    <td><span class="badge-base badge-success">Active</span></td>
                                    <td>
                                        <span class="connection-action-btn" style="margin-right: 8px;">Copy</span>
                                        <span class="connection-action-btn btn-danger-action">Revoke</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="font-weight: 600;">notebook_sales_verify_token</td>
                                    <td><code class="text-code" style="background-color: var(--color-bg-app); padding: 2px 6px; border-radius: 4px;">sch_live_••••f91e</code></td>
                                    <td>2026-07-09</td>
                                    <td>Yesterday</td>
                                    <td><span class="badge-base badge-success">Active</span></td>
                                    <td>
                                        <span class="connection-action-btn" style="margin-right: 8px;">Copy</span>
                                        <span class="connection-action-btn btn-danger-action">Revoke</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <!-- Empty state panel illustration placeholder -->
                    <div class="test-state-box" style="justify-content: center; text-align: center; padding: var(--spacing-5);">
                        <div>
                            <span style="font-size: 24px;">🔑</span>
                            <h4 class="font-h4" style="margin: 8px 0 4px 0;">No Active API Tokens</h4>
                            <p class="text-caption" style="margin: 0;">Create a token key block to automate ingestion steps.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif settings_section == "Help & About":
            st.markdown(
                """
                <div class="workspace-card fade-in" style="padding: var(--spacing-5);">
                    <h3 class="font-h3" style="margin-top: 0; margin-bottom: 20px;">Help & Support Resources</h3>
                    
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-5); margin-bottom: var(--spacing-6);">
                        <div class="card-standard" style="padding: var(--spacing-4);">
                            <h4 class="font-h4" style="margin-top: 0; margin-bottom: 6px;">📖 Product Documentation</h4>
                            <p class="text-caption" style="margin-bottom: 12px;">Explore user manuals, database setup guides, and SQL formatting standards.</p>
                            <button class="btn-base btn-secondary btn-sm" style="width: 100%;">View Docs</button>
                        </div>
                        <div class="card-standard" style="padding: var(--spacing-4);">
                            <h4 class="font-h4" style="margin-top: 0; margin-bottom: 6px;">👥 Developer Community</h4>
                            <p class="text-caption" style="margin-bottom: 12px;">Join the Slack organization to discuss database integration recipes and analyst workflows.</p>
                            <button class="btn-base btn-secondary btn-sm" style="width: 100%;">Join Channel</button>
                        </div>
                        <div class="card-standard" style="padding: var(--spacing-4);">
                            <h4 class="font-h4" style="margin-top: 0; margin-bottom: 6px;">✉ Contact Enterprise Support</h4>
                            <p class="text-caption" style="margin-bottom: 12px;">Talk with database specialists and account support teams for custom SLA inquiries.</p>
                            <button class="btn-base btn-secondary btn-sm" style="width: 100%;">Email Support</button>
                        </div>
                        <div class="card-standard" style="padding: var(--spacing-4);">
                            <h4 class="font-h4" style="margin-top: 0; margin-bottom: 6px;">❓ System FAQ</h4>
                            <p class="text-caption" style="margin-bottom: 12px;">Find quick answers regarding cold start delays, spreadsheet limits, and security protocols.</p>
                            <button class="btn-base btn-secondary btn-sm" style="width: 100%;">Open FAQ</button>
                        </div>
                    </div>

                    <div style="border-top: 1px solid var(--color-divider); padding-top: var(--spacing-4); display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="text-body" style="font-weight: 600;">SchemaSay Workspace Client</div>
                            <div class="text-caption" style="margin-top: 2px;">Version: <strong>1.4.2-staging</strong> &nbsp;•&nbsp; License: <strong>Enterprise Standard SaaS</strong></div>
                        </div>
                        <span class="badge-base badge-secondary">All Services Operational</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.stop()

if active_view == "Database Connections":
    st.markdown(
        """
        <div class="connections-page-wrapper fade-in" style="padding: 0 var(--spacing-6) var(--spacing-8) var(--spacing-6);">
            <div class="page-header-row" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
                <div>
                    <h1 class="font-h1" style="color: var(--color-text-primary); margin: 0;">Database Connections</h1>
                    <p class="text-subtitle" style="margin: 4px 0 0 0;">Create and manage your active database connection parameters.</p>
                </div>
                <button class="btn-base btn-primary">+ Create Connection</button>
            </div>
            
            <div class="connections-toolbar" style="display: flex; gap: var(--spacing-4); margin-bottom: 24px;">
                <input type="text" class="connections-search-input" placeholder="🔍 Search connections..." style="flex-grow: 1;" />
                <select class="pagination-select" style="padding: 8px 14px;">
                    <option>All Databases</option>
                    <option>PostgreSQL</option>
                    <option>MySQL</option>
                    <option>SQLite</option>
                </select>
            </div>
            
            <div class="connections-grid">
                <!-- Card 1: Postgres -->
                <div class="connection-card card-postgres">
                    <div class="connection-card-header">
                        <div class="db-logo-wrapper logo-postgres">PG</div>
                        <div class="connection-status badge-base badge-success">Connected</div>
                    </div>
                    <h3 class="font-h3 connection-name">pg_sales_production</h3>
                    <div class="connection-details">
                        <div class="detail-row"><span class="detail-label">Host:</span> <span class="detail-value">aws-rds-sales.rds.amazonaws.com</span></div>
                        <div class="detail-row"><span class="detail-label">Port:</span> <span class="detail-value">5432</span></div>
                        <div class="detail-row"><span class="detail-label">Database:</span> <span class="detail-value">sales_prod</span></div>
                        <div class="detail-row"><span class="detail-label">Username:</span> <span class="detail-value">sales_admin</span></div>
                    </div>
                    <div class="connection-card-footer">
                        <span class="last-used-label">Last used: 2 mins ago</span>
                        <div class="action-buttons-group">
                            <button class="connection-action-btn">Edit</button>
                            <button class="connection-action-btn btn-danger-action">Delete</button>
                            <button class="btn-base btn-secondary btn-sm">Test Connection</button>
                        </div>
                    </div>
                </div>
                
                <!-- Card 2: MySQL -->
                <div class="connection-card card-mysql">
                    <div class="connection-card-header">
                        <div class="db-logo-wrapper logo-mysql">MY</div>
                        <div class="connection-status badge-base badge-success">Connected</div>
                    </div>
                    <h3 class="font-h3 connection-name">mysql_orders_staging</h3>
                    <div class="connection-details">
                        <div class="detail-row"><span class="detail-label">Host:</span> <span class="detail-value">staging-mysql.orders.net</span></div>
                        <div class="detail-row"><span class="detail-label">Port:</span> <span class="detail-value">3306</span></div>
                        <div class="detail-row"><span class="detail-label">Database:</span> <span class="detail-value">staging_orders</span></div>
                        <div class="detail-row"><span class="detail-label">Username:</span> <span class="detail-value">stage_reader</span></div>
                    </div>
                    <div class="connection-card-footer">
                        <span class="last-used-label">Last used: Yesterday</span>
                        <div class="action-buttons-group">
                            <button class="connection-action-btn">Edit</button>
                            <button class="connection-action-btn btn-danger-action">Delete</button>
                            <button class="btn-base btn-secondary btn-sm">Test Connection</button>
                        </div>
                    </div>
                </div>

                <!-- Card 3: SQLite -->
                <div class="connection-card card-sqlite">
                    <div class="connection-card-header">
                        <div class="db-logo-wrapper logo-sqlite">SL</div>
                        <div class="connection-status badge-base badge-success">Connected</div>
                    </div>
                    <h3 class="font-h3 connection-name">sqlite_local_cache</h3>
                    <div class="connection-details">
                        <div class="detail-row"><span class="detail-label">File Path:</span> <span class="detail-value">/data/local_cache.db</span></div>
                        <div class="detail-row"><span class="detail-label">Database:</span> <span class="detail-value">sqlite_db</span></div>
                        <div class="detail-row"><span class="detail-label">Mode:</span> <span class="detail-value">Read-Write</span></div>
                        <div class="detail-row"><span class="detail-label">Size:</span> <span class="detail-value">24.5 MB</span></div>
                    </div>
                    <div class="connection-card-footer">
                        <span class="last-used-label">Last used: 3 days ago</span>
                        <div class="action-buttons-group">
                            <button class="connection-action-btn">Edit</button>
                            <button class="connection-action-btn btn-danger-action">Delete</button>
                            <button class="btn-base btn-secondary btn-sm">Test Connection</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Connection test states panel details -->
            <div class="workspace-card" style="margin-top: 30px;">
                <div class="card-header-row" style="margin-bottom: 16px;">
                    <div class="card-header-title">Connection Status Tester</div>
                </div>
                <div class="tester-panels-grid">
                    <!-- Testing -->
                    <div class="test-state-box">
                        <div class="test-state-spinner"></div>
                        <div class="test-state-text">Testing connection details for pg_sales_production...</div>
                    </div>
                    <!-- Success -->
                    <div class="test-state-box test-state-success">
                        <span class="test-state-icon">✔</span>
                        <div class="test-state-text">Connection verified successfully! (Latency: 14 ms)</div>
                    </div>
                    <!-- Failed -->
                    <div class="test-state-box test-state-failed">
                        <span class="test-state-icon">✘</span>
                        <div class="test-state-text">Connection failed: Connection timed out. Please check Host and Port.</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

if active_view == "Spreadsheet Upload":
    st.markdown(
        """
        <div class="upload-page-wrapper fade-in" style="padding: 0 var(--spacing-6) var(--spacing-8) var(--spacing-6);">
            <div class="page-header-row" style="margin-bottom: 24px;">
                <div>
                    <h1 class="font-h1" style="color: var(--color-text-primary); margin: 0;">Spreadsheet Upload</h1>
                    <p class="text-subtitle" style="margin: 4px 0 0 0;">Upload CSV or Excel spreadsheets to parse schemas and auto-ingest into memory cache.</p>
                </div>
            </div>
            
            <div class="upload-grid">
                <!-- Left: Drag and Drop -->
                <div class="workspace-card dropzone-card">
                    <div class="upload-dropzone">
                        <div class="upload-cloud-icon">☁</div>
                        <h3 class="font-h3" style="margin: 12px 0 6px 0; color: var(--color-text-primary);">Drag and drop your spreadsheet here</h3>
                        <p class="text-caption" style="margin-bottom: 16px;">Supported formats: CSV, XLSX, XLS (Max size: 50MB)</p>
                        <button class="btn-base btn-primary">Browse Files</button>
                    </div>
                </div>
                
                <!-- Right: Status / Progress -->
                <div class="workspace-card upload-status-card">
                    <div class="card-header-row" style="margin-bottom: 16px;">
                        <div class="card-header-title">Ingestion Pipeline Progress</div>
                    </div>
                    
                    <!-- Progress Bar 1 -->
                    <div class="progress-item-wrapper">
                        <div class="progress-meta">
                            <span class="progress-status-title">Uploading sales_january_2026.csv</span>
                            <span class="progress-percentage">84%</span>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: 84%;"></div>
                        </div>
                        <div class="progress-cancel-row">
                            <span class="text-caption">12.4 MB of 14.8 MB uploaded</span>
                            <span class="cancel-upload-trigger">Cancel</span>
                        </div>
                    </div>
                    
                    <!-- Progress Bar 2 -->
                    <div class="progress-item-wrapper" style="margin-top: 20px;">
                        <div class="progress-meta">
                            <span class="progress-status-title">Validating schema structure...</span>
                            <span class="progress-percentage">98%</span>
                        </div>
                        <div class="progress-track track-success">
                            <div class="progress-fill fill-success" style="width: 98%;"></div>
                        </div>
                        <div class="progress-cancel-row">
                            <span class="text-caption">Checking column types and constraints</span>
                            <span class="cancel-upload-trigger">Cancel</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="upload-outcome-grid" style="margin-top: 30px;">
                <!-- Success Outcome -->
                <div class="workspace-card outcome-success-card">
                    <span class="outcome-icon success-icon">✔</span>
                    <h3 class="font-h3" style="margin: 12px 0 6px 0; color: var(--color-success);">Upload Successful!</h3>
                    <p class="text-body" style="text-align: center; color: var(--color-text-secondary); margin-bottom: 16px;">
                        Spreadsheet <strong>sales_january_2026.csv</strong> was successfully imported.<br/>
                        Parsed <strong>12,483 rows</strong> across <strong>8 columns</strong>. Created table <strong>sales_jan_2026</strong>.
                    </p>
                    <button class="btn-base btn-success">Ingest Table and Query</button>
                </div>
                
                <!-- Error Outcome -->
                <div class="workspace-card outcome-failed-card">
                    <span class="outcome-icon error-icon">✘</span>
                    <h3 class="font-h3" style="margin: 12px 0 6px 0; color: var(--color-danger);">Upload Ingestion Failed</h3>
                    <p class="text-body" style="text-align: center; color: var(--color-text-secondary); margin-bottom: 16px;">
                        Ingestion pipeline failed on step: <strong>Schema Conversion</strong>.<br/>
                        Reason: <em>Malformed encoding structure found on line 4,821. Expected UTF-8 compatible format.</em>
                    </p>
                    <button class="btn-base btn-danger">Upload Another File</button>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

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
