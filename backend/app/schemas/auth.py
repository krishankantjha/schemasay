from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Validation schema for incoming registration requests.
    Enforces valid email format and mandatory password field.
    """
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    """
    Serialization schema for outgoing user profile responses.
    Filters out password attributes to prevent credential exposure.
    """
    id: int
    email: EmailStr
    full_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """
    Validation schema for incoming login requests.
    """
    email: EmailStr
    password: str

class Token(BaseModel):
    """
    Structure of the JWT response payload returned on successful login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Structure of the decoded JWT token payload.
    """
    email: Optional[str] = None
