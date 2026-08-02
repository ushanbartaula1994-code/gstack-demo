"""
Workout schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class WorkoutGenerateRequest(BaseModel):
    """Schema for workout generation request"""
    workout_type: str = Field(default="strength", description="Type of workout")
    duration_minutes: int = Field(default=30, ge=10, le=90, description="Workout duration in minutes")
    fitness_level: str = Field(default="beginner", description="User's fitness level")
    equipment: str = Field(default="bodyweight", description="Available equipment")
    goals: Optional[str] = Field(default=None, description="Fitness goals")
    available_days: int = Field(default=3, ge=1, le=7, description="Days available per week")


class WorkoutGenerateResponse(BaseModel):
    """Schema for workout generation response"""
    workout_id: str
    title: str
    description: Optional[str] = None
    workout_type: str
    total_duration: int
    estimated_calories: int
    exercises: List[dict]
    recommended_frequency: str


class WorkoutResponse(BaseModel):
    """Schema for workout response"""
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    workout_type: Optional[str] = None
    total_duration: Optional[int] = None
    estimated_calories: Optional[int] = None
    is_completed: bool = False
    completed_at: Optional[str] = None
    rating: Optional[int] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class WorkoutListResponse(BaseModel):
    """Schema for list of workouts"""
    workouts: List[WorkoutResponse]
    count: int