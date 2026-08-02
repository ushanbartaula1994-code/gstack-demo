"""
Application settings using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "AI Fitness Coach API"
    APP_VERSION: str = "0.1.0"
    API_PORT: int = 8000
    API_HOST: str = "localhost"

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://aifitness:aifitness2024@localhost:5432/aifitnesscoach"

    # Authentication settings
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60
    JWT_REFRESH_EXPIRY_DAYS: int = 7

    # CORS settings
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Stripe settings (optional)
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Claude API settings (optional)
    CLAUDE_API_KEY: str = ""

    # Supabase Auth (optional)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # Model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()