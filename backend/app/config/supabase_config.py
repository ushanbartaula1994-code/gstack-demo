"""
Supabase configuration and JWT validation utilities
"""

import os
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from pydantic import BaseModel


class SupabaseSettings:
    """Settings for Supabase integration"""

    def __init__(self):
        from app.config.settings import settings
        self.supabase_url: str = os.getenv("SUPABASE_URL", "") or settings.SUPABASE_URL
        self.supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "") or settings.SUPABASE_SERVICE_KEY
        self.jwt_secret: str = (os.getenv("SUPABASE_JWT_SECRET", "")
                               or settings.SUPABASE_JWT_SECRET
                               or settings.JWT_SECRET)

    def validate_jwt(self, token: str) -> dict:
        """
        Validate Supabase JWT token and return the payload

        Args:
            token: JWT token to validate

        Returns:
            dict: Decoded token payload

        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            # Supabase JWT tokens use the JWT secret from Supabase config
            # If we have a service key, we can verify it directly
            if self.supabase_service_key:
                payload = jwt.decode(
                    token,
                    self.supabase_service_key,
                    algorithms=["HS256"],
                    options={"verify_exp": True, "verify_iat": True}
                )
            else:
                # Fallback to our JWT secret for development
                payload = jwt.decode(
                    token,
                    self.jwt_secret,
                    algorithms=["HS256"],
                    options={"verify_exp": True, "verify_iat": True}
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_id_from_token(self, token: str) -> str:
        """
        Extract user ID from Supabase JWT token

        Args:
            token: JWT token

        Returns:
            str: User ID

        Raises:
            HTTPException: If token is invalid or user ID not found
        """
        payload = self.validate_jwt(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    def get_user_email_from_token(self, token: str) -> Optional[str]:
        """
        Extract user email from Supabase JWT token

        Args:
            token: JWT token

        Returns:
            str: User email or None
        """
        payload = self.validate_jwt(token)
        return payload.get("email")


# Token payload model
class TokenPayload(BaseModel):
    sub: str  # User ID
    email: Optional[str] = None
    iat: Optional[float] = None
    exp: Optional[float] = None

    @property
    def user_id(self) -> str:
        return self.sub


# Create settings instance
supabase_settings = SupabaseSettings()


"""
Utility function to validate JWT tokens from Supabase
This can be used as a FastAPI dependency
"""
async def get_current_user_from_supabase(
    token: str = None
) -> TokenPayload:
    """
    FastAPI dependency to get current user from Supabase JWT

    Args:
        token: Bearer token from Authorization header

    Returns:
        TokenPayload: Decoded token payload with user info

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use global settings instance
    settings = supabase_settings

    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    payload = settings.validate_jwt(token)
    return TokenPayload(**payload)


def get_supabase_settings() -> SupabaseSettings:
    """Get the global Supabase settings instance"""
    return supabase_settings