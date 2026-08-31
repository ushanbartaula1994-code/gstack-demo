"""
Workout routes (issue #11 stub - actual handlers in issues #14-#16)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/")
async def list_workouts_placeholder():
    """Placeholder - real handlers implemented in issues #14-#16"""
    return {"message": "workouts endpoint - see issues #14-#16"}
