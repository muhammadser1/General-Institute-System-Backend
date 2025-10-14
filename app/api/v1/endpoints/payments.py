from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId
from app.schemas.payment import PaymentCreate, PaymentResponse, MonthlyPaymentsResponse
from app.api.deps import get_current_admin
from app.db import mongo_db

router = APIRouter()


# @router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
# def create_payment(
#     payment_data: PaymentCreate,
#     current_admin: Dict = Depends(get_current_admin)
# ):
#     """
#     Admin adds a new student payment
#     """
#     new_payment = {
#         "student_name": payment_data.student_name,
#         "student_email": payment_data.student_email,
#         "amount": payment_data.amount,
#         "payment_date": payment_data.payment_date,
#         "lesson_id": payment_data.lesson_id,
#         "notes": payment_data.notes,
#         "created_at": datetime.utcnow(),
#         "created_by": str(current_admin["_id"])
#     }
    
#     result = mongo_db.payments_collection.insert_one(new_payment)
#     new_payment["_id"] = result.inserted_id
    
#     return PaymentResponse(
#         id=str(new_payment["_id"]),
#         student_name=new_payment["student_name"],
#         student_email=new_payment.get("student_email"),
#         amount=new_payment["amount"],
#         payment_date=new_payment["payment_date"],
#         lesson_id=new_payment.get("lesson_id"),
#         notes=new_payment.get("notes"),
#         created_at=new_payment["created_at"],
#     )


# @router.get("/", response_model=MonthlyPaymentsResponse)
# def get_monthly_payments(
#     current_admin: Dict = Depends(get_current_admin),
#     month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
#     year: int = Query(..., ge=2000, le=2100, description="Year"),
#     student_name: Optional[str] = Query(None, description="Filter by student name"),
# ):
#     """
#     Admin gets all student payments for a specific month
#     - Required: month and year
#     - Optional: filter by student name
#     - Returns: payments + total amount
#     """
#     # Build date range query
#     start_date = datetime(year, month, 1)
#     if month == 12:
#         end_date = datetime(year + 1, 1, 1)
#     else:
#         end_date = datetime(year, month + 1, 1)
    
#     query = {
#         "payment_date": {
#             "$gte": start_date,
#             "$lt": end_date
#         }
#     }
    
#     # Filter by student name if provided
#     if student_name:
#         query["student_name"] = {"$regex": student_name, "$options": "i"}
    
#     # Get payments
#     payments = list(mongo_db.payments_collection.find(query).sort("payment_date", -1))
    
#     # Calculate total amount
#     total_amount = round(sum(payment.get("amount", 0) for payment in payments), 2)
    
#     # Convert to response
#     payment_responses = [
#         PaymentResponse(
#             id=str(payment["_id"]),
#             student_name=payment["student_name"],
#             student_email=payment.get("student_email"),
#             amount=payment["amount"],
#             payment_date=payment["payment_date"],
#             lesson_id=payment.get("lesson_id"),
#             notes=payment.get("notes"),
#             created_at=payment["created_at"],
#         )
#         for payment in payments
#     ]
    
#     return MonthlyPaymentsResponse(
#         month=month,
#         year=year,
#         total_payments=len(payments),
#         total_amount=total_amount,
#         payments=payment_responses
#     )

