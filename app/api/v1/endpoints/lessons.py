from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId
from app.schemas.lesson import (
    LessonCreate,
    LessonResponse,
    LessonUpdate,
    LessonsStatsResponse,
    StudentInfo,
    LessonType,
)
from app.api.deps import get_current_user, get_current_admin, get_current_teacher
from app.db import mongo_db

router = APIRouter()


# # ==================== TEACHER ENDPOINTS ====================

# @router.post("/submit", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
# def submit_lesson(
#     lesson_data: LessonCreate,
#     current_user: Dict = Depends(get_current_teacher)
# ):
#     """
#     Teacher creates a new lesson (individual or group) - starts as pending
#     """
#     teacher_name = f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}".strip()
#     if not teacher_name:
#         teacher_name = current_user["username"]
    
#     new_lesson = {
#         "teacher_id": str(current_user["_id"]),
#         "teacher_name": teacher_name,
#         "title": lesson_data.title,
#         "description": lesson_data.description,
#         "lesson_type": lesson_data.lesson_type.value,
#         "subject": lesson_data.subject,
#         "scheduled_date": lesson_data.scheduled_date,
#         "duration_minutes": lesson_data.duration_minutes,
#         "max_students": lesson_data.max_students,
#         "status": "pending",  # Scheduled lesson, not yet completed
#         "students": [student.model_dump() for student in (lesson_data.students or [])],
#         "notes": lesson_data.notes,
#         "homework": lesson_data.homework,
#         "created_at": datetime.utcnow(),
#         "updated_at": None,
#         "completed_at": None
#     }
    
#     result = mongo_db.lessons_collection.insert_one(new_lesson)
#     new_lesson["_id"] = result.inserted_id
    
#     return LessonResponse(
#         id=str(new_lesson["_id"]),
#         teacher_id=new_lesson["teacher_id"],
#         teacher_name=new_lesson["teacher_name"],
#         title=new_lesson["title"],
#         description=new_lesson.get("description"),
#         lesson_type=new_lesson["lesson_type"],
#         subject=new_lesson["subject"],
#         scheduled_date=new_lesson["scheduled_date"],
#         duration_minutes=new_lesson["duration_minutes"],
#         max_students=new_lesson.get("max_students"),
#         status=new_lesson["status"],
#         students=[StudentInfo(**s) for s in new_lesson.get("students", [])],
#         notes=new_lesson.get("notes"),
#         homework=new_lesson.get("homework"),
#         created_at=new_lesson["created_at"],
#         updated_at=new_lesson.get("updated_at"),
#         completed_at=new_lesson.get("completed_at"),
#     )


# @router.get("/my-lessons", response_model=LessonsStatsResponse)
# def get_my_lessons(
#     current_user: Dict = Depends(get_current_teacher),
#     lesson_type: Optional[str] = Query(None, description="Filter by: individual or group"),
#     lesson_status: Optional[str] = Query(None, description="Filter by: pending, completed, cancelled"),
#     student_name: Optional[str] = Query(None, description="Filter by student name"),
#     month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
#     year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year"),
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, ge=1, le=1000),
# ):
#     """
#     Teacher gets their own lessons with filters and total hours
#     - Filter by: type (individual/group), status, student name, month, year
#     - Returns: lessons + total_lessons + total_hours
#     """
#     query = {"teacher_id": str(current_user["_id"])}
    
#     # Type filter (individual/group)
#     if lesson_type:
#         query["lesson_type"] = lesson_type
    
#     # Status filter
#     if lesson_status:
#         query["status"] = lesson_status
    
#     # Student name filter (case-insensitive)
#     if student_name:
#         query["students.student_name"] = {"$regex": student_name, "$options": "i"}
    
#     # Date filter (month/year)
#     if month or year:
#         date_query = {}
#         if year:
#             date_query["$gte"] = datetime(year, month or 1, 1)
#             if month:
#                 if month == 12:
#                     date_query["$lt"] = datetime(year + 1, 1, 1)
#                 else:
#                     date_query["$lt"] = datetime(year, month + 1, 1)
#             else:
#                 date_query["$lt"] = datetime(year + 1, 1, 1)
#         query["scheduled_date"] = date_query
    
