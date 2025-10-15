from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional, Dict
from app.schemas.user import UserCreate, UserResponse, UserUpdate, ChangePasswordRequest
from app.schemas.earnings import (
    TeacherEarningsReport,
    SubjectEarnings,
    AllSubjectPricesResponse,
    SubjectPriceResponse
)
from app.core.security import get_password_hash
from app.core.pricing import (
    get_subject_price,
    calculate_subject_earnings,
    get_all_subject_prices,
    DEFAULT_INDIVIDUAL_PRICE,
    DEFAULT_GROUP_PRICE
)
from app.api.deps import get_current_admin
from app.db import mongo_db
from datetime import datetime
from bson import ObjectId
from collections import defaultdict

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin creates a new user (teacher or admin)
    Only admin can access this endpoint
    """
    # Check if username already exists
    existing_user = mongo_db.users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # If creating admin, email is required
    if user_data.role == "admin" and not user_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required for admin users",
        )
    
    # Check if email already exists (if provided)
    if user_data.email:
        existing_email = mongo_db.users_collection.find_one({"email": user_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
    
    # Create user document
    new_user = {
        "username": user_data.username,
        "password": get_password_hash(user_data.password),
        "role": user_data.role.value,
        "status": "active",
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "phone": user_data.phone,
        "birthdate": user_data.birthdate,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "updated_at": None
    }
    
    result = mongo_db.users_collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    
    return UserResponse(
        id=str(new_user["_id"]),
        username=new_user["username"],
        role=new_user["role"],
        status=new_user["status"],
        email=new_user.get("email"),
        first_name=new_user.get("first_name"),
        last_name=new_user.get("last_name"),
        phone=new_user.get("phone"),
        birthdate=new_user.get("birthdate"),
        last_login=new_user.get("last_login"),
        created_at=new_user["created_at"],
        updated_at=new_user.get("updated_at"),
    )


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    current_admin: Dict = Depends(get_current_admin),
    role: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """
    Admin gets all users with optional filters
    """
    query = {}
    if role:
        query["role"] = role
    if status:
        query["status"] = status
    
    users = list(mongo_db.users_collection.find(query).skip(skip).limit(limit))
    
    return [
        UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            role=user["role"],
            status=user["status"],
            email=user.get("email"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            phone=user.get("phone"),
            last_login=user.get("last_login"),
            created_at=user["created_at"],
            updated_at=user.get("updated_at"),
        )
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin gets a specific user
    """
    from bson import ObjectId
    
    try:
        user = mongo_db.users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user ID",
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserResponse(
        id=str(user["_id"]),
        username=user["username"],
        role=user["role"],
        status=user["status"],
        email=user.get("email"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        phone=user.get("phone"),
        last_login=user.get("last_login"),
        created_at=user["created_at"],
        updated_at=user.get("updated_at"),
    )


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin updates a user
    """
    from bson import ObjectId
    
    try:
        user = mongo_db.users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user ID",
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check username uniqueness if updating
    if "username" in update_data and update_data["username"] != user["username"]:
        existing = mongo_db.users_collection.find_one({"username": update_data["username"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
    
    # Check email uniqueness if updating
    if "email" in update_data and update_data.get("email") != user.get("email"):
        existing = mongo_db.users_collection.find_one({"email": update_data["email"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
    
    # Add updated_at timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update in database
    mongo_db.users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    # Get updated user
    updated_user = mongo_db.users_collection.find_one({"_id": ObjectId(user_id)})
    
    return UserResponse(
        id=str(updated_user["_id"]),
        username=updated_user["username"],
        role=updated_user["role"],
        status=updated_user["status"],
        email=updated_user.get("email"),
        first_name=updated_user.get("first_name"),
        last_name=updated_user.get("last_name"),
        phone=updated_user.get("phone"),
        last_login=updated_user.get("last_login"),
        created_at=updated_user["created_at"],
        updated_at=updated_user.get("updated_at"),
    )


@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: str,
    password_data: ChangePasswordRequest,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin resets a user's password
    """
    from bson import ObjectId
    
    try:
        user = mongo_db.users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user ID",
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update password
    mongo_db.users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "password": get_password_hash(password_data.new_password),
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {"message": "Password reset successfully"}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin deletes a user
    """
    from bson import ObjectId
    
    try:
        user = mongo_db.users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user ID",
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    mongo_db.users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}


@router.get("/teachers-birthdays", response_model=List[UserResponse])
def get_teachers_birthdays(
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Get teachers whose birthday is today
    """
    from datetime import date
    
    today = date.today()
    
    # Get all teachers
    teachers = list(mongo_db.users_collection.find({"role": "teacher"}))
    
    # Filter by birthday
    birthday_teachers = []
    for teacher in teachers:
        if teacher.get("birthdate"):
            birthdate = teacher["birthdate"]
            # Check if month and day match today
            if isinstance(birthdate, datetime):
                if birthdate.month == today.month and birthdate.day == today.day:
                    birthday_teachers.append(teacher)
    
    # Convert to response
    return [
        UserResponse(
            id=str(teacher["_id"]),
            username=teacher["username"],
            role=teacher["role"],
            status=teacher["status"],
            email=teacher.get("email"),
            first_name=teacher.get("first_name"),
            last_name=teacher.get("last_name"),
            phone=teacher.get("phone"),
            birthdate=teacher.get("birthdate"),
            last_login=teacher.get("last_login"),
            created_at=teacher["created_at"],
            updated_at=teacher.get("updated_at"),
        )
        for teacher in birthday_teachers
    ]


@router.get("/teacher-earnings/{teacher_id}", response_model=TeacherEarningsReport)
def get_teacher_earnings(
    teacher_id: str,
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Filter by year"),
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin gets teacher earnings breakdown by subject.
    Shows total hours per subject, price per hour, and total payment.
    Optionally filter by month and/or year.
    """
    # Verify teacher exists
    try:
        teacher = mongo_db.users_collection.find_one({"_id": ObjectId(teacher_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid teacher ID",
        )
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )
    
    if teacher["role"] != "teacher":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a teacher",
        )
    
    # Build query for lessons
    query = {
        "teacher_id": teacher_id,
        "status": {"$in": ["pending", "completed"]}  # Don't count cancelled lessons
    }
    
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
    
    # Get all lessons for this teacher
    lessons = list(mongo_db.lessons_collection.find(query))
    
    # Group by subject AND lesson_type
    subject_data = defaultdict(lambda: {"hours": 0.0, "count": 0})
    
    for lesson in lessons:
        subject = lesson.get("subject", "other")
        lesson_type = lesson.get("lesson_type", "individual")
        duration_minutes = lesson.get("duration_minutes", 0)
        hours = duration_minutes / 60
        
        # Create unique key for subject + lesson_type
        key = (subject, lesson_type)
        subject_data[key]["hours"] += hours
        subject_data[key]["count"] += 1
    
    # Calculate earnings per subject + lesson_type
    subject_earnings_list = []
    total_hours = 0.0
    total_earnings = 0.0
    
    for (subject, lesson_type), data in subject_data.items():
        hours = round(data["hours"], 2)
        price_per_hour = get_subject_price(subject, lesson_type)
        earnings = calculate_subject_earnings(hours, subject, lesson_type)
        
        subject_earnings_list.append(
            SubjectEarnings(
                subject=subject,
                lesson_type=lesson_type,
                total_hours=hours,
                price_per_hour=price_per_hour,
                total_earnings=earnings,
                lesson_count=data["count"]
            )
        )
        
        total_hours += hours
        total_earnings += earnings
    
    # Sort by subject name then lesson_type
    subject_earnings_list.sort(key=lambda x: (x.subject, x.lesson_type))
    
    teacher_name = f"{teacher.get('first_name', '')} {teacher.get('last_name', '')}".strip()
    if not teacher_name:
        teacher_name = teacher["username"]
    
    return TeacherEarningsReport(
        teacher_id=teacher_id,
        teacher_name=teacher_name,
        month=month,
        year=year,
        total_hours=round(total_hours, 2),
        total_earnings=round(total_earnings, 2),
        by_subject=subject_earnings_list,
        total_lessons=len(lessons)
    )


@router.get("/subject-prices", response_model=AllSubjectPricesResponse)
def get_subject_prices(
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin gets all subject prices for reference.
    Useful to know the pricing structure.
    """
    all_prices = get_all_subject_prices()
    
    price_list = [
        SubjectPriceResponse(
            subject=subject,
            individual_price=prices["individual"],
            group_price=prices["group"]
        )
        for subject, prices in sorted(all_prices.items())
    ]
    
    return AllSubjectPricesResponse(
        prices=price_list,
        default_individual_price=DEFAULT_INDIVIDUAL_PRICE,
        default_group_price=DEFAULT_GROUP_PRICE
    )

