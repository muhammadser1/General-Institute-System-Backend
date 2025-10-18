"""
Admin Pricing Management Endpoints

Admins can create, read, update, and delete subject pricing.
Teachers and public can query pricing.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Optional
from app.schemas.pricing import (
    PricingCreate,
    PricingUpdate,
    PricingResponse,
    PricingListResponse,
    PricingLookupResponse
)
from app.models.pricing import Pricing
from app.api.deps import get_current_admin, get_current_user
from app.db import mongo_db

router = APIRouter()


# ===== Admin Endpoints (CRUD) =====

@router.post("/", response_model=PricingResponse, status_code=status.HTTP_201_CREATED)
def create_pricing(
    pricing_data: PricingCreate,
    current_user: Dict = Depends(get_current_admin)
):
    """
    Admin creates new subject pricing
    - Subject must be unique
    - Both individual and group prices required
    """
    # Check if subject already exists
    if Pricing.subject_exists(pricing_data.subject, mongo_db.pricing_collection):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pricing for subject '{pricing_data.subject}' already exists"
        )
    
    # Create pricing
    new_pricing = Pricing(
        subject=pricing_data.subject,
        individual_price=pricing_data.individual_price,
        group_price=pricing_data.group_price,
        currency=pricing_data.currency
    )
    
    new_pricing.save(mongo_db.pricing_collection)
    
    return PricingResponse(
        id=new_pricing._id,
        subject=new_pricing.subject,
        individual_price=new_pricing.individual_price,
        group_price=new_pricing.group_price,
        currency=new_pricing.currency,
        is_active=new_pricing.is_active,
        created_at=new_pricing.created_at,
        updated_at=new_pricing.updated_at
    )


@router.get("/", response_model=PricingListResponse)
def get_all_pricing(
    include_inactive: bool = False,
    current_user: Dict = Depends(get_current_admin)
):
    """
    Admin gets all pricing (active and inactive)
    """
    if include_inactive:
        # Get all pricing
        pricing_docs = list(mongo_db.pricing_collection.find().sort("subject", 1))
        pricing_list = [Pricing.from_dict(doc) for doc in pricing_docs]
    else:
        # Get only active pricing
        pricing_list = Pricing.get_all_active(mongo_db.pricing_collection)
    
    pricing_responses = [
        PricingResponse(
            id=p._id,
            subject=p.subject,
            individual_price=p.individual_price,
            group_price=p.group_price,
            currency=p.currency,
            is_active=p.is_active,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in pricing_list
    ]
    
    return PricingListResponse(
        total=len(pricing_responses),
        pricing=pricing_responses
    )


@router.get("/{pricing_id}", response_model=PricingResponse)
def get_pricing_by_id(
    pricing_id: str,
    current_user: Dict = Depends(get_current_admin)
):
    """
    Admin gets pricing by ID
    """
    pricing = Pricing.find_by_id(pricing_id, mongo_db.pricing_collection)
    
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing not found"
        )
    
    return PricingResponse(
        id=pricing._id,
        subject=pricing.subject,
        individual_price=pricing.individual_price,
        group_price=pricing.group_price,
        currency=pricing.currency,
        is_active=pricing.is_active,
        created_at=pricing.created_at,
        updated_at=pricing.updated_at
    )


@router.put("/{pricing_id}", response_model=PricingResponse)
def update_pricing(
    pricing_id: str,
    pricing_update: PricingUpdate,
    current_user: Dict = Depends(get_current_admin)
):
    """
    Admin updates pricing
    - Can update prices, currency, or active status
    - Cannot change to existing subject name
    """
    pricing = Pricing.find_by_id(pricing_id, mongo_db.pricing_collection)
    
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing not found"
        )
    
    # Check if trying to change to existing subject
    if pricing_update.subject and pricing_update.subject != pricing.subject:
        if Pricing.subject_exists(pricing_update.subject, mongo_db.pricing_collection, exclude_id=pricing_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pricing for subject '{pricing_update.subject}' already exists"
            )
    
    # Update fields
    update_data = pricing_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(pricing, field):
            setattr(pricing, field, value)
    
    pricing.update_in_db(mongo_db.pricing_collection)
    
    return PricingResponse(
        id=pricing._id,
        subject=pricing.subject,
        individual_price=pricing.individual_price,
        group_price=pricing.group_price,
        currency=pricing.currency,
        is_active=pricing.is_active,
        created_at=pricing.created_at,
        updated_at=pricing.updated_at
    )


@router.delete("/{pricing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pricing(
    pricing_id: str,
    current_user: Dict = Depends(get_current_admin)
):
    """
    Admin deletes pricing
    """
    pricing = Pricing.find_by_id(pricing_id, mongo_db.pricing_collection)
    
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing not found"
        )
    
    Pricing.delete(pricing_id, mongo_db.pricing_collection)
    return None


# ===== Public/Teacher Endpoints (Query) =====

@router.get("/lookup/{subject}", response_model=PricingLookupResponse)
def lookup_price(
    subject: str,
    lesson_type: str = "individual",
    current_user: Optional[Dict] = Depends(get_current_user)
):
    """
    Lookup price for a specific subject and lesson type
    Available to all authenticated users
    """
    pricing = Pricing.find_by_subject(subject, mongo_db.pricing_collection)
    
    if not pricing:
        # Return default pricing or not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pricing not found for subject '{subject}'"
        )
    
    price_per_hour = pricing.get_price(lesson_type)
    
    return PricingLookupResponse(
        subject=pricing.subject,
        lesson_type=lesson_type,
        price_per_hour=price_per_hour,
        currency=pricing.currency,
        found=True
    )


@router.get("/public/all", response_model=List[PricingResponse])
def get_public_pricing():
    """
    Get all active pricing (public endpoint, no auth required)
    Useful for displaying pricing on public pages
    """
    pricing_list = Pricing.get_all_active(mongo_db.pricing_collection)
    
    return [
        PricingResponse(
            id=p._id,
            subject=p.subject,
            individual_price=p.individual_price,
            group_price=p.group_price,
            currency=p.currency,
            is_active=p.is_active,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in pricing_list
    ]

