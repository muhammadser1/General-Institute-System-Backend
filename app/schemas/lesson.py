from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


# -----------------------------------------------------------
# ENUMS
# -----------------------------------------------------------
class LessonType(str, Enum):
    """Defines whether a lesson is individual or group."""
    INDIVIDUAL = "individual"
    GROUP = "group"


class LessonStatus(str, Enum):
    """Simplified lesson life cycle."""
    PENDING = "pending"      # Scheduled lesson, not yet completed
    COMPLETED = "completed"  # Lesson finished
    CANCELLED = "cancelled"  # Soft deleted or cancelled


# -----------------------------------------------------------
# STUDENT INFO
# -----------------------------------------------------------
class StudentInfo(BaseModel):
    """Student information in a lesson."""
    student_name: str = Field(..., min_length=1, max_length=100)
    student_email: Optional[str] = None


# -----------------------------------------------------------
# LESSON MODELS
# -----------------------------------------------------------
class LessonBase(BaseModel):
    """Base lesson information shared by all models."""
    title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    lesson_type: LessonType
    scheduled_date: datetime
    duration_minutes: int = Field(..., gt=0, le=480)  # 1–480 min
    max_students: Optional[int] = Field(None, gt=0)


class LessonCreate(LessonBase):
    """Used to create a new lesson."""
    teacher_id: Optional[str] = None
    students: Optional[List[StudentInfo]] = Field(default_factory=list)
    notes: Optional[str] = None
    homework: Optional[str] = None


class LessonUpdate(BaseModel):
    """Used to edit lesson info or mark status. Can only update if NOT completed."""
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0, le=480)
    max_students: Optional[int] = Field(None, gt=0)
    students: Optional[List[StudentInfo]] = None
    status: Optional[LessonStatus] = None
    notes: Optional[str] = None
    homework: Optional[str] = None


class LessonResponse(LessonBase):
    """Returned when fetching a lesson."""
    id: str
    teacher_id: str
    teacher_name: str
    status: LessonStatus
    students: List[StudentInfo] = Field(default_factory=list)
    notes: Optional[str] = None
    homework: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LessonsStatsResponse(BaseModel):
    """Statistics for lessons with filters applied."""
    total_lessons: int
    total_hours: float
    lessons: List[LessonResponse]
