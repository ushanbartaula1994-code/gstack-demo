"""
Subscription model
"""

from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from app.models.base import BaseModel


class SubscriptionStatus(str, PyEnum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    TRIALING = "trialing"


class SubscriptionTier(str, PyEnum):
    FREE = "free"
    PREMIUM = "premium"


class Subscription(BaseModel):
    """User subscription information"""

    __tablename__ = "subscriptions"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Subscription details
    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)

    # Billing information
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    stripe_price_id = Column(String(255))

    # Trial period
    trial_start = Column(DateTime(timezone=True))
    trial_end = Column(DateTime(timezone=True))

    # Subscription period
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))

    # Cancellation
    cancel_at_period_end = Column(Boolean, default=False)
    canceled_at = Column(DateTime(timezone=True))

    # Usage tracking (for free tier limits)
    workouts_this_week = Column(Integer, default=0)
    last_workout_date = Column(DateTime(timezone=True))

    # Relations
    user = relationship("User", back_populates="subscription")
