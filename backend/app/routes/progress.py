"""
Progress tracking routes (issue #11 stub - actual handlers in issue #17)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/")
async def list_progress_placeholder():
    """Placeholder - real handlers implemented in issue #17"""
    return {"message": "progress endpoint - see issue #17"}
