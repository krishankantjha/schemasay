import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    Provides type validation and fail-fast checks on startup.
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Default: 15 minutes. Override via ACCESS_TOKEN_EXPIRE_MINUTES in .env
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI provider API keys — both are optional. If neither is set, the heuristic offline compiler is used instead.
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Fernet symmetric encryption key for storing database credentials. Generate with: Fernet.generate_key()
    ENCRYPTION_KEY: str
    
    # Allowed origins for CORS (comma-separated string)
    ALLOWED_ORIGINS: str = "http://localhost:8501,http://127.0.0.1:8501"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        extra="ignore"
    )

settings = Settings()
