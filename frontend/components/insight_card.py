import html
import streamlit as st

def render_insight_card(insight: str):
    """
    Renders a premium, styled AI business insight card in Streamlit.
    Escapes all LLM-generated outputs to prevent HTML, SVG, and JavaScript injection (XSS).
    """
    if not insight:
        return

    # Neutralize any malicious DOM elements or script blocks in LLM output
    safe_insight = html.escape(insight)

    st.markdown(
        f"""
        <div style="
            border-radius: 12px;
            padding: 20px;
            background: linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(13, 71, 161, 0.08) 100%);
            border: 1px solid rgba(25, 118, 210, 0.15);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
            margin-top: 20px;
            margin-bottom: 20px;
        ">
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                color: rgb(25, 118, 210);
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                💡 AI Business Insight
            </div>
            <p style="
                font-size: 0.95rem;
                line-height: 1.6;
                color: var(--text-color, #333333);
                margin: 0;
                font-family: 'Outfit', 'Inter', sans-serif;
                white-space: pre-wrap;
            ">
                {safe_insight}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
