"""
Workout, WorkoutExercise, and WorkoutSession models
"""

from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel, Base


class Workout(BaseModel):
    """Generated workout programs"""

    __tablename__ = "workouts"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Workout details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    workout_type = Column(String(50))  # strength, cardio, hiiit, mobility, etc.

    # Statistics
    total_duration = Column(Integer)  # Estimated duration in minutes
    estimated_calories = Column(Integer)

    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    rating = Column(Integer)  # User rating 1-5

    # Relations
    user = relationship("User", back_populates="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout", order_by="WorkoutExercise.order")
    sessions = relationship("WorkoutSession", back_populates="workout")


class WorkoutExercise(BaseModel):
    """Exercises within a workout"""

    __tablename__ = "workout_exercises"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    workout_id = Column(String(36), ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False, index=True)

    # Exercise configuration
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    duration_seconds = Column(Integer)  # For timed exercises (plank, etc.)
    rest_time_seconds = Column(Integer, default=60)
    weight_kg = Column(Float)  # Optional: weight used

    # Order within workout
    order = Column(Integer, default=0)

    # Notes
    notes = Column(Text)

    # Relations
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")


class WorkoutSession(BaseModel):
    """Individual workout sessions"""

    __tablename__ = "workout_sessions"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    workout_id = Column(String(36), ForeignKey("workouts.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Session timing
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)  # Actual duration in seconds

    # Statistics
    calories_burned = Column(Integer)
    total_sets = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)

    # Relations
    user = relationship("User", back_populates="sessions")
    workout = relationship("Workout", back_populates="sessions")
    form_analysis_events = relationship("FormAnalysisEvent", back_populates="session")
