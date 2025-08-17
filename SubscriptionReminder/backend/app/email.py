import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@re-mind.xyz")

# Check if SendGrid is configured
if not SENDGRID_API_KEY:
    logger.error("❌ SENDGRID_API_KEY not found in environment variables!")
    logger.error("Please set SENDGRID_API_KEY in your .env file")

def send_email_via_sendgrid(message):
    """Helper function to send email via SendGrid with proper error handling"""
    if not SENDGRID_API_KEY:
        logger.error("❌ Cannot send email: SENDGRID_API_KEY not configured")
        return False
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"✅ Email sent successfully! Status: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send email via SendGrid: {str(e)}")
        return False

def send_verification_email(to_email, token):
    """Send email verification email"""
    verification_link = f"https://app.re-mind.xyz/verify-email?token={token}"
    subject = "Please verify your email for Re:Mind"
    html_content = f"""
        <p>Hello, 👋 <br>
        Thanks for signing up to Re:Mind. To complete your registration, please click the link below to verify your email: <br>
        <a href="{verification_link}">Verify Email</a></p>

        <p style="font-size: 12px; color: #888;">
        If you didn't create this account, you can safely ignore this message.
        </p>    
    """

    from_email = Email(SENDER_EMAIL, "Re:Mind Team")
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    message.add_content(Content("text/plain", f"Hello,\nThanks for signing up to Re:Mind. Please verify your email by clicking this link: {verification_link}\n\nIf you didn't request this, ignore this email."))

    success = send_email_via_sendgrid(message)
    if success:
        logger.info(f"✅ Verification email sent to {to_email}")
    else:
        logger.error(f"❌ Failed to send verification email to {to_email}")
    return success

def send_reminder_email(to_email, sub_name, deadline):
    """Send subscription reminder email"""
    subject = f"⏰ Reminder: {sub_name} is due soon!"
    html_content = f"""
        <p>Hi there,</p>
        <p>This is a reminder that your subscription <strong>{sub_name}</strong> is due on <strong>{deadline}</strong>.</p>
        <p>Don't forget to cancel or manage it before it's too late.</p>
        <p style="font-size: 12px; color: #888;">You're getting this because you're subscribed to reminders on Re:Mind.</p>
    """
    
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    
    success = send_email_via_sendgrid(message)
    if success:
        logger.info(f"✅ Reminder email sent to {to_email} for subscription {sub_name}")
    else:
        logger.error(f"❌ Failed to send reminder email to {to_email} for subscription {sub_name}")
    return success

def send_password_reset_email(to_email, token):
    """Send password reset email"""
    reset_link = f"https://app.re-mind.xyz/reset-password?token={token}"

    subject = "🔐 Reset your password - Re:Mind"
    html_content = f"""
        <p>Hello,</p>
        <p>It looks like you requested to reset your password. Click the link below:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you didn't request this, you can ignore the message.</p>
    """

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    success = send_email_via_sendgrid(message)
    if success:
        logger.info(f"✅ Password reset email sent to {to_email}")
    else:
        logger.error(f"❌ Failed to send password reset email to {to_email}")
    return success