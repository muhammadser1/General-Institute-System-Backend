from fastapi import APIRouter
<<<<<<< Updated upstream
from app.api.v1.endpoints import user, admin, lessons, payments, pricing
=======
from app.api.v1.endpoints import user, admin, lessons, payments, pricing, students
from app.core.config import config
>>>>>>> Stashed changes

api_router = APIRouter()

# User routes (auth + profile)
api_router.include_router(user.router, prefix="/user", tags=["User"])

# Admin routes
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

# Student routes (teachers and admins can view)
api_router.include_router(students.router, prefix="/students", tags=["Students"])

# Lesson routes
api_router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])

# Payment routes
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])

# Pricing routes (admin management + public lookup)
api_router.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])

<<<<<<< Updated upstream
=======
# Admin routes - Dashboard/Statistics
from app.api.v1.endpoints import dashboard
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Admin routes - Weekly Reports
from app.api.v1.endpoints import weekly_report
api_router.include_router(weekly_report.router, prefix="/weekly-report", tags=["Weekly Reports"])

# Admin routes - Pricing Population
from app.api.v1.endpoints import populate_pricing
api_router.include_router(populate_pricing.router, prefix="/populate-pricing", tags=["Pricing Population"])

# Test routes (only in development)
if config.DEBUG or config.ENVIRONMENT == "development":
    from app.api.v1.endpoints import email_test, test_crash
    api_router.include_router(email_test.router, prefix="/email-test", tags=["Email Testing"])
    api_router.include_router(test_crash.router, prefix="/test-crash", tags=["Testing"])

>>>>>>> Stashed changes
