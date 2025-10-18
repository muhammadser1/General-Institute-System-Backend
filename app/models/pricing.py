"""
Pricing Model for MongoDB

Represents subject pricing in the database.
Admins can manage pricing through API endpoints.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class Pricing:
    """
    Pricing Model - Represents the 'pricing' collection in MongoDB
    Stores pricing per subject for individual and group lessons
    """
    
    def __init__(
        self,
        subject: str,
        individual_price: float,
        group_price: float,
        currency: str = "USD",
        is_active: bool = True,
        _id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = _id or str(uuid.uuid4())
        self.subject = subject.strip()  # e.g., "Mathematics", "Physics"
        self.individual_price = individual_price
        self.group_price = group_price
        self.currency = currency
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Pricing object to dictionary for MongoDB insertion"""
        return {
            "_id": self._id,
            "subject": self.subject,
            "individual_price": self.individual_price,
            "group_price": self.group_price,
            "currency": self.currency,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Pricing":
        """Create Pricing object from MongoDB document"""
        return Pricing(
            _id=data.get("_id"),
            subject=data.get("subject"),
            individual_price=data.get("individual_price"),
            group_price=data.get("group_price"),
            currency=data.get("currency", "USD"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    # ===== Database Methods =====
    
    @staticmethod
    def find_by_subject(subject: str, db_collection) -> Optional["Pricing"]:
        """Find active pricing by subject name (case-insensitive)"""
        pricing_doc = db_collection.find_one({
            "subject": {"$regex": f"^{subject}$", "$options": "i"},
            "is_active": True
        })
        if pricing_doc:
            return Pricing.from_dict(pricing_doc)
        return None
    
    @staticmethod
    def find_by_id(pricing_id: str, db_collection) -> Optional["Pricing"]:
        """Find pricing by ID"""
        pricing_doc = db_collection.find_one({"_id": pricing_id})
        if pricing_doc:
            return Pricing.from_dict(pricing_doc)
        return None
    
    @staticmethod
    def get_all_active(db_collection) -> list["Pricing"]:
        """Get all active pricing"""
        pricing_docs = db_collection.find({"is_active": True}).sort("subject", 1)
        return [Pricing.from_dict(doc) for doc in pricing_docs]
    
    @staticmethod
    def subject_exists(subject: str, db_collection, exclude_id: Optional[str] = None) -> bool:
        """Check if subject already exists (case-insensitive)"""
        query = {
            "subject": {"$regex": f"^{subject}$", "$options": "i"}
        }
        if exclude_id:
            query["_id"] = {"$ne": exclude_id}
        return db_collection.count_documents(query) > 0
    
    def save(self, db_collection):
        """Insert pricing into database"""
        db_collection.insert_one(self.to_dict())
    
    def update_in_db(self, db_collection):
        """Update pricing in database"""
        self.updated_at = datetime.utcnow()
        db_collection.update_one(
            {"_id": self._id},
            {"$set": self.to_dict()}
        )
    
    @staticmethod
    def delete(pricing_id: str, db_collection) -> bool:
        """Delete pricing from database"""
        result = db_collection.delete_one({"_id": pricing_id})
        return result.deleted_count > 0
    
    # ===== Business Logic Methods =====
    
    def get_price(self, lesson_type: str) -> float:
        """Get price for specific lesson type"""
        if lesson_type.lower() == "group":
            return self.group_price
        return self.individual_price
    
    def calculate_earnings(self, hours: float, lesson_type: str) -> float:
        """Calculate earnings for given hours and lesson type"""
        price_per_hour = self.get_price(lesson_type)
        return round(hours * price_per_hour, 2)

