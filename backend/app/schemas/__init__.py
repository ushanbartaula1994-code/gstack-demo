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
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.common import MessageResponse

__all__ = [
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
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
]
