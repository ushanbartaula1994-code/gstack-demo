"""
Main FastAPI application for AI Fitness Coach
Issue #11: Configure CORS and API routes structure.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.middleware import register_error_handlers

# Domain routers
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.exercises import router as exercises_router
from app.routes.workouts import router as workouts_router
from app.routes.form_analysis import router as form_analysis_router
from app.routes.progress import router as progress_router
from app.routes.stripe import router as stripe_router

logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for AI Fitness Coach - Adaptive workout programs with real-time form feedback",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register error handlers first so they wrap all routes
register_error_handlers(app)

# CORS — allow configured origins (comma-separated list in settings)
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount every domain router under /api/v1
API_V1_PREFIX = "/api/v1"
app.include_router(health_router, prefix=API_V1_PREFIX)
app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(users_router, prefix=API_V1_PREFIX)
app.include_router(exercises_router, prefix=API_V1_PREFIX)
app.include_router(workouts_router, prefix=API_V1_PREFIX)
app.include_router(form_analysis_router, prefix=API_V1_PREFIX)
app.include_router(progress_router, prefix=API_V1_PREFIX)
app.include_router(stripe_router, prefix=API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api": API_V1_PREFIX,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
