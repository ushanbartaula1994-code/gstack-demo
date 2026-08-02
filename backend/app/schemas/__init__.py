"""Pydantic schemas module"""
from app.schemas.user import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.schemas.exercise import ExerciseResponse, ExerciseListResponse
from app.schemas.workout import (
    WorkoutGenerateRequest,
    WorkoutGenerateResponse,
    WorkoutResponse,
    WorkoutListResponse,
)
from app.schemas.progress import ProgressResponse
from app.schemas.auth import Token, TokenData, UserAuth, UserAuthResponse
from app.schemas.common import (
    MessageResponse,
    SuccessResponse,
    ErrorResponse,
    ApiResponse,
    PaginatedResponse,
    FilterParams,
)

__all__ = [
    # Auth
    "Token",
    "TokenData",
    "UserAuth",
    "UserAuthResponse",
    # User
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    # Exercise
    "ExerciseResponse",
    "ExerciseListResponse",
    # Workout
    "WorkoutGenerateRequest",
    "WorkoutGenerateResponse",
    "WorkoutResponse",
    "WorkoutListResponse",
    # Progress
    "ProgressResponse",
    # Common
    "MessageResponse",
    "SuccessResponse",
    "ErrorResponse",
    "ApiResponse",
    "PaginatedResponse",
    "FilterParams",
]
