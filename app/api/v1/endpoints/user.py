from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from app.schemas.user import (
    LoginRequest, 
    LoginResponse, 
    UserSummary,
    LogoutResponse, 
    TeacherSignup, 
    UserResponse,
    UserRole,
    UserStatus
)
from app.models.user import User
from app.db import mongo_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    """
    User login - returns access token and user info
    """
    # Find user by username using model method
    user = User.find_by_username(credentials.username, mongo_db.users_collection)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Check if user is active using model method
    if not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User account is {user.status.value}",
        )
    
    # Update last login using model method
    user.update_last_login()
    user.update_in_db(mongo_db.users_collection, {"last_login": user.last_login})
    
    # Create access token
    token_data = {
        "sub": str(user._id),
        "username": user.username,
        "role": user.role.value,
    }
    access_token = create_access_token(token_data)
    
    # Return login response with token and user info
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSummary(
            id=str(user._id),
            username=user.username,
            role=user.role,
            status=user.status,
            last_login=user.last_login
        )
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(current_user: dict = Depends(get_current_user)):
    """
    User logout (client should delete token)
    """
    return LogoutResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user's full profile
    """
    return UserResponse(
        id=str(current_user["_id"]),
        username=current_user["username"],
        role=current_user["role"],
        status=current_user.get("status", "active"),
        email=current_user.get("email"),
        first_name=current_user.get("first_name"),
        last_name=current_user.get("last_name"),
        phone=current_user.get("phone"),
        birthdate=current_user.get("birthdate"),
        last_login=current_user.get("last_login"),
        created_at=current_user.get("created_at", datetime.utcnow()),
        updated_at=current_user.get("updated_at"),
    )


@router.post("/teacher/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def teacher_signup(signup_data: TeacherSignup):
    """
    Teacher self-registration (public endpoint)
    Teachers can create their own account
    """
    # Check if username already exists using model method
    if User.username_exists(signup_data.username, mongo_db.users_collection):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # Check if email already exists using model method
    if User.email_exists(signup_data.email, mongo_db.users_collection):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    
    # Create new teacher using User model
    new_teacher = User(
        username=signup_data.username,
        hashed_password=get_password_hash(signup_data.password),
        role=UserRole.TEACHER,  # Always teacher for self-signup
        status=UserStatus.ACTIVE,  # Active by default
        email=signup_data.email,
        first_name=signup_data.first_name,
        last_name=signup_data.last_name,
        phone=signup_data.phone,
        birthdate=signup_data.birthdate,
    )
    
    # Save to database using model method
    new_teacher.save(mongo_db.users_collection)
    
    # Return user response
    return UserResponse(
        id=new_teacher._id,
        username=new_teacher.username,
        role=new_teacher.role,
        status=new_teacher.status,
        email=new_teacher.email,
        first_name=new_teacher.first_name,
        last_name=new_teacher.last_name,
        phone=new_teacher.phone,
        birthdate=new_teacher.birthdate,
        last_login=new_teacher.last_login,
        created_at=new_teacher.created_at,
        updated_at=new_teacher.updated_at,
    )

