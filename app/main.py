from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import config
from app.db import connect_to_mongo, close_mongo_connection
from app.api.v1.api import api_router
from app.utils.email import send_crash_notification
from app.utils.weekly_report import send_weekly_report_job

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events - startup and shutdown
    """
    # Startup
    logger.info("🚀 Starting General Institute System API...")
    try:
        connect_to_mongo()
        logger.info("✅ Application startup complete")
        
        # Start scheduler for weekly reports
        scheduler = BackgroundScheduler()
        
        # Schedule weekly report every Saturday at 9:00 AM
        scheduler.add_job(
            send_weekly_report_job,
            trigger=CronTrigger(day_of_week='sat', hour=9, minute=0),
            id='weekly_lesson_report',
            name='Weekly Lesson Report',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("📅 Weekly lesson report scheduler started (Every Saturday at 9:00 AM)")
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down General Institute System API...")
    close_mongo_connection()
    
    # Shutdown scheduler
    try:
        scheduler.shutdown()
        logger.info("📅 Scheduler stopped")
    except:
        pass
    
    logger.info("✅ Application shutdown complete")


app = FastAPI(
    title="General Institute System",
    description="A comprehensive backend system for managing institute operations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler - catches all unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that catches all unhandled errors
    and sends email notification
    """
    # Get user info if available
    user_id = None
    if hasattr(request.state, "user"):
        user_id = getattr(request.state.user, "id", None)
    
    # Log the error
    logger.error(f"❌ Unhandled error: {str(exc)}")
    logger.error(f"   Endpoint: {request.method} {request.url.path}")
    logger.error(f"   Traceback: {traceback.format_exc()}")
    
    # Send email notification if configured
    try:
        send_crash_notification(
            error=exc,
            endpoint=request.url.path,
            method=request.method,
            user_id=user_id
        )
    except Exception as email_error:
        logger.error(f"Failed to send crash notification: {str(email_error)}")
    
    # Return error response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. The issue has been logged and reported."
        }
    )


# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint - Hello World
    """
    return {
        "message": "Hello World",
        "app": "General Institute System",
        "version": "1.0.0"
    }

