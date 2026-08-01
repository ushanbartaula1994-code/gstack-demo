"""
Progress Metrics model
"""

from sqlalchemy import Column, String, Integer, Float, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

from app.models.base import BaseModel


class ProgressMetrics(BaseModel):
    """User progress tracking over time"""

    __tablename__ = "progress_metrics"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Date tracking
    record_date = Column(Date, default=date.today, index=True)
    week_number = Column(Integer)  # ISO week number
    month = Column(Integer)  # Month (1-12)
    year = Column(Integer)  # Year

    # Workout statistics
    workouts_completed = Column(Integer, default=0)
    total_duration_minutes = Column(Integer, default=0)
    total_sets = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)

    # Performance metrics
    average_form_score = Column(Float, default=0.0)  # 0-100
    consistency_score = Column(Float, default=0.0)  # 0-100

    # Streaks
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)

    # Goals progress
    goals_progress = Column(JSON)  # {"strength": 0.75, "endurance": 0.5, ...}

    # Relations
    user = relationship("User", back_populates="progress")
