"""
Main FastAPI application for AI Fitness Coach
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router

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
app.include_router(health_router, tags=["health"])
app.include_router(auth_router, tags=["authentication"])


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
