"""
Pricing Schemas for API request/response validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class PricingBase(BaseModel):
    """Base pricing information"""
    subject: str = Field(..., min_length=1, max_length=100, description="Subject name (e.g., Mathematics, Physics)")
    individual_price: float = Field(..., gt=0, description="Price per hour for individual lessons")
    group_price: float = Field(..., gt=0, description="Price per hour for group lessons")
    currency: str = Field(default="USD", min_length=3, max_length=3, description="Currency code (USD, EUR, etc.)")
    
    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v):
        """Ensure subject is properly formatted"""
        return v.strip().title()  # "mathematics" -> "Mathematics"
    
    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        """Ensure currency is uppercase"""
        return v.upper()


class PricingCreate(PricingBase):
    """Schema for creating new pricing"""
    pass


class PricingUpdate(BaseModel):
    """Schema for updating pricing (all fields optional)"""
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    individual_price: Optional[float] = Field(None, gt=0)
    group_price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    is_active: Optional[bool] = None
    
    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v):
        if v:
            return v.strip().title()
        return v
    
    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        if v:
            return v.upper()
        return v


class PricingResponse(PricingBase):
    """Schema for pricing response"""
    id: str = Field(..., description="Pricing ID")
    is_active: bool = Field(default=True, description="Whether this pricing is active")
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PricingListResponse(BaseModel):
    """Schema for list of pricing"""
    total: int
    pricing: list[PricingResponse]


class PricingLookupResponse(BaseModel):
    """Schema for price lookup by subject and type"""
    subject: str
    lesson_type: str
    price_per_hour: float
    currency: str
    found: bool = True

