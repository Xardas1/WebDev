from app.database import SessionLocal
from app.models import Subscriptions, User
from app.email import send_reminder_email
from datetime import datetime, timedelta, UTC



def send_reminders():
    db = SessionLocal()
    try: 
        reminder_date = (datetime.now(UTC) + timedelta(days=3)).date()
        subscriptions = db.query(Subscriptions).filter(
            Subscriptions.deadline == reminder_date
        ).all()

        for sub in subscriptions:
            user = db.query(User).filter(User.id == sub.user_id).first()
            if user and user.is_verified:
                send_reminder_email(user.email, sub.subscription_name, sub.deadline)

    finally:
        db.close()


if __name__ == "__main__":
    send_reminders()