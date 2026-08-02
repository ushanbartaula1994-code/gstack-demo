"""API routes module"""

# Import existing route modules
from app.routes.health import router as health
from app.routes.auth import router as auth

__all__ = ["health", "auth"]