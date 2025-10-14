from pydantic import BaseModel
from typing import List, Optional


class SubjectEarnings(BaseModel):
    """Earnings breakdown for a specific subject and lesson type."""
    subject: str
    lesson_type: str  # "individual" or "group"
    total_hours: float
    price_per_hour: float
    total_earnings: float
    lesson_count: int


class TeacherEarningsReport(BaseModel):
    """Complete earnings report for a teacher."""
    teacher_id: str
    teacher_name: str
    month: Optional[int] = None
    year: Optional[int] = None
    total_hours: float
    total_earnings: float
    by_subject: List[SubjectEarnings]
    total_lessons: int


class SubjectPriceResponse(BaseModel):
    """Subject pricing information."""
    subject: str
    individual_price: float
    group_price: float


class AllSubjectPricesResponse(BaseModel):
    """All subject prices."""
    prices: List[SubjectPriceResponse]
    default_individual_price: float
    default_group_price: float

