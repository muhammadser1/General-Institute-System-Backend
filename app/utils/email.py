"""
Email utility functions
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import traceback
from typing import Optional

from app.core.config import config


def send_email(
    subject: str,
    body: str,
    to_email: str
) -> bool:
    """
    Send email
    
    Args:
        subject: Email subject
        body: Email body text
        to_email: Recipient email
        
    Returns:
        True if sent successfully, False otherwise
    """
    if not config.EMAIL_USER or not config.EMAIL_PASSWORD:
        print("⚠️  Email not configured. Skipping email send.")
        return False
    
    sender_email = config.EMAIL_USER
    password = config.EMAIL_PASSWORD
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def send_crash_notification(
    error: Exception,
    endpoint: str = "Unknown",
    method: str = "Unknown",
    user_id: Optional[str] = None
) -> bool:
    """
    Send email notification when application crashes
    
    Args:
        error: The exception that occurred
        endpoint: API endpoint where error occurred
        method: HTTP method
        user_id: User ID if authenticated
        
    Returns:
        True if email sent successfully
    """
    if not config.EMAIL_TO:
        print("⚠️  EMAIL_TO not configured. Skipping crash notification.")
        return False
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_traceback = traceback.format_exc()
    
    subject = f"🚨 Application Crash Alert - {config.APP_NAME}"
    
    body = f"""
Application Crash Notification

Time: {timestamp}
Application: {config.APP_NAME}
Environment: {config.ENVIRONMENT}

Error Details:
==============
Error Type: {type(error).__name__}
Error Message: {str(error)}

Request Details:
===============
Endpoint: {method} {endpoint}
User ID: {user_id if user_id else "Not authenticated"}

Full Traceback:
===============
{error_traceback}

---
This is an automated error notification from {config.APP_NAME}
"""
    
    return send_email(subject, body, config.EMAIL_TO)

