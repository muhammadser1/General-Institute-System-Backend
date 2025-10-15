from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional, Dict
from datetime import datetime
from app.schemas.lesson import (
    LessonCreate,
    LessonResponse,
    LessonUpdate,
    LessonsStatsResponse,
    StudentInfo,
    LessonType,
    LessonStatus,
)
from app.models.lesson import Lesson
from app.models.user import User
from app.api.deps import get_current_user, get_current_admin, get_current_teacher
from app.db import mongo_db

router = APIRouter()


# ==================== TEACHER ENDPOINTS ====================

@router.post("/submit", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def submit_lesson(
    lesson_data: LessonCreate,
    current_user: Dict = Depends(get_current_teacher)
):
    """
    Teacher creates a new lesson (individual or group) - starts as pending
    """
    # Get teacher info using User model
    teacher = User.from_dict(current_user)
    teacher_name = teacher.get_full_name()
    
    # Create lesson using Lesson model
    new_lesson = Lesson(
        teacher_id=str(current_user["_id"]),
        teacher_name=teacher_name,
        title=lesson_data.title,
        description=lesson_data.description,
        lesson_type=lesson_data.lesson_type,
        subject=lesson_data.subject,
        scheduled_date=lesson_data.scheduled_date,
        duration_minutes=lesson_data.duration_minutes,
        max_students=lesson_data.max_students,
        status=LessonStatus.PENDING,
        students=[student.model_dump() for student in (lesson_data.students or [])],
        notes=lesson_data.notes,
        homework=lesson_data.homework,
    )
    
    # Save to database using model method
    new_lesson.save(mongo_db.lessons_collection)
    
    return LessonResponse(
        id=new_lesson._id,
        teacher_id=new_lesson.teacher_id,
        teacher_name=new_lesson.teacher_name,
        title=new_lesson.title,
        description=new_lesson.description,
        lesson_type=new_lesson.lesson_type,
        subject=new_lesson.subject,
        scheduled_date=new_lesson.scheduled_date,
        duration_minutes=new_lesson.duration_minutes,
        max_students=new_lesson.max_students,
        status=new_lesson.status,
        students=[StudentInfo(**s) for s in new_lesson.students],
        notes=new_lesson.notes,
        homework=new_lesson.homework,
        created_at=new_lesson.created_at,
        updated_at=new_lesson.updated_at,
        completed_at=new_lesson.completed_at,
    )


@router.get("/my-lessons", response_model=LessonsStatsResponse)
def get_my_lessons(
    current_user: Dict = Depends(get_current_teacher),
    lesson_type: Optional[str] = Query(None, description="Filter by: individual or group"),
    lesson_status: Optional[str] = Query(None, description="Filter by: pending, completed, cancelled"),
    student_name: Optional[str] = Query(None, description="Filter by student name"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Teacher gets their own lessons with filters and total hours
    - Filter by: type (individual/group), status, student name, month, year
    - Returns: lessons + total_lessons + total_hours
    """
    query = {"teacher_id": str(current_user["_id"])}
    
    # Type filter
    if lesson_type:
        query["lesson_type"] = lesson_type
    
    # Status filter
    if lesson_status:
        query["status"] = lesson_status
    
    # Student name filter
    if student_name:
        query["students.student_name"] = {"$regex": student_name, "$options": "i"}
    
    # Date filter
    if month or year:
        date_query = {}
        if year:
            date_query["$gte"] = datetime(year, month or 1, 1)
            if month:
                if month == 12:
                    date_query["$lt"] = datetime(year + 1, 1, 1)
                else:
                    date_query["$lt"] = datetime(year, month + 1, 1)
            else:
                date_query["$lt"] = datetime(year + 1, 1, 1)
        query["scheduled_date"] = date_query
    
    # Get lessons
    lessons_docs = list(mongo_db.lessons_collection.find(query).skip(skip).limit(limit).sort("scheduled_date", -1))
    lessons = [Lesson.from_dict(doc) for doc in lessons_docs]
    
    # Calculate total hours using model method
    total_hours = Lesson.calculate_total_hours(lessons)
    
    # Convert to response
    lesson_responses = [
        LessonResponse(
            id=lesson._id,
            teacher_id=lesson.teacher_id,
            teacher_name=lesson.teacher_name,
            title=lesson.title,
            description=lesson.description,
            lesson_type=lesson.lesson_type,
            subject=lesson.subject,
            scheduled_date=lesson.scheduled_date,
            duration_minutes=lesson.duration_minutes,
            max_students=lesson.max_students,
            status=lesson.status,
            students=[StudentInfo(**s) for s in lesson.students],
            notes=lesson.notes,
            homework=lesson.homework,
            created_at=lesson.created_at,
            updated_at=lesson.updated_at,
            completed_at=lesson.completed_at,
        )
        for lesson in lessons
    ]
    
    return LessonsStatsResponse(
        total_lessons=len(lessons),
        total_hours=total_hours,
        lessons=lesson_responses
    )


@router.put("/update-lesson/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: str,
    lesson_update: LessonUpdate,
    current_user: Dict = Depends(get_current_teacher)
):
    """
    Teacher updates their own lesson
    - Can only update if status is pending (NOT completed or cancelled)
    """
    # Find lesson using model method
    lesson = Lesson.find_by_id(lesson_id, mongo_db.lessons_collection)
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )
    
    # Check ownership
    if lesson.teacher_id != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this lesson",
        )
    
    # Check if can be updated using model method
    if not lesson.can_be_updated():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update {lesson.status.value} lesson. Only pending lessons can be updated.",
        )
    
    # Prepare update
    update_data = lesson_update.model_dump(exclude_unset=True)
    
    if "students" in update_data and update_data["students"]:
        update_data["students"] = [s.model_dump() if hasattr(s, 'model_dump') else s for s in update_data["students"]]
    
    if "lesson_type" in update_data:
        update_data["lesson_type"] = update_data["lesson_type"].value
    
    if "status" in update_data:
        # If marking as completed, set completed_at
        if update_data["status"] == LessonStatus.COMPLETED:
            update_data["completed_at"] = datetime.utcnow()
        update_data["status"] = update_data["status"].value
    
    # Update using model method
    lesson.update_in_db(mongo_db.lessons_collection, update_data)
    
    # Get updated lesson
    updated_lesson = Lesson.find_by_id(lesson_id, mongo_db.lessons_collection)
    
    return LessonResponse(
        id=updated_lesson._id,
        teacher_id=updated_lesson.teacher_id,
        teacher_name=updated_lesson.teacher_name,
        title=updated_lesson.title,
        description=updated_lesson.description,
        lesson_type=updated_lesson.lesson_type,
        subject=updated_lesson.subject,
        scheduled_date=updated_lesson.scheduled_date,
        duration_minutes=updated_lesson.duration_minutes,
        max_students=updated_lesson.max_students,
        status=updated_lesson.status,
        students=[StudentInfo(**s) for s in updated_lesson.students],
        notes=updated_lesson.notes,
        homework=updated_lesson.homework,
        created_at=updated_lesson.created_at,
        updated_at=updated_lesson.updated_at,
        completed_at=updated_lesson.completed_at,
    )


@router.delete("/delete-lesson/{lesson_id}")
def delete_lesson(
    lesson_id: str,
    current_user: Dict = Depends(get_current_teacher)
):
    """
    Teacher 'deletes' their own lesson (soft delete - changes status to cancelled)
    - Can only delete pending lessons
    """
    # Find lesson using model method
    lesson = Lesson.find_by_id(lesson_id, mongo_db.lessons_collection)
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )
    
    # Check ownership
    if lesson.teacher_id != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this lesson",
        )
    
    # Can only delete pending lessons
    if not lesson.is_pending():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete {lesson.status.value} lesson. Only pending lessons can be deleted.",
        )
    
    # Soft delete using model method
    lesson.delete(mongo_db.lessons_collection)
    
    return {"message": "Lesson cancelled successfully"}


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson_by_id(
    lesson_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get a specific lesson by ID
    - Teachers can only see their own
    - Admins can see any
    """
    # Find lesson using model method
    lesson = Lesson.find_by_id(lesson_id, mongo_db.lessons_collection)
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )
    
    # Check permission
    if current_user["role"] == "teacher" and lesson.teacher_id != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this lesson",
        )
    
    return LessonResponse(
        id=lesson._id,
        teacher_id=lesson.teacher_id,
        teacher_name=lesson.teacher_name,
        title=lesson.title,
        description=lesson.description,
        lesson_type=lesson.lesson_type,
        subject=lesson.subject,
        scheduled_date=lesson.scheduled_date,
        duration_minutes=lesson.duration_minutes,
        max_students=lesson.max_students,
        status=lesson.status,
        students=[StudentInfo(**s) for s in lesson.students],
        notes=lesson.notes,
        homework=lesson.homework,
        created_at=lesson.created_at,
        updated_at=lesson.updated_at,
        completed_at=lesson.completed_at,
    )
