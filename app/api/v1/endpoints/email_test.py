"""
Email testing endpoint
"""
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class EmailTestRequest(BaseModel):
    to_email: EmailStr | None = None  # Optional, will use EMAIL_TO from env if not provided
    subject: str = "Test Email"
    body: str = "This is a test email from General Institute System"


@router.post("/send-test")
async def send_test_email(request: EmailTestRequest):
    """
    Test endpoint to send an email manually
    """
    from app.core.config import config
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Check if email is configured
    if not config.EMAIL_USER or not config.EMAIL_PASSWORD:
        return {
            "success": False,
            "message": "Email not configured. Please set EMAIL_USER and EMAIL_PASSWORD in .env"
        }
    
    # Use EMAIL_TO from env if no recipient provided
    recipient_email = request.to_email or config.EMAIL_TO
    if not recipient_email:
        return {
            "success": False,
            "message": "No recipient email provided. Set EMAIL_TO in .env or provide to_email in request"
        }
    
    sender_email = config.EMAIL_USER
    password = config.EMAIL_PASSWORD
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = request.subject
    msg.attach(MIMEText(request.body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        return {
            "success": True,
            "message": f"Email sent successfully to {recipient_email}",
            "from": sender_email,
            "to": recipient_email,
            "subject": request.subject
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending email: {str(e)}",
            "error": str(e)
        }

