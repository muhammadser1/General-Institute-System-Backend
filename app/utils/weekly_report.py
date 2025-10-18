"""
Weekly lesson report utilities
"""
import csv
import io
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.utils.email import send_email
from app.core.config import config
from app.db.mongodb import get_database


def export_lessons_to_csv(lessons: List[Dict[str, Any]]) -> str:
    """
    Export lessons to CSV in memory (no file writes)
    
    Args:
        lessons: List of lesson dictionaries
        
    Returns:
        CSV content as string
    """
    if not lessons:
        return ""
    
    buf = io.StringIO()
    
    # Define headers with nice formatting
    headers = [
        "Lesson ID",
        "Title",
        "Subject",
        "Teacher",
        "Type",
        "Status",
        "Scheduled Date",
        "Duration (min)",
        "Duration (hrs)",
        "Students Count",
        "Max Students",
        "Notes",
        "Homework",
        "Created At",
        "Completed At"
    ]
    
    writer = csv.DictWriter(buf, fieldnames=headers)
    writer.writeheader()
    
    for lesson in lessons:
        # Format scheduled date
        scheduled_date = ""
        if lesson.get("scheduled_date"):
            if isinstance(lesson["scheduled_date"], datetime):
                scheduled_date = lesson["scheduled_date"].strftime("%Y-%m-%d %H:%M")
            else:
                scheduled_date = str(lesson["scheduled_date"])
        
        # Format created at
        created_at = ""
        if lesson.get("created_at"):
            if isinstance(lesson["created_at"], datetime):
                created_at = lesson["created_at"].strftime("%Y-%m-%d %H:%M")
            else:
                created_at = str(lesson["created_at"])
        
        # Format completed at
        completed_at = ""
        if lesson.get("completed_at"):
            if isinstance(lesson["completed_at"], datetime):
                completed_at = lesson["completed_at"].strftime("%Y-%m-%d %H:%M")
            else:
                completed_at = str(lesson["completed_at"])
        
        # Calculate duration in hours
        duration_hours = round(lesson.get("duration_minutes", 0) / 60, 2) if lesson.get("duration_minutes") else 0
        
        # Get student count
        students_count = len(lesson.get("students", []))
        
        # Write row
        row = {
            "Lesson ID": lesson.get("_id", ""),
            "Title": lesson.get("title", ""),
            "Subject": lesson.get("subject", ""),
            "Teacher": lesson.get("teacher_name", ""),
            "Type": lesson.get("lesson_type", "").upper() if lesson.get("lesson_type") else "",
            "Status": lesson.get("status", "").upper() if lesson.get("status") else "",
            "Scheduled Date": scheduled_date,
            "Duration (min)": lesson.get("duration_minutes", ""),
            "Duration (hrs)": duration_hours,
            "Students Count": students_count,
            "Max Students": lesson.get("max_students", ""),
            "Notes": lesson.get("notes", ""),
            "Homework": lesson.get("homework", ""),
            "Created At": created_at,
            "Completed At": completed_at
        }
        writer.writerow(row)
    
    buf.seek(0)
    return buf.getvalue()


def get_lessons_for_period(start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """
    Get all lessons for a specific time period
    
    Args:
        start_date: Start of the period
        end_date: End of the period
        
    Returns:
        List of lesson dictionaries
    """
    db = get_database()
    lessons_collection = db["lessons"]
    
    # Query lessons within the period
    lessons = lessons_collection.find({
        "scheduled_date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }).sort("scheduled_date", 1)  # Sort by date ascending
    
    return list(lessons)


def send_weekly_lesson_report() -> bool:
    """
    Send weekly lesson report via email with CSV attachment
    
    Returns:
        True if email sent successfully
    """
    if not config.EMAIL_TO:
        print("⚠️  EMAIL_TO not configured. Skipping weekly report.")
        return False
    
    # Calculate date range (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    # Get lessons for the period
    lessons = get_lessons_for_period(start_date, end_date)
    
    # Generate CSV
    csv_content = export_lessons_to_csv(lessons)
    
    if not csv_content:
        print("⚠️  No lessons found for the period. Skipping report.")
        return False
    
    # Calculate statistics
    total_lessons = len(lessons)
    total_minutes = sum(lesson.get("duration_minutes", 0) for lesson in lessons)
    total_hours = round(total_minutes / 60, 2)
    
    completed_lessons = len([l for l in lessons if l.get("status") == "completed"])
    pending_lessons = len([l for l in lessons if l.get("status") == "pending"])
    cancelled_lessons = len([l for l in lessons if l.get("status") == "cancelled"])
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"weekly_lessons_report_{timestamp}.csv"
    
    # Email subject
    subject = f"📊 Weekly Lesson Report - {config.APP_NAME}"
    
    # Email body with statistics
    body = f"""
Weekly Lesson Report

Report Period: {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📈 SUMMARY:
===========
Total Lessons: {total_lessons}
Total Hours: {total_hours} hours

Status Breakdown:
- Completed: {completed_lessons}
- Pending: {pending_lessons}
- Cancelled: {cancelled_lessons}

📎 ATTACHMENT:
==============
Please find the detailed lesson report in the attached CSV file.

The CSV includes:
- Lesson details (ID, Title, Subject, Teacher)
- Scheduling information (Date, Duration)
- Student information (Count, Max capacity)
- Status and completion details
- Notes and homework assignments

---
This is an automated weekly report from {config.APP_NAME}
"""
    
    # Send email with CSV attachment
    return send_email(subject, body, config.EMAIL_TO, attachments=[(filename, csv_content)])


def send_weekly_report_job():
    """
    Job function for scheduled weekly reports
    This will be called by the scheduler
    """
    print(f"📅 Running weekly lesson report job...")
    result = send_weekly_lesson_report()
    if result:
        print(f"✅ Weekly lesson report sent successfully")
    else:
        print(f"❌ Failed to send weekly lesson report")
    return result

