"""
Form analysis routes (issue #11 stub - actual handlers in issues #19-#24)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/form-analysis", tags=["form-analysis"])


@router.get("/")
async def list_form_analysis_placeholder():
    """Placeholder - real handlers implemented in issues #19-#24"""
    return {"message": "form-analysis endpoint - see issues #19-#24"}
