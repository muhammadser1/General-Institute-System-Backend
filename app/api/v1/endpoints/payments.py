from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId
from app.schemas.payment import PaymentCreate, PaymentResponse, MonthlyPaymentsResponse
from app.models.payment import Payment
from app.api.deps import get_current_admin
from app.db import mongo_db

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_data: PaymentCreate,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin adds a new student payment
    """
    # Create payment using Payment model
    new_payment = Payment(
        student_name=payment_data.student_name,
        student_email=payment_data.student_email,
        amount=payment_data.amount,
        payment_date=payment_data.payment_date,
        lesson_id=payment_data.lesson_id,
        notes=payment_data.notes,
        created_by=str(current_admin["_id"])
    )
    
    # Save to database using model method
    new_payment.save(mongo_db.payments_collection)
    
    # Return payment response
    return PaymentResponse(
        id=new_payment._id,
        student_name=new_payment.student_name,
        student_email=new_payment.student_email,
        amount=new_payment.amount,
        payment_date=new_payment.payment_date,
        lesson_id=new_payment.lesson_id,
        notes=new_payment.notes,
        created_at=new_payment.created_at,
    )


@router.get("/", response_model=MonthlyPaymentsResponse)
def get_monthly_payments(
    current_admin: Dict = Depends(get_current_admin),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, le=2100, description="Year"),
    student_name: Optional[str] = Query(None, description="Filter by student name"),
):
    """
    Admin gets all student payments for a specific month
    - Required: month and year
    - Optional: filter by student name
    - Returns: payments + total amount
    """
    # Get payments by month using model method
    payments = Payment.find_by_month(month, year, mongo_db.payments_collection)
    
    # Filter by student name if provided
    if student_name:
        payments = [p for p in payments if student_name.lower() in p.student_name.lower()]
    
    # Calculate total amount using model method
    total_amount = Payment.calculate_total(payments)
    
    # Convert to response
    payment_responses = [
        PaymentResponse(
            id=payment._id,
            student_name=payment.student_name,
            student_email=payment.student_email,
            amount=payment.amount,
            payment_date=payment.payment_date,
            lesson_id=payment.lesson_id,
            notes=payment.notes,
            created_at=payment.created_at,
        )
        for payment in payments
    ]
    
    return MonthlyPaymentsResponse(
        month=month,
        year=year,
        total_payments=len(payments),
        total_amount=total_amount,
        payments=payment_responses
    )


@router.get("/student/{student_name}")
def get_student_payments(
    student_name: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin gets all payments for a specific student
    - Shows all payments made by the student
    - Shows total amount paid
    """
    # Get all payments for the student
    payments = Payment.find_by_student_name(student_name, mongo_db.payments_collection)
    
    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No payments found for student '{student_name}'"
        )
    
    # Calculate total amount
    total_amount = Payment.calculate_total(payments)
    
    # Convert to response
    payment_responses = [
        PaymentResponse(
            id=payment._id,
            student_name=payment.student_name,
            student_email=payment.student_email,
            amount=payment.amount,
            payment_date=payment.payment_date,
            lesson_id=payment.lesson_id,
            notes=payment.notes,
            created_at=payment.created_at,
        )
        for payment in payments
    ]
    
    return {
        "student_name": student_name,
        "total_payments": len(payments),
        "total_amount": total_amount,
        "payments": payment_responses
    }


@router.get("/student/{student_name}/total")
def get_student_total(
    student_name: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin gets total amount paid by a specific student
    - Quick summary endpoint
    """
    # Get all payments for the student
    payments = Payment.find_by_student_name(student_name, mongo_db.payments_collection)
    
    # Calculate total amount
    total_amount = Payment.calculate_total(payments)
    
    return {
        "student_name": student_name,
        "total_payments": len(payments),
        "total_amount": total_amount,
        "currency": "USD"
    }


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: str,
    current_admin: Dict = Depends(get_current_admin)
):
    """
    Admin deletes a payment record
    """
    payment = Payment.find_by_id(payment_id, mongo_db.payments_collection)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    payment.delete(mongo_db.payments_collection)
    return None
