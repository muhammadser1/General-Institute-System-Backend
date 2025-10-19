"""
Student Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    """Create a new student"""
    full_name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None
    notes: Optional[str] = None


class StudentUpdate(BaseModel):
    """Update student information"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponse(BaseModel):
    """Student response"""
    id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    """List of students"""
    total: int
    students: list[StudentResponse]

