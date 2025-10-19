"""
Dashboard/Statistics Endpoints
Provides overview statistics for admins
"""
from fastapi import APIRouter, Depends, Query
from typing import Dict, Optional
from app.api.deps import get_current_admin
from app.db import mongo_db

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(
    current_admin: Dict = Depends(get_current_admin),
    month: Optional[int] = None,
    year: Optional[int] = None
):
    """
    Admin dashboard statistics
    Optional filters: month (1-12) and year (2000-2100)
    
    Returns:
    - Total teachers count
    - Total students count
    - Pending lessons count
    - Completed lessons count
    - Cancelled lessons count
    - Total payments count
    - Total revenue
    """
    from datetime import datetime
    
    # Count teachers (always total, not filtered by month)
    teachers_count = mongo_db.users_collection.count_documents({"role": "teacher", "status": "active"})
    
    # Count admins (always total, not filtered by month)
    admins_count = mongo_db.users_collection.count_documents({"role": "admin", "status": "active"})
    
    # Count students (always total, not filtered by month)
    students_count = mongo_db.students_collection.count_documents({"is_active": True})
    
    # Build lesson query with optional month filter
    lesson_query = {}
    if month and year:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        lesson_query["scheduled_date"] = {"$gte": start_date, "$lt": end_date}
    
    # Count lessons by status
    pending_query = {**lesson_query, "status": "pending"}
    completed_query = {**lesson_query, "status": "completed"}
    cancelled_query = {**lesson_query, "status": "cancelled"}
    
    pending_lessons_count = mongo_db.lessons_collection.count_documents(pending_query)
    completed_lessons_count = mongo_db.lessons_collection.count_documents(completed_query)
    cancelled_lessons_count = mongo_db.lessons_collection.count_documents(cancelled_query)
    total_lessons_count = mongo_db.lessons_collection.count_documents(lesson_query)
    
    # Build payment query with optional month filter
    payment_query = {}
    if month and year:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        payment_query["payment_date"] = {"$gte": start_date, "$lt": end_date}
    
    # Count payments and calculate total revenue
    payments_count = mongo_db.payments_collection.count_documents(payment_query)
    
    # Calculate total revenue from payments
    pipeline = [{"$match": payment_query}, {"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
    result = list(mongo_db.payments_collection.aggregate(pipeline))
    total_revenue = result[0]["total"] if result else 0
    
    # Count pricing subjects (always total, not filtered by month)
    pricing_count = mongo_db.pricing_collection.count_documents({"is_active": True})
    
    response = {
        "users": {
            "total_teachers": teachers_count,
            "total_admins": admins_count,
            "total_users": teachers_count + admins_count
        },
        "students": {
            "total_students": students_count
        },
        "lessons": {
            "total_lessons": total_lessons_count,
            "pending_lessons": pending_lessons_count,
            "completed_lessons": completed_lessons_count,
            "cancelled_lessons": cancelled_lessons_count
        },
        "payments": {
            "total_payments": payments_count,
            "total_revenue": round(total_revenue, 2)
        },
        "pricing": {
            "active_subjects": pricing_count
        }
    }
    
    # Add filter info if month/year provided
    if month and year:
        response["filter"] = {
            "month": month,
            "year": year,
            "note": "Statistics filtered by month and year"
        }
    
    return response


@router.get("/stats/teachers")
def get_teachers_stats(
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Get detailed statistics about teachers
    """
    # Get all active teachers
    teachers = list(mongo_db.users_collection.find({"role": "teacher", "status": "active"}))
    
    teacher_stats = []
    
    for teacher in teachers:
        teacher_id = teacher["_id"]
        teacher_name = f"{teacher.get('first_name', '')} {teacher.get('last_name', '')}".strip() or teacher["username"]
        
        # Count lessons for this teacher
        teacher_lessons = list(mongo_db.lessons_collection.find({"teacher_id": teacher_id}))
        
        pending = len([l for l in teacher_lessons if l.get("status") == "pending"])
        completed = len([l for l in teacher_lessons if l.get("status") == "completed"])
        cancelled = len([l for l in teacher_lessons if l.get("status") == "cancelled"])
        
        teacher_stats.append({
            "teacher_id": teacher_id,
            "teacher_name": teacher_name,
            "username": teacher["username"],
            "email": teacher.get("email"),
            "total_lessons": len(teacher_lessons),
            "pending_lessons": pending,
            "completed_lessons": completed,
            "cancelled_lessons": cancelled
        })
    
    return {
        "total_teachers": len(teacher_stats),
        "teachers": teacher_stats
    }


@router.get("/stats/students")
def get_students_stats(
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Get detailed statistics about students
    """
    # Get all active students
    students = list(mongo_db.students_collection.find({"is_active": True}))
    
    student_stats = []
    
    for student in students:
        student_name = student["full_name"]
        
        # Count payments for this student
        student_payments = list(mongo_db.payments_collection.find({
            "student_name": {"$regex": student_name, "$options": "i"}
        }))
        
        total_paid = sum(p.get("amount", 0) for p in student_payments)
        
        student_stats.append({
            "student_id": student["_id"],
            "student_name": student_name,
            "email": student.get("email"),
            "phone": student.get("phone"),
            "total_payments": len(student_payments),
            "total_paid": round(total_paid, 2)
        })
    
    return {
        "total_students": len(student_stats),
        "students": student_stats
    }


@router.get("/stats/lessons")
def get_lessons_stats(
    current_admin: Dict = Depends(get_current_admin),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year")
):
    """
    Get detailed statistics about lessons
    Optional filters: month (1-12) and year (2000-2100)
    """
    from datetime import datetime
    
    # Build query with optional month filter
    query = {}
    if month and year:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        query["scheduled_date"] = {"$gte": start_date, "$lt": end_date}
    
    # Count by type
    individual_query = {**query, "lesson_type": "individual"}
    group_query = {**query, "lesson_type": "group"}
    
    individual_count = mongo_db.lessons_collection.count_documents(individual_query)
    group_count = mongo_db.lessons_collection.count_documents(group_query)
    
    # Count by status
    pending_query = {**query, "status": "pending"}
    completed_query = {**query, "status": "completed"}
    cancelled_query = {**query, "status": "cancelled"}
    
    pending_count = mongo_db.lessons_collection.count_documents(pending_query)
    completed_count = mongo_db.lessons_collection.count_documents(completed_query)
    cancelled_count = mongo_db.lessons_collection.count_documents(cancelled_query)
    
    # Calculate total hours
    pipeline = [{"$match": query}, {"$group": {"_id": None, "total_minutes": {"$sum": "$duration_minutes"}}}]
    result = list(mongo_db.lessons_collection.aggregate(pipeline))
    total_minutes = result[0]["total_minutes"] if result else 0
    total_hours = round(total_minutes / 60, 2)
    
    response = {
        "by_type": {
            "individual_lessons": individual_count,
            "group_lessons": group_count,
            "total_lessons": individual_count + group_count
        },
        "by_status": {
            "pending_lessons": pending_count,
            "completed_lessons": completed_count,
            "cancelled_lessons": cancelled_count,
            "total_lessons": pending_count + completed_count + cancelled_count
        },
        "total_hours": total_hours
    }
    
    # Add filter info if month/year provided
    if month and year:
        response["filter"] = {
            "month": month,
            "year": year,
            "note": "Statistics filtered by month and year"
        }
    
    return response

