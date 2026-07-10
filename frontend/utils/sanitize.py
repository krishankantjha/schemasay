"""
SchemaSay Frontend — Output Sanitization Utilities

Security helpers for safely rendering user-generated or LLM-generated
content inside Streamlit markdown blocks.
"""

import html
from typing import Any


def escape_html(value: Any) -> str:
    """
    Escapes HTML control characters to prevent stored XSS or injection
    attacks in Streamlit HTML/SVG/markdown blocks.

    Replaces <, >, &, ", and ' with their safe HTML entity equivalents.
    Must be applied to ALL LLM-generated or user-supplied text before
    injecting it into unsafe_allow_html=True markdown calls.

    Args:
        value: Any value to sanitize. None is returned as empty string.

    Returns:
        HTML-safe string.
    """
    if value is None:
        return ""
    return html.escape(str(value))
