"""
SchemaSay Views — Help & Documentation View

Renders tutorials, security descriptions, and analytics support instructions.
"""

import streamlit as st

def show_help_view():
    """Renders the guides index panel."""
    with st.container(border=True):
        st.write("### Help Center & Guides")
        st.write("Access tutorials, architecture explanations, and documentation on sandbox security constraints.")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.write("##### 🤖 Writing Natural Prompts")
                st.write(
                    "To generate high-quality SQL queries, frame your questions clearly using business terms:\n"
                    "- **Clear:** *'Count customers grouped by signup month in 2026.'*\n"
                    "- **Unclear:** *'Get metrics records'* (Requires dialect schema context)."
                )

        with col2:
            with st.container(border=True):
                st.write("##### 🛡️ Sandbox SQL Security")
                st.write(
                    "SchemaSay enforces read-only sandboxes using SQLGlot AST analysis:\n"
                    "- Blocks destructive writes (`INSERT`, `UPDATE`, `DELETE`, `DROP`).\n"
                    "- Prevents multi-statement semi-colon query injections.\n"
                    "- Rejects SQL timing exploits like `sleep()` or `pg_sleep()`."
                )

        st.write("")
        st.write("#### Frequently Asked Questions")
        
        with st.expander("How do I update database schema reflections?"):
            st.write("Whenever you make migrations on your database engine, click the 'Sync Schema' button under the Connections manager tab to update our introspection catalog.")
            
        with st.expander("Can I upload spreadsheet files?"):
            st.write("Yes! Navigate to 'Upload File', upload any CSV or Excel sheet, and it will be reflected as a queryable SQLite table automatically.")
