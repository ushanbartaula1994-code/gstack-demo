"""
User schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import MessageResponse


class UserProfileCreate(BaseModel):
    """Schema for creating a user profile"""
    name: Optional[str] = Field(default=None, description="User's display name")
    age: Optional[int] = Field(default=None, ge=13, le=120, description="User's age")
    height_cm: Optional[int] = Field(default=None, ge=50, le=250, description="Height in centimeters")
    weight_kg: Optional[int] = Field(default=None, ge=20, le=200, description="Weight in kilograms")
    gender: Optional[str] = Field(default=None, description="User's gender")
    fitness_level: str = Field(default="beginner", description="Fitness level")
    goals: Optional[str] = Field(default=None, description="Fitness goals")
    equipment: str = Field(default="bodyweight", description="Available equipment")
    available_days: int = Field(default=3, ge=1, le=7, description="Available days per week")
    available_time: int = Field(default=30, ge=10, le=120, description="Available time per workout in minutes")
    receive_notifications: bool = Field(default=True, description="Enable email notifications")
    theme_preference: str = Field(default="system", description="Theme preference")


class UserProfileUpdate(BaseModel):
    """Schema for updating a user profile"""
    name: Optional[str] = Field(default=None, description="User's display name")
    age: Optional[int] = Field(default=None, ge=13, le=120, description="User's age")
    height_cm: Optional[int] = Field(default=None, ge=50, le=250, description="Height in centimeters")
    weight_kg: Optional[int] = Field(default=None, ge=20, le=200, description="Weight in kilograms")
    gender: Optional[str] = Field(default=None, description="User's gender")
    fitness_level: Optional[str] = Field(default=None, description="Fitness level")
    goals: Optional[str] = Field(default=None, description="Fitness goals")
    equipment: Optional[str] = Field(default=None, description="Available equipment")
    available_days: Optional[int] = Field(default=None, ge=1, le=7, description="Available days per week")
    available_time: Optional[int] = Field(default=None, ge=10, le=120, description="Available time per workout in minutes")
    receive_notifications: Optional[bool] = Field(default=None, description="Enable email notifications")
    theme_preference: Optional[str] = Field(default=None, description="Theme preference")


class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    id: str
    user_id: str
    name: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    gender: Optional[str] = None
    fitness_level: str
    goals: Optional[str] = None
    equipment: str
    available_days: int
    available_time: int
    receive_notifications: bool
    theme_preference: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True