#     # Get lessons
#     lessons = list(mongo_db.lessons_collection.find(query).skip(skip).limit(limit).sort("scheduled_date", -1))
    
#     # Calculate total hours
#     total_minutes = sum(lesson.get("duration_minutes", 0) for lesson in lessons)
#     total_hours = round(total_minutes / 60, 2)
    
#     # Convert to response
#     lesson_responses = [
#         LessonResponse(
#             id=str(lesson["_id"]),
#             teacher_id=lesson["teacher_id"],
#             teacher_name=lesson["teacher_name"],
#             title=lesson["title"],
#             description=lesson.get("description"),
#             lesson_type=lesson["lesson_type"],
#             subject=lesson["subject"],
#             scheduled_date=lesson["scheduled_date"],
#             duration_minutes=lesson["duration_minutes"],
#             max_students=lesson.get("max_students"),
#             status=lesson["status"],
#             students=[StudentInfo(**s) for s in lesson.get("students", [])],
#             notes=lesson.get("notes"),
#             homework=lesson.get("homework"),
#             created_at=lesson["created_at"],
#             updated_at=lesson.get("updated_at"),
#             completed_at=lesson.get("completed_at"),
#         )
#         for lesson in lessons
#     ]
    
#     return LessonsStatsResponse(
#         total_lessons=len(lessons),
#         total_hours=total_hours,
#         lessons=lesson_responses
#     )


# @router.get("/dashboard-stats")
# def get_dashboard_stats(
#     current_user: Dict = Depends(get_current_teacher),
#     month: Optional[int] = Query(None, ge=1, le=12),
#     year: Optional[int] = Query(None, ge=2000, le=2100),
# ):
#     """
#     Teacher dashboard overview with statistics
#     - Optionally filtered by month/year
#     - Shows: pending, completed, cancelled counts and hours
#     """
#     query = {"teacher_id": str(current_user["_id"])}
    
#     # Date filter
#     if month or year:
#         date_query = {}
#         if year:
#             date_query["$gte"] = datetime(year, month or 1, 1)
#             if month:
#                 if month == 12:
#                     date_query["$lt"] = datetime(year + 1, 1, 1)
#                 else:
#                     date_query["$lt"] = datetime(year, month + 1, 1)
#             else:
#                 date_query["$lt"] = datetime(year + 1, 1, 1)
#         query["scheduled_date"] = date_query
    
#     # Get all lessons for this teacher
#     all_lessons = list(mongo_db.lessons_collection.find(query))
    
#     # Calculate stats by status
#     stats = {
#         "pending": {"count": 0, "hours": 0},
#         "completed": {"count": 0, "hours": 0},
#         "cancelled": {"count": 0, "hours": 0},
#     }
    
#     for lesson in all_lessons:
#         lesson_status = lesson.get("status", "pending")
#         if lesson_status in stats:
#             stats[lesson_status]["count"] += 1
#             stats[lesson_status]["hours"] += lesson.get("duration_minutes", 0) / 60
    
#     # Round hours
#     for stat_status in stats:
#         stats[stat_status]["hours"] = round(stats[stat_status]["hours"], 2)
    
#     # Calculate totals
#     total_lessons = sum(s["count"] for s in stats.values())
#     total_hours = round(sum(s["hours"] for s in stats.values()), 2)
    
#     return {
#         "total_lessons": total_lessons,
#         "total_hours": total_hours,
#         "by_status": stats,
#         "filter": {
#             "month": month,
#             "year": year
#         }
#     }


# @router.put("/update-lesson/{lesson_id}", response_model=LessonResponse)
# def update_lesson(
#     lesson_id: str,
#     lesson_update: LessonUpdate,
#     current_user: Dict = Depends(get_current_teacher)
# ):
#     """
#     Teacher updates their own lesson
#     - Can only update if status is pending (NOT completed or cancelled)
#     """
#     try:
#         lesson = mongo_db.lessons_collection.find_one({"_id": ObjectId(lesson_id)})
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid lesson ID",
#         )
    
#     if not lesson:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Lesson not found",
#         )
    
#     # Check ownership
#     if lesson["teacher_id"] != str(current_user["_id"]):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to update this lesson",
#         )
    
