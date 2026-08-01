"""
Form Analysis Event model
"""

from sqlalchemy import Column, String, Text, Float, JSON, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class FormAnalysisEvent(BaseModel):
    """Real-time form analysis data"""

    __tablename__ = "form_analysis_events"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    session_id = Column(String(36), ForeignKey("workout_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False, index=True)

    # Pose data from MediaPipe (client-side)
    # Stored as JSON: {"landmarks": [...], "angles": {...}, ...}
    pose_data = Column(JSON, nullable=False)

    # Form feedback
    feedback = Column(Text)  # Detailed feedback message
    accuracy_score = Column(Float, default=0.0)  # 0-100

    # Error detection
    errors_detected = Column(JSON)  # List of error codes/types
    error_severity = Column(String(20))  # low, medium, high

    # Timing
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    frame_number = Column(Integer)  # Frame number in the video stream

    # Relations
    session = relationship("WorkoutSession", back_populates="form_analysis_events")
    exercise = relationship("Exercise", back_populates="form_analysis_events")
