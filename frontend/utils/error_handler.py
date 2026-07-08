import streamlit as st
import requests

def parse_api_response(response: requests.Response, friendly_context: str) -> dict:
    """
    Validates API responses and extracts JSON datasets.
    Standardizes error displays across Streamlit view components.
    """
    if response.status_code in (200, 201):
        try:
            return response.json()
        except Exception:
            return {}

    # Extract backend detail if available
    try:
        err_data = response.json()
        err_detail = err_data.get("detail", "An unexpected error occurred.")
    except Exception:
        err_detail = "Backend connection lost or failed to parse error response."

    if response.status_code == 401:
        st.error(f"Authentication Expired: {err_detail}")
    elif response.status_code == 429:
        st.warning(f"Request throttled: {err_detail}")
    elif response.status_code >= 500:
        st.error(f"Service Error: The analytics server encountered an internal failure. ({err_detail})")
    else:
        st.error(f"Action Failed ({friendly_context}): {err_detail}")

    return {}