#     # Check if can be updated
#     if lesson["status"] in ["completed", "cancelled"]:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Cannot update {lesson['status']} lesson",
#         )
    
#     # Prepare update
#     update_data = lesson_update.model_dump(exclude_unset=True)
    
#     if "students" in update_data and update_data["students"]:
#         update_data["students"] = [s.model_dump() if hasattr(s, 'model_dump') else s for s in update_data["students"]]
    
#     update_data["updated_at"] = datetime.utcnow()
    
#     # If status changed to completed, set completed_at
#     if update_data.get("status") == "completed":
#         update_data["completed_at"] = datetime.utcnow()
    
#     # Update
#     mongo_db.lessons_collection.update_one(
#         {"_id": ObjectId(lesson_id)},
#         {"$set": update_data}
#     )
    
#     # Get updated lesson
#     updated_lesson = mongo_db.lessons_collection.find_one({"_id": ObjectId(lesson_id)})
    
#     return LessonResponse(
#         id=str(updated_lesson["_id"]),
#         teacher_id=updated_lesson["teacher_id"],
#         teacher_name=updated_lesson["teacher_name"],
#         title=updated_lesson["title"],
#         description=updated_lesson.get("description"),
#         lesson_type=updated_lesson["lesson_type"],
#         subject=updated_lesson["subject"],
#         scheduled_date=updated_lesson["scheduled_date"],
#         duration_minutes=updated_lesson["duration_minutes"],
#         max_students=updated_lesson.get("max_students"),
#         status=updated_lesson["status"],
#         students=[StudentInfo(**s) for s in updated_lesson.get("students", [])],
#         notes=updated_lesson.get("notes"),
#         homework=updated_lesson.get("homework"),
#         created_at=updated_lesson["created_at"],
#         updated_at=updated_lesson.get("updated_at"),
#         completed_at=updated_lesson.get("completed_at"),
#     )


# @router.delete("/delete-lesson/{lesson_id}")
# def delete_lesson(
#     lesson_id: str,
#     current_user: Dict = Depends(get_current_teacher)
# ):
#     """
#     Teacher 'deletes' their own lesson (soft delete - changes status to cancelled)
#     - Can only delete pending lessons
#     """
#     try:
#         lesson = mongo_db.lessons_collection.find_one({"_id": ObjectId(lesson_id)})
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid lesson ID",
#         )
    
#     if not lesson:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Lesson not found",
#         )
    
#     # Check ownership
#     if lesson["teacher_id"] != str(current_user["_id"]):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to delete this lesson",
#         )
    
#     # Can only delete pending lessons
#     if lesson["status"] != "pending":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Cannot delete {lesson['status']} lesson. Only pending lessons can be deleted.",
#         )
    
#     # Soft delete - change status to cancelled
#     mongo_db.lessons_collection.update_one(
#         {"_id": ObjectId(lesson_id)},
#         {"$set": {
#             "status": "cancelled",
#             "updated_at": datetime.utcnow()
#         }}
#     )
    
#     return {"message": "Lesson cancelled successfully"}


# # ==================== ADMIN ENDPOINTS ====================

# @router.get("/admin/all-lessons", response_model=LessonsStatsResponse)
# def admin_get_all_lessons(
#     current_user: Dict = Depends(get_current_admin),
#     lesson_type: Optional[str] = Query(None, description="Filter by: individual or group"),
#     lesson_status: Optional[str] = Query(None, description="Filter by: pending, completed, cancelled"),
#     teacher_id: Optional[str] = Query(None, description="Filter by specific teacher"),
#     student_name: Optional[str] = Query(None, description="Filter by student name"),
#     month: Optional[int] = Query(None, ge=1, le=12),
#     year: Optional[int] = Query(None, ge=2000, le=2100),
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, ge=1, le=1000),
# ):
#     """
#     Admin gets all lessons with filters
#     - Can filter by: type, status, teacher, student name, month, year
#     - Returns: lessons + total_lessons + total_hours
#     """
#     query = {}
    
#     if lesson_type:
#         query["lesson_type"] = lesson_type
    
#     if lesson_status:
#         query["status"] = lesson_status
    
#     if teacher_id:
#         query["teacher_id"] = teacher_id
    
