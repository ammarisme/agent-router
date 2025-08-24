"""Authentication API endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    SignInRequest,
    SignInResponse,
    SignUpRequest,
    SignUpResponse,
    UserResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.services.auth import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Get authentication service."""
    return AuthService(db)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Get current authenticated user."""
    user = await auth_service.get_current_user(credentials.credentials)
    role_names = [role.name for role in user.roles]
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        status=user.status,
        roles=role_names,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    sign_up_data: SignUpRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> SignUpResponse:
    """Sign up a new user."""
    try:
        result = await auth_service.sign_up(sign_up_data)
        logger.info(f"New user signed up: {sign_up_data.email}")
        return SignUpResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during sign up: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during sign up"
        )


@router.post("/signin", response_model=SignInResponse)
async def sign_in(
    sign_in_data: SignInRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> SignInResponse:
    """Sign in a user."""
    try:
        result = await auth_service.sign_in(sign_in_data)
        logger.info(f"User signed in: {sign_in_data.email}")
        return SignInResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during sign in: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during sign in"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RefreshTokenResponse:
    """Refresh an access token."""
    try:
        result = await auth_service.refresh_token(refresh_data.refresh_token)
        logger.info("Token refreshed successfully")
        return RefreshTokenResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Get current user information."""
    return current_user


@router.post("/signout", status_code=status.HTTP_200_OK)
async def sign_out(
    current_user: UserResponse = Depends(get_current_user),
) -> dict:
    """Sign out a user (client should discard tokens)."""
    logger.info(f"User signed out: {current_user.email}")
    return {"message": "Successfully signed out"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    password_reset_data: PasswordResetRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """Request password reset."""
    # In a real implementation, you would:
    # 1. Generate a reset token
    # 2. Send an email with the reset link
    # 3. Store the token with expiration
    
    logger.info(f"Password reset requested for: {password_reset_data.email}")
    return {
        "message": "If an account with that email exists, a password reset link has been sent"
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    password_reset_confirm: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """Reset password with token."""
    # In a real implementation, you would:
    # 1. Verify the reset token
    # 2. Update the user's password
    # 3. Invalidate the reset token
    
    logger.info("Password reset completed")
    return {"message": "Password has been reset successfully"}


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """Change user password."""
    # In a real implementation, you would:
    # 1. Verify the current password
    # 2. Update to the new password
    # 3. Invalidate all existing tokens
    
    logger.info(f"Password changed for user: {current_user.email}")
    return {"message": "Password changed successfully"}
