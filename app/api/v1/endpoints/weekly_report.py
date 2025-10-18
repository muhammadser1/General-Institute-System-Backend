"""
Weekly report endpoints
"""
from fastapi import APIRouter, Depends
from app.api.deps import get_current_admin
from app.schemas.user import UserResponse
from app.utils.weekly_report import send_weekly_lesson_report

router = APIRouter()


@router.post("/send-weekly-report")
async def trigger_weekly_report(
    current_admin: UserResponse = Depends(get_current_admin)
):
    """
    Manually trigger weekly lesson report
    Requires admin authentication
    """
    result = send_weekly_lesson_report()
    
    if result:
        return {
            "success": True,
            "message": "Weekly lesson report sent successfully",
            "recipient": "EMAIL_TO configured in .env",
            "triggered_by": current_admin.email
        }
    else:
        return {
            "success": False,
            "message": "Failed to send weekly lesson report. Check logs for details."
        }

