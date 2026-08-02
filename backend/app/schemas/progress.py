"""
Progress schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date


class ProgressMetricsResponse(BaseModel):
    """Schema for progress metrics response"""
    id: str
    user_id: str
    record_date: date
    week_number: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    workouts_completed: int = 0
    total_duration_minutes: int = 0
    total_sets: int = 0
    total_exercises: int = 0
    average_form_score: float = 0.0
    consistency_score: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    goals_progress: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ProgressSummaryResponse(BaseModel):
    """Schema for progress summary"""
    total_workouts: int = 0
    total_duration: int = 0
    avg_form_score: float = 0.0
    consistency_score: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    weekly_progress: Optional[Dict[str, Any]] = None


class ProgressResponse(BaseModel):
    """Schema for progress response"""
    metrics: ProgressMetricsResponse
    summary: ProgressSummaryResponse

    class Config:
        from_attributes = True