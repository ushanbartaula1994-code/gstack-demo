"""
Stripe webhook routes (issue #11 stub - actual handlers in issue #32)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/stripe", tags=["stripe"])


@router.post("/webhook")
async def stripe_webhook_placeholder():
    """Placeholder - real handlers implemented in issue #32"""
    return {"message": "stripe webhook - see issue #32"}
