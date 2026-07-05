import os
import requests
from typing import Optional

# Dynamically load the backend URL from environment variables, defaulting to local development port
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

class APIClient:
    """
    HTTP client wrapper handling all communications between 
    the Streamlit frontend and the versioned FastAPI backend.
    """
    def __init__(self):
        self.base_url = BACKEND_URL

    def check_health(self) -> bool:
        """
        Queries the backend health check endpoint.
        Returns True if online, False otherwise.
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
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
        return requests.post(f"{self.base_url}/api/v1/auth/register", json=payload)

    def login(self, email: str, password: str) -> requests.Response:
        """
        Sends credentials to login endpoint and retrieves token data.
        """
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(f"{self.base_url}/api/v1/auth/login", json=payload)

    def refresh(self, refresh_token: str) -> requests.Response:
        """
        Submits a refresh token to obtain a rotated credentials set.
        """
        payload = {
            "refresh_token": refresh_token
        }
        return requests.post(f"{self.base_url}/api/v1/auth/refresh", json=payload)

    def logout(self, token: str) -> requests.Response:
        """
        Submits the active access token for backend session revocation.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return requests.post(f"{self.base_url}/api/v1/auth/logout", headers=headers)

    def get_me(self, token: str) -> requests.Response:
        """
        Retrieves active user profile using the JWT access token.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(f"{self.base_url}/api/v1/auth/me", headers=headers)

api_client = APIClient()
