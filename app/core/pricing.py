"""
Subject pricing configuration for teacher payments.
Admins can easily update prices here.
Supports different prices for individual and group lessons.
"""

# Subject pricing in your currency (e.g., USD, EUR, etc.)
# Format: {"subject": {"individual": price, "group": price}}
# Easy to modify - just update the prices below
SUBJECT_PRICES = {
    "math": {"individual": 50.0, "group": 30.0},
    "arabic": {"individual": 60.0, "group": 35.0},
    "english": {"individual": 55.0, "group": 32.0},
    "science": {"individual": 50.0, "group": 30.0},
    "physics": {"individual": 55.0, "group": 33.0},
    "chemistry": {"individual": 55.0, "group": 33.0},
    "biology": {"individual": 50.0, "group": 30.0},
    "history": {"individual": 45.0, "group": 28.0},
    "geography": {"individual": 45.0, "group": 28.0},
    "computer_science": {"individual": 60.0, "group": 35.0},
    "programming": {"individual": 65.0, "group": 40.0},
    "music": {"individual": 40.0, "group": 25.0},
    "art": {"individual": 40.0, "group": 25.0},
    "sports": {"individual": 35.0, "group": 22.0},
    "other": {"individual": 45.0, "group": 28.0},
}

DEFAULT_INDIVIDUAL_PRICE = 45.0
DEFAULT_GROUP_PRICE = 28.0


def get_subject_price(subject: str, lesson_type: str = "individual") -> float:
    """
    Get the price per hour for a specific subject and lesson type.
    Case-insensitive lookup.
    
    Args:
        subject: Subject name (e.g., "Math", "Arabic")
        lesson_type: "individual" or "group"
    
    Returns:
        Price per hour for the subject and lesson type
    """
    subject_lower = subject.lower().strip()
    lesson_type_lower = lesson_type.lower().strip()
    
    # Get subject pricing
    subject_pricing = SUBJECT_PRICES.get(subject_lower)
    
    if not subject_pricing:
        # Subject not found, use defaults
        return DEFAULT_INDIVIDUAL_PRICE if lesson_type_lower == "individual" else DEFAULT_GROUP_PRICE
    
    # Get price for lesson type
    if lesson_type_lower == "group":
        return subject_pricing.get("group", DEFAULT_GROUP_PRICE)
    else:
        return subject_pricing.get("individual", DEFAULT_INDIVIDUAL_PRICE)


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
    Get all subject prices for admin reference.
    
    Returns:
        Dictionary of all subject prices (with individual and group rates)
    """
    return SUBJECT_PRICES.copy()

