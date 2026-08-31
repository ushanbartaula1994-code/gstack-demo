"""
Exercise library routes (issue #11 stub - actual handlers in issue #13)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/")
async def list_exercises_placeholder():
    """Placeholder - real handlers implemented in issue #13"""
    return {"message": "exercises endpoint - see issue #13"}