#     if student_name:
#         query["students.student_name"] = {"$regex": student_name, "$options": "i"}
    
#     if month or year:
#         date_query = {}
#         if year:
#             date_query["$gte"] = datetime(year, month or 1, 1)
#             if month:
#                 if month == 12:
#                     date_query["$lt"] = datetime(year + 1, 1, 1)
#                 else:
#                     date_query["$lt"] = datetime(year, month + 1, 1)
#             else:
#                 date_query["$lt"] = datetime(year + 1, 1, 1)
#         query["scheduled_date"] = date_query
    
#     lessons = list(mongo_db.lessons_collection.find(query).skip(skip).limit(limit).sort("scheduled_date", -1))
    
#     total_minutes = sum(lesson.get("duration_minutes", 0) for lesson in lessons)
#     total_hours = round(total_minutes / 60, 2)
    
#     lesson_responses = [
#         LessonResponse(
#             id=str(lesson["_id"]),
#             teacher_id=lesson["teacher_id"],
#             teacher_name=lesson["teacher_name"],
#             title=lesson["title"],
#             description=lesson.get("description"),
#             lesson_type=lesson["lesson_type"],
#             subject=lesson["subject"],
#             scheduled_date=lesson["scheduled_date"],
#             duration_minutes=lesson["duration_minutes"],
#             max_students=lesson.get("max_students"),
#             status=lesson["status"],
#             students=[StudentInfo(**s) for s in lesson.get("students", [])],
#             notes=lesson.get("notes"),
#             homework=lesson.get("homework"),
#             created_at=lesson["created_at"],
#             updated_at=lesson.get("updated_at"),
#             completed_at=lesson.get("completed_at"),
#         )
#         for lesson in lessons
#     ]
    
#     return LessonsStatsResponse(
#         total_lessons=len(lessons),
#         total_hours=total_hours,
#         lessons=lesson_responses
#     )


# @router.delete("/admin/delete-lesson/{lesson_id}")
# def admin_delete_lesson(
#     lesson_id: str,
#     current_user: Dict = Depends(get_current_admin)
# ):
#     """
#     Admin 'deletes' any lesson (soft delete - changes status to cancelled)
#     """
#     try:
#         lesson = mongo_db.lessons_collection.find_one({"_id": ObjectId(lesson_id)})
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid lesson ID",
#         )
    
#     if not lesson:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Lesson not found",
#         )
    
#     # Soft delete
#     mongo_db.lessons_collection.update_one(
#         {"_id": ObjectId(lesson_id)},
#         {"$set": {
#             "status": "cancelled",
#             "updated_at": datetime.utcnow()
#         }}
#     )
    
#     return {"message": "Lesson cancelled successfully"}


# @router.get("/{lesson_id}", response_model=LessonResponse)
# def get_lesson_by_id(
#     lesson_id: str,
#     current_user: Dict = Depends(get_current_user)
# ):
#     """
#     Get a specific lesson by ID
#     - Teachers can only see their own
#     - Admins can see any
#     """
#     try:
#         lesson = mongo_db.lessons_collection.find_one({"_id": ObjectId(lesson_id)})
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid lesson ID",
#         )
    
#     if not lesson:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Lesson not found",
#         )
    
#     # Check permission
#     if current_user["role"] == "teacher" and lesson["teacher_id"] != str(current_user["_id"]):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to access this lesson",
#         )
    
#     return LessonResponse(
#         id=str(lesson["_id"]),
#         teacher_id=lesson["teacher_id"],
#         teacher_name=lesson["teacher_name"],
#         title=lesson["title"],
#         description=lesson.get("description"),
#         lesson_type=lesson["lesson_type"],
#         subject=lesson["subject"],
#         scheduled_date=lesson["scheduled_date"],
#         duration_minutes=lesson["duration_minutes"],
#         max_students=lesson.get("max_students"),
#         status=lesson["status"],
#         students=[StudentInfo(**s) for s in lesson.get("students", [])],
#         notes=lesson.get("notes"),
#         homework=lesson.get("homework"),
#         created_at=lesson["created_at"],
#         updated_at=lesson.get("updated_at"),
#         completed_at=lesson.get("completed_at"),
#     )
