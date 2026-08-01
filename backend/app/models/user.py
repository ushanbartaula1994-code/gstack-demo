"""
User and UserProfile models
"""

from sqlalchemy import Column, String, Integer, Enum, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import BaseModel, Base


class FitnessLevel(str, PyEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class FitnessGoal(str, PyEnum):
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    FAT_LOSS = "fat_loss"
    GENERAL_FITNESS = "general_fitness"


class EquipmentType(str, PyEnum):
    BODYWEIGHT = "bodyweight"
    DUMBBELLS = "dumbbells"
    RESISTANCE_BANDS = "resistance_bands"
    FULL_GYM = "full_gym"


class User(Base):
    """User model for authentication"""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(512), nullable=True)  # Can be null for OAuth users
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Relations
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    workouts = relationship("Workout", back_populates="user")
    sessions = relationship("WorkoutSession", back_populates="user")
    progress = relationship("ProgressMetrics", back_populates="user")
    subscription = relationship("Subscription", uselist=False, back_populates="user")


class UserProfile(BaseModel):
    """User fitness profile"""

    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Fitness information
    fitness_level = Column(Enum(FitnessLevel), default=FitnessLevel.BEGINNER)
    goals = Column(Enum(FitnessGoal), nullable=True)  # For now, single goal; can be JSON array later
    equipment = Column(Enum(EquipmentType), default=EquipmentType.BODYWEIGHT)

    # Schedule
    available_days = Column(Integer, default=3)  # Days per week
    available_time = Column(Integer, default=30)  # Minutes per workout

    # Personal info
    name = Column(String(100))
    age = Column(Integer)
    height_cm = Column(Integer)  # Height in centimeters
    weight_kg = Column(Integer)  # Weight in kilograms
    gender = Column(String(20))

    # Preferences
    receive_notifications = Column(Boolean, default=True)
    theme_preference = Column(String(20), default="system")  # light, dark, system

    # Relations
    user = relationship("User", back_populates="profile")
