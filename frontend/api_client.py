import os
import requests
from typing import Optional

# Dynamically load the backend URL from environment variables, defaulting to local development port
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

class APIClient:
    """
    HTTP client wrapper handling all communications between 
    the Streamlit frontend and the versioned FastAPI backend.
    Uses requests.Session for connection pooling and enforces timeouts on all operations.
    """
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()

    def check_health(self) -> bool:
        """
        Queries the backend health check endpoint.
        Returns True if online, False otherwise.
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=(5, 10))
            return response.status_code == 200
        except Exception:
            return False

    def register(self, email: str, password: str, full_name: Optional[str] = None) -> requests.Response:
        """
        Sends user registration payload to the versioned backend API.
        """
        payload = {
            "email": email,
            "password": password,
            "full_name": full_name
        }
        return self.session.post(f"{self.base_url}/api/v1/auth/register", json=payload, timeout=(5, 30))

    def login(self, email: str, password: str) -> requests.Response:
        """
        Sends credentials to login endpoint and retrieves token data.
        """
        payload = {
            "email": email,
            "password": password
        }
        return self.session.post(f"{self.base_url}/api/v1/auth/login", json=payload, timeout=(5, 30))

    def refresh(self, refresh_token: str) -> requests.Response:
        """
        Submits a refresh token to obtain a rotated credentials set.
        """
        payload = {
            "refresh_token": refresh_token
        }
        return self.session.post(f"{self.base_url}/api/v1/auth/refresh", json=payload, timeout=(5, 30))

    def logout(self, token: str) -> requests.Response:
        """
        Submits the active access token for backend session revocation.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(f"{self.base_url}/api/v1/auth/logout", headers=headers, timeout=(5, 30))

    def get_me(self, token: str) -> requests.Response:
        """
        Retrieves active user profile using the JWT access token.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(f"{self.base_url}/api/v1/auth/me", headers=headers, timeout=(5, 30))

    # --- Connection Management ---

    def get_connections(self, token: str) -> requests.Response:
        """
        Queries and lists all database connection metadata records configured by the active user.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(f"{self.base_url}/api/v1/connections/", headers=headers, timeout=(5, 30))

    def create_connection(self, token: str, payload: dict) -> requests.Response:
        """
        Registers a new database connection configuration (encrypts password on backend).
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(f"{self.base_url}/api/v1/connections/", json=payload, headers=headers, timeout=(5, 30))

    def upload_file_connection(self, token: str, name: str, file_name: str, file_bytes: bytes) -> requests.Response:
        """
        Ingests an uploaded CSV/Excel spreadsheet, loads it into a SQLite table,
        and registers a SQLite database connection record.
        """
        headers = {"Authorization": f"Bearer {token}"}
        files = {"file": (file_name, file_bytes, "application/octet-stream")}
        data = {"name": name}
        return self.session.post(
            f"{self.base_url}/api/v1/connections/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=(5, 60)
        )

    def delete_connection(self, token: str, connection_id: int) -> requests.Response:
        """
        Deletes a database connection record and cleanses any local spreadsheet files.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.delete(f"{self.base_url}/api/v1/connections/{connection_id}", headers=headers, timeout=(5, 30))

    def test_connection(self, token: str, payload: dict) -> requests.Response:
        """
        Tests database connection parameters before saving them.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(f"{self.base_url}/api/v1/connections/test", json=payload, headers=headers, timeout=(5, 30))

    def get_query_history(
        self,
        token: str,
        page: int = 1,
        limit: int = 100,
        connection_id: Optional[int] = None
    ) -> requests.Response:
        """
        Retrieves user's query execution audit history logs (paginated).
        Optionally filters logs by connection source.
        """
        headers = {"Authorization": f"Bearer {token}"}
        params = {"page": page, "limit": limit}
        if connection_id is not None:
            params["connection_id"] = connection_id
        return self.session.get(
            f"{self.base_url}/api/v1/connections/history",
            params=params,
            headers=headers,
            timeout=(5, 30)
        )

    # --- Schema Introspection ---

    def get_schema(self, token: str, connection_id: int) -> requests.Response:
        """
        Retrieves the cached schema metadata layout for a connection.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(f"{self.base_url}/api/v1/schema/{connection_id}", headers=headers, timeout=(5, 30))

    def sync_schema(self, token: str, connection_id: int) -> requests.Response:
        """
        Forces a manual database schema reflection and cache sync.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(f"{self.base_url}/api/v1/schema/{connection_id}/sync", headers=headers, timeout=(5, 30))

    # --- Query Execution ---

    def query_assistant(self, token: str, connection_id: int, question: str) -> requests.Response:
        """
        Translates a natural language question into SQL, runs it, and returns results.
        """
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"connection_id": connection_id, "question": question}
        return self.session.post(f"{self.base_url}/api/v1/assistant/query", json=payload, headers=headers, timeout=(5, 30))

    def execute_raw_sql(self, token: str, connection_id: int, sql_query: str) -> requests.Response:
        """
        Directly executes raw SQL Workbench queries using the dedicated execution engine.
        """
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"connection_id": connection_id, "sql_query": sql_query}
        return self.session.post(f"{self.base_url}/api/v1/query/execute", json=payload, headers=headers, timeout=(5, 30))

    def generate_insight(self, token: str, payload: dict) -> requests.Response:
        """
        Submits data rows, columns, and question to generate AI business narrative insights.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(f"{self.base_url}/api/v1/insights/generate", json=payload, headers=headers, timeout=(5, 30))

api_client = APIClient()
