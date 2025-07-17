import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "noreply@re-mind.xyz"
load_dotenv()

def send_verification_email(to_email, token):
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

    from_email = Email("noreply@re-mind.xyz", "Re:Mind Team")
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    message.add_content(Content("text/plain", f"Hello,\nThanks for signing up to Re:Mind. Please verify your email by clicking this link: {verification_link}\n\nIf you didn't request this, ignore this email."))

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("✅ Verification email sent.")
    except Exception as e:
        print("❌ Failed to send email:", str(e))




def send_reminder_email(to_email, sub_name, deadline):
    subject = f"⏰Reminder: {sub_name} is due soon!"
    html_content = f"""
        <p>Hi there,</p>
        <p>This is a remidner that your subscription <strong>{sub_name}</strong> is due on <strong>{deadline}</strong>.</p>
        <p>Don't forget to cancel or manage it before it's too late.</p>
        <p style="font-size: 12px; color: #888;">You're getting this  because you're subscribed to reminders on Re:Mind.</p>
    """
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("✅ Reminder email sent.")
    except Exception as e:
        print("❌ Failed to send reminder email:", str(e))



def send_password_reset_email(to_email, token):
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

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("✅ Password reset email sent.")
    except Exception as e:
        print("❌ Failed to send reset email:", str(e))