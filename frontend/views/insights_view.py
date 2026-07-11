"""
SchemaSay Views — AI Insights View

Renders detailed natural language analytical findings and LLM summaries.
"""

import streamlit as st

def show_insights_view():
    """Renders the AI Insights report log panel."""
    with st.container(border=True):
        st.write("### AI Analytical Insights")
        st.write("Review auto-generated summaries, performance trends, and anomalies discovered across database tables.")
        st.markdown("---")

        # Mock Insights cards
        insights_list = [
            {
                "icon": "📈",
                "title": "Revenue Acceleration Detected",
                "desc": "Sales metrics show a 12% revenue growth rate starting July 8. This spike is highly correlated with the regional discount campaign launched in the East zone.",
                "type": "positive"
            },
            {
                "icon": "⚠️",
                "title": "Unusual Cart Abandonment Spike",
                "desc": "A 4.2x increase in abandoned carts was identified on July 9 between 14:00 and 16:30 UTC. Recommend checking checkout api latency logs.",
                "type": "warning"
            },
            {
                "icon": "💡",
                "title": "Product Recommendation Optimization",
                "desc": "Customers buying products in category 'Electronics' have a 68% probability of purchasing an 'Accessories' category item within 24 hours. Suggest launching cross-sell bundles.",
                "type": "info"
            }
        ]

        for ins in insights_list:
            bg_color = "rgba(16,185,129,0.04)" if ins["type"] == "positive" else "rgba(245,158,11,0.04)" if ins["type"] == "warning" else "rgba(59,130,246,0.04)"
            border_color = "rgba(16,185,129,0.15)" if ins["type"] == "positive" else "rgba(245,158,11,0.15)" if ins["type"] == "warning" else "rgba(59,130,246,0.15)"
            
            st.markdown(
                f"""
                <div style="background-color:{bg_color}; border:1px solid {border_color}; padding:16px; border-radius:10px; margin-bottom:14px;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                        <span style="font-size:20px;">{ins['icon']}</span>
                        <span style="font-weight:700; font-size:14px; color:var(--color-text-primary);">{ins['title']}</span>
                    </div>
                    <div style="font-size:12px; color:var(--color-text-secondary); line-height:1.5; padding-left:30px;">
                        {ins['desc']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
