"""
User profile routes (issue #11 stub - actual handlers in issue #12)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users_placeholder():
    """Placeholder - real handlers implemented in issue #12"""
    return {"message": "users endpoint - see issue #12"}
