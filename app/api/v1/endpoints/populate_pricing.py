"""
Pricing Population Endpoints
Populate database with default subject pricing
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.api.deps import get_current_admin
from app.schemas.user import UserResponse
from app.models.pricing import Pricing
from app.db import mongo_db

router = APIRouter()


# Default subjects with pricing (in USD)
DEFAULT_SUBJECTS = [
    {
        "subject": "Mathematics",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    },
    {
        "subject": "Physics",
        "individual_price": 55.0,
        "group_price": 35.0,
        "currency": "USD"
    },
    {
        "subject": "Chemistry",
        "individual_price": 55.0,
        "group_price": 35.0,
        "currency": "USD"
    },
    {
        "subject": "Biology",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    },
    {
        "subject": "English",
        "individual_price": 45.0,
        "group_price": 25.0,
        "currency": "USD"
    },
    {
        "subject": "History",
        "individual_price": 40.0,
        "group_price": 25.0,
        "currency": "USD"
    },
    {
        "subject": "Geography",
        "individual_price": 40.0,
        "group_price": 25.0,
        "currency": "USD"
    },
    {
        "subject": "Computer Science",
        "individual_price": 60.0,
        "group_price": 40.0,
        "currency": "USD"
    },
    {
        "subject": "Programming",
        "individual_price": 65.0,
        "group_price": 45.0,
        "currency": "USD"
    },
    {
        "subject": "Arabic",
        "individual_price": 45.0,
        "group_price": 25.0,
        "currency": "USD"
    },
    {
        "subject": "French",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    },
    {
        "subject": "Spanish",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    },
    {
        "subject": "Music",
        "individual_price": 55.0,
        "group_price": 35.0,
        "currency": "USD"
    },
    {
        "subject": "Art",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    },
    {
        "subject": "Physical Education",
        "individual_price": 40.0,
        "group_price": 20.0,
        "currency": "USD"
    }
]


@router.post("/populate-defaults")
def populate_default_pricing(
    current_admin: dict = Depends(get_current_admin)
):
    """
    Populate database with default subject pricing
    - Only adds subjects that don't already exist
    - Admin only
    """
    created_count = 0
    skipped_count = 0
    errors = []
    
    for subject_data in DEFAULT_SUBJECTS:
        subject_name = subject_data["subject"]
        
        # Check if subject already exists
        if Pricing.subject_exists(subject_name, mongo_db.pricing_collection):
            skipped_count += 1
            continue
        
        try:
            # Create new pricing
            new_pricing = Pricing(
                subject=subject_data["subject"],
                individual_price=subject_data["individual_price"],
                group_price=subject_data["group_price"],
                currency=subject_data["currency"]
            )
            
            new_pricing.save(mongo_db.pricing_collection)
            created_count += 1
            
        except Exception as e:
            errors.append({
                "subject": subject_name,
                "error": str(e)
            })
    
    return {
        "success": True,
        "message": f"Pricing population completed",
        "created": created_count,
        "skipped": skipped_count,
        "total_subjects": len(DEFAULT_SUBJECTS),
        "errors": errors if errors else None,
        "triggered_by": current_admin.get("email", "unknown")
    }


@router.post("/populate-custom")
def populate_custom_pricing(
    subjects: List[dict],
    current_admin: dict = Depends(get_current_admin)
):
    """
    Populate database with custom subject pricing
    - Only adds subjects that don't already exist
    - Admin only
    
    Expected format:
    [
        {
            "subject": "Subject Name",
            "individual_price": 50.0,
            "group_price": 30.0,
            "currency": "USD"
        },
        ...
    ]
    """
    created_count = 0
    skipped_count = 0
    errors = []
    
    for subject_data in subjects:
        # Validate required fields
        if not all(key in subject_data for key in ["subject", "individual_price", "group_price"]):
            errors.append({
                "subject": subject_data.get("subject", "Unknown"),
                "error": "Missing required fields: subject, individual_price, group_price"
            })
            continue
        
        subject_name = subject_data["subject"]
        
        # Check if subject already exists
        if Pricing.subject_exists(subject_name, mongo_db.pricing_collection):
            skipped_count += 1
            continue
        
        try:
            # Create new pricing
            new_pricing = Pricing(
                subject=subject_data["subject"],
                individual_price=subject_data["individual_price"],
                group_price=subject_data["group_price"],
                currency=subject_data.get("currency", "USD")
            )
            
            new_pricing.save(mongo_db.pricing_collection)
            created_count += 1
            
        except Exception as e:
            errors.append({
                "subject": subject_name,
                "error": str(e)
            })
    
    return {
        "success": True,
        "message": f"Custom pricing population completed",
        "created": created_count,
        "skipped": skipped_count,
        "total_subjects": len(subjects),
        "errors": errors if errors else None,
        "triggered_by": current_admin.get("email", "unknown")
    }


@router.get("/default-subjects")
def get_default_subjects():
    """
    Get list of default subjects with pricing
    Public endpoint - no auth required
    """
    return {
        "subjects": DEFAULT_SUBJECTS,
        "total": len(DEFAULT_SUBJECTS),
        "note": "These are the default subjects that can be populated using /populate-defaults endpoint"
    }

