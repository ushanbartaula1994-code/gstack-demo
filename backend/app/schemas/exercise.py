"""
Exercise schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    CORE = "core"
    GLUTES = "glutes"
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    CALVES = "calves"
    FULL_BODY = "full_body"


class ExerciseResponse(BaseModel):
    """Schema for exercise response"""
    id: str
    name: str
    description: Optional[str] = None
    muscle_groups: Optional[MuscleGroup] = None
    secondary_muscles: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    is_core_exercise: bool = False
    form_analysis_available: bool = False
    equipment_required: str = "bodyweight"
    category: str = "strength"
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ExerciseListResponse(BaseModel):
    """Schema for list of exercises"""
    exercises: list[ExerciseResponse]
    count: int