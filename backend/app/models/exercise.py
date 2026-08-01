"""
Exercise model
"""

from sqlalchemy import Column, String, Text, Integer, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import BaseModel


class DifficultyLevel(str, PyEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MuscleGroup(str, PyEnum):
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


class Exercise(BaseModel):
    """Exercise library"""

    __tablename__ = "exercises"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    muscle_groups = Column(Enum(MuscleGroup), nullable=True)  # Primary muscle group
    secondary_muscles = Column(String(500))  # Comma-separated list of secondary muscles
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)

    # Media
    video_url = Column(String(500))
    image_url = Column(String(500))

    # Form analysis
    is_core_exercise = Column(Boolean, default=False)  # For MVP: 5 core exercises
    form_analysis_available = Column(Boolean, default=False)

    # Metadata
    equipment_required = Column(String(100))  # bodyweight, dumbbells, etc.
    category = Column(String(100))  # strength, cardio, mobility, etc.

    # Relations (for workout planning)
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")
    form_analysis_events = relationship("FormAnalysisEvent", back_populates="exercise")
