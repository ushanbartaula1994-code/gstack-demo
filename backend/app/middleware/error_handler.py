"""
Centralized error handling for consistent API responses
"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _format_error(code: str, message: str, details=None) -> dict:
    """Build a consistent error envelope."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Wrap FastAPI HTTPException into the standard envelope."""
    return JSONResponse(
        status_code=exc.status_code,
        content=_format_error(
            code=f"http_{exc.status_code}",
            message=str(exc.detail),
        ),
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return 422 with field-level error details."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_format_error(
            code="validation_error",
            message="Request validation failed",
            details=exc.errors(),
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Last-resort handler — never leak a stack trace to the client."""
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_format_error(
            code="internal_error",
            message="An internal server error occurred",
        ),
    )


def register_error_handlers(app: FastAPI) -> None:
    """Wire handlers onto the FastAPI app."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
