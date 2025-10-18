from fastapi import APIRouter
from app.api.v1.endpoints import user, admin, lessons, payments, pricing

api_router = APIRouter()

# User routes (auth + profile)
api_router.include_router(user.router, prefix="/user", tags=["User"])

# Admin routes
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

# Lesson routes
api_router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])

# Payment routes
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])

# Pricing routes (admin management + public lookup)
api_router.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])

