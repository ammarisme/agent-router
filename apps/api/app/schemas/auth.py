"""Authentication schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    """Sign up request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    name: str = Field(..., min_length=2, max_length=50, description="User full name")
    accept_terms: bool = Field(..., description="Must accept terms and conditions")


class SignInRequest(BaseModel):
    """Sign in request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    remember_me: Optional[bool] = Field(False, description="Remember user session")


class UserResponse(BaseModel):
    """User response schema."""
    id: UUID = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    status: str = Field(..., description="User status (active/inactive)")
    roles: List[str] = Field(default_factory=list, description="User roles")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")

    class Config:
        from_attributes = True


class SignInResponse(BaseModel):
    """Sign in response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse


class SignUpResponse(BaseModel):
    """Sign up response schema."""
    message: str = Field(..., description="Success message")
    user: UserResponse


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str = Field(..., description="JWT refresh token")


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema."""
    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
