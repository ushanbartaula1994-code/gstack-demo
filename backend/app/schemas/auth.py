"""
Schemas for authentication
"""

from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    """Token schema for authentication responses"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: Optional[int] = Field(default=None, description="Expiration time in seconds")


class TokenData(BaseModel):
    """Data contained in JWT token"""
    sub: Optional[str] = Field(default=None, description="User ID")
    email: Optional[str] = Field(default=None, description="User email")


class UserAuth(BaseModel):
    """User authentication data"""
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")


class UserAuthResponse(BaseModel):
    """Successful authentication response"""
    user: dict
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserInDB(BaseModel):
    """User data as stored in database"""
    id: str
    email: str
    hashed_password: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response without sensitive data"""
    id: str
    email: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True