"""
Test crash endpoint - for testing crash notifications
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/test-crash")
async def test_crash():
    """
    Test endpoint to trigger a crash and verify email notification
    Only available in development mode
    """
    raise ValueError("This is a test crash to verify email notifications are working!")

