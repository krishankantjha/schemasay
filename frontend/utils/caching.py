import streamlit as st
from api_client import api_client

@st.cache_data(ttl=60)
def get_cached_connections(token: str):
    """
    Caches connection configuration list to improve latency and reduce backend load.
    Partitioned securely by user authorization token.
    """
    res = api_client.get_connections(token)
    if res.status_code == 200:
        return res.json()
    return None

@st.cache_data(ttl=300)
def get_cached_schema(token: str, connection_id: int):
    """
    Caches database schema metadata trees for up to 5 minutes to prevent redundant introspection requests.
    Partitioned securely by user authorization token and target connection source.
    """
    res = api_client.get_schema(token, connection_id)
    if res.status_code == 200:
        return res.json()
    return None
