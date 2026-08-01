"""
Main FastAPI application for AI Fitness Coach
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes import health, users, exercises, workouts, progress

# Load configuration
from app.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title="AI Fitness Coach API",
    description="Backend API for AI Fitness Coach - Adaptive workout programs with real-time form feedback",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup CORS
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
app.include_router(workouts.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["progress"])


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "AI Fitness Coach API",
        "version": "0.1.0",
        "docs": "/docs",
    }


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
