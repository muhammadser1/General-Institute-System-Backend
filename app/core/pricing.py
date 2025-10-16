"""
Subject pricing configuration for teacher payments.
NOW USES DATABASE INSTEAD OF HARDCODED VALUES!

Admins manage pricing through API endpoints.
This module provides helper functions to fetch pricing from database.
"""

from typing import Optional
from app.db import mongo_db
from app.models.pricing import Pricing


# Default prices (fallback if subject not found in database)
DEFAULT_INDIVIDUAL_PRICE = 45.0
DEFAULT_GROUP_PRICE = 28.0
DEFAULT_CURRENCY = "USD"


def get_subject_price(subject: str, lesson_type: str = "individual") -> float:
    """
    Get the price per hour for a specific subject and lesson type from DATABASE.
    
    Args:
        subject: Subject name (e.g., "Math", "Arabic")
        lesson_type: "individual" or "group"
    
    Returns:
        Price per hour for the subject and lesson type
    """
    # Fetch from database
    pricing = Pricing.find_by_subject(subject, mongo_db.pricing_collection)
    
    if pricing:
        return pricing.get_price(lesson_type)
    
    # Fallback to defaults if not found
    return DEFAULT_INDIVIDUAL_PRICE if lesson_type.lower() == "individual" else DEFAULT_GROUP_PRICE


def calculate_subject_earnings(hours: float, subject: str, lesson_type: str = "individual") -> float:
    """
    Calculate earnings for a specific subject and lesson type.
    
    Args:
        hours: Total hours taught
        subject: Subject name
        lesson_type: "individual" or "group"
    
    Returns:
        Total earnings for this subject
    """
    price_per_hour = get_subject_price(subject, lesson_type)
    return round(hours * price_per_hour, 2)


def get_all_subject_prices() -> dict:
    """
    Get all subject prices from DATABASE for admin reference.
    
    Returns:
        Dictionary of all subject prices (with individual and group rates)
    """
    pricing_list = Pricing.get_all_active(mongo_db.pricing_collection)
    
    result = {}
    for pricing in pricing_list:
        result[pricing.subject.lower()] = {
            "individual": pricing.individual_price,
            "group": pricing.group_price,
            "currency": pricing.currency
        }
    
    return result


def get_price_with_currency(subject: str, lesson_type: str = "individual") -> tuple[float, str]:
    """
    Get price and currency for a subject and lesson type.
    
    Args:
        subject: Subject name
        lesson_type: "individual" or "group"
    
    Returns:
        Tuple of (price, currency)
    """
    pricing = Pricing.find_by_subject(subject, mongo_db.pricing_collection)
    
    if pricing:
        return (pricing.get_price(lesson_type), pricing.currency)
    
    # Fallback
    price = DEFAULT_INDIVIDUAL_PRICE if lesson_type.lower() == "individual" else DEFAULT_GROUP_PRICE
    return (price, DEFAULT_CURRENCY)
