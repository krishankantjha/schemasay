import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Append project root and frontend directories to path to allow imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "frontend"))

@pytest.fixture(autouse=True)
def mock_streamlit():
    """
    Mocks streamlit session state dictionary and UI alerts to avoid running
    inside a live Streamlit context during backend test execution.
    """
    mock_state = {}
    with patch("streamlit.session_state", mock_state), \
         patch("streamlit.error") as mock_error, \
         patch("streamlit.warning") as mock_warning, \
         patch("streamlit.info") as mock_info, \
         patch("streamlit.success") as mock_success:
        yield {
            "state": mock_state,
            "error": mock_error,
            "warning": mock_warning,
            "info": mock_info,
            "success": mock_success
        }

def test_session_state_initialization(mock_streamlit):
    """
    Verifies that the state manager initializes session state attributes.
    """
    from frontend.state import init_session_state, KEY_ACTIVE_TAB, KEY_WORKBENCH_SQL
    
    init_session_state()
    assert mock_streamlit["state"][KEY_ACTIVE_TAB] == "AI Copilot"
    assert "SELECT * FROM" in mock_streamlit["state"][KEY_WORKBENCH_SQL]

def test_session_state_clear(mock_streamlit):
    """
    Verifies that logging out clears session state variables.
    """
    from frontend.state import init_session_state, clear_session_state, KEY_TOKEN
    
    mock_streamlit["state"][KEY_TOKEN] = "mock-jwt-token"
    init_session_state()
    
    clear_session_state()
    assert KEY_TOKEN not in mock_streamlit["state"]

@patch("api_client.APIClient.get_connections")
def test_cached_connections(mock_get_connections, mock_streamlit):
    """
    Verifies that get_cached_connections caches response contents.
    """
    from frontend.utils.caching import get_cached_connections
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "name": "Test DB"}]
    mock_get_connections.return_value = mock_response
    
    connections = get_cached_connections("mock-token")
    assert len(connections) == 1
    assert connections[0]["name"] == "Test DB"

@patch("api_client.APIClient.get_schema")
def test_cached_schema(mock_get_schema, mock_streamlit):
    """
    Verifies that get_cached_schema caches schema layout metadata.
    """
    from frontend.utils.caching import get_cached_schema
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"table_name": "users", "column_name": "id", "data_type": "integer"}]
    mock_get_schema.return_value = mock_response
    
    schema = get_cached_schema("mock-token", 1)
    assert len(schema) == 1
    assert schema[0]["table_name"] == "users"

def test_api_error_handler_patterns(mock_streamlit):
    """
    Verifies that parse_api_response extracts response JSON on success
    and handles standard HTTP errors with corresponding UI alerts.
    """
    from frontend.utils.error_handler import parse_api_response
    
    # Success response
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {"success": True}
    res = parse_api_response(success_response, "test query")
    assert res == {"success": True}
    
    # Unauthorized response
    unauthorized_response = MagicMock()
    unauthorized_response.status_code = 401
    unauthorized_response.json.return_value = {"detail": "Token expired"}
    res = parse_api_response(unauthorized_response, "test query")
    assert res == {}
    mock_streamlit["error"].assert_called_with("Authentication Expired: Token expired")
    
    # Throttled response
    throttled_response = MagicMock()
    throttled_response.status_code = 429
    throttled_response.json.return_value = {"detail": "Rate limit reached"}
    res = parse_api_response(throttled_response, "test query")
    assert res == {}
    mock_streamlit["warning"].assert_called_with("Request throttled: Rate limit reached")
    
    # Internal service failure response
    internal_response = MagicMock()
    internal_response.status_code = 500
    internal_response.json.return_value = {"detail": "Database connection timeout"}
    res = parse_api_response(internal_response, "test query")
    assert res == {}
    mock_streamlit["error"].assert_called_with("Service Error: The analytics server encountered an internal failure. (Database connection timeout)")

def test_demo_seeding_utility(db):
    """
    Asserts that the demo database seeding utility successfully creates mock SQLite tables,
    populates connection metadata details, caches schema structures, and inserts history logs.
    """
    from app.utils.seed_demo import seed_platform_database
    from app.models.user import User
    from app.models.connection import DatabaseConnection, QueryAuditLog, DatabaseSchemaCache
    
    # Execute the seed script inside testing session context
    seed_platform_database(db)
    
    # Assert database structures exist and are populated
    user = db.query(User).filter(User.email == "demo@schemasay.com").first()
    assert user is not None
    assert user.full_name == "Demo Workspace User"
    
    conn = db.query(DatabaseConnection).filter(DatabaseConnection.user_id == user.id).first()
    assert conn is not None
    assert conn.db_type == "sqlite"
    assert "demo_sales.db" in conn.database_name
    
    schemas = db.query(DatabaseSchemaCache).filter(DatabaseSchemaCache.connection_id == conn.id).all()
    assert len(schemas) > 0
    
    logs = db.query(QueryAuditLog).filter(QueryAuditLog.user_id == user.id).all()
    assert len(logs) == 4
    assert logs[0].question == "What are our total customer records?"
