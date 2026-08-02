"""
Authentication routes for Supabase integration
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import httpx
import os
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

from app.config.settings import settings
from app.config.supabase_config import (
    supabase_settings,
    get_current_user_from_supabase,
    TokenPayload
)
from app.schemas.common import SuccessResponse, ErrorResponse

# Create router
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# Security scheme
security = HTTPBearer()


# Supabase client configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", settings.SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", settings.SUPABASE_SERVICE_KEY)


class AuthResponse(BaseModel):
    """Response model for authentication endpoints"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    email: Optional[str] = None


class UserInfoResponse(BaseModel):
    """Response model for user information"""
    id: str
    email: str
    name: Optional[str] = None
    image: Optional[str] = None
    is_authenticated: bool = True


@router.post("/supabase-callback", response_model=AuthResponse)
async def supabase_callback(
    request: Request,
    access_token: str,
    refresh_token: Optional[str] = None
):
    """
    Handle the callback from Supabase OAuth or direct authentication

    This endpoint receives the Supabase access token and validates it,
    then returns our own JWT token for API authentication.
    """
    try:
        # Validate the Supabase token
        payload = supabase_settings.validate_jwt(access_token)
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user in token"
            )

        # Create our own JWT token for API authentication
        # This integrates Supabase auth with our existing JWT system
        token_payload = {
            "sub": user_id,
            "email": email,
            "auth_provider": "supabase",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
        }

        # Sign with our JWT secret
        api_token = jwt.encode(
            token_payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        return AuthResponse(
            access_token=api_token,
            expires_in=settings.JWT_EXPIRY_MINUTES * 60,
            user_id=user_id,
            email=email
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user(
    token_payload: TokenPayload = Depends(get_current_user_from_supabase)
):
    """
    Get current user information from Supabase JWT

    Requires a valid Bearer token in the Authorization header.
    """
    return {
        "id": token_payload.user_id,
        "email": token_payload.email or "",
        "is_authenticated": True
    }


@router.post("/validate", response_model=SuccessResponse)
async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Validate the current JWT token
    """
    try:
        supabase_settings.validate_jwt(credentials.credentials)
        return SuccessResponse(message="Token is valid")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    request: Request,
    refresh_token: str
):
    """
    Refresh the access token using Supabase refresh token
    """
    try:
        # For Supabase, we need to call their token refresh endpoint
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase configuration is missing"
            )

        # Call Supabase token refresh
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/token",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                },
                json={"refresh_token": refresh_token}
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to refresh token"
                )

            data = response.json()
            new_access_token = data.get("access_token")
            user_id = data.get("user", {}).get("id")
            email = data.get("user", {}).get("email")

            if not new_access_token or not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token response"
                )

            # Create our own JWT token
            token_payload = {
                "sub": user_id,
                "email": email,
                "auth_provider": "supabase",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
            }

            api_token = jwt.encode(
                token_payload,
                settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )

            return AuthResponse(
                access_token=api_token,
                expires_in=settings.JWT_EXPIRY_MINUTES * 60,
                user_id=user_id,
                email=email
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/signout", response_model=SuccessResponse)
async def signout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Sign out the current user by invalidating the token

    Note: JWT tokens are stateless, so this mainly cleans up on the client side.
    For true token invalidation, a token blacklist system would be needed.
    """
    try:
        # Validate the token first
        supabase_settings.validate_jwt(credentials.credentials)

        # In a real implementation, we could add the token to a blacklist
        # For now, just return success - client should clear their tokens
        return SuccessResponse(message="Successfully signed out")

    except Exception:
        # Even if token is invalid, we can still return success
        # as the user wants to sign out
        return SuccessResponse(message="Successfully signed out")


def get_current_user(
    token: str = None
) -> TokenPayload:
    """
    Dependency to get current user for protected routes
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return get_current_user_from_supabase(token)


def get_optional_user(
    token: str = None
) -> Optional[TokenPayload]:
    """
    Dependency to get current user if token is valid, or None if not authenticated
    Useful for routes that work with or without authentication
    """
    try:
        if not token:
            return None
        return get_current_user_from_supabase(token)
    except:
        return None