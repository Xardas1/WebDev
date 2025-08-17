from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .models import Base, Subscriptions, User
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from .auth import router as auth_router
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .email import send_reminder_email

load_dotenv()

app = FastAPI()

# ✅ Allow cross-origin cookies from frontend
origins = [
    "https://app.re-mind.xyz",
    "https://www.re-mind.xyz",
    "https://re-mind.xyz",                # optional, fallback base domain
    "http://localhost:3000",             # local dev
    "http://127.0.0.1:3000"
]



# ✅ CORS middleware (MUST come before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Optional: log frontend origin to debug CORS
@app.middleware("http")
async def debug_origin(request: Request, call_next):
    print(">>> ORIGIN HEADER:", request.headers.get("origin"))
    response = await call_next(request)
    return response

# ✅ Include auth routes (register, token, users/me)
app.include_router(auth_router)

# ✅ Create tables if needed
Base.metadata.create_all(bind=engine)

# ✅ Subscription endpoints
@app.get("/subscriptions/", response_model=list[schemas.SubscriptionResponse])
def get_subscriptions(current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscriptions = session.query(Subscriptions).filter(
            Subscriptions.user_id == current_user.id
        ).all()
    return subscriptions

@app.post("/subscriptions/", response_model=schemas.SubscriptionCreate)
def create_subscriptions(subscription: schemas.Subscription, current_user: models.User = Depends(get_current_user)):
    db_subscription = Subscriptions(
        subscription_name=subscription.subscription_name,
        deadline=subscription.deadline,
        user_id=current_user.id
    )
    with Session(engine) as session:
        session.add(db_subscription)
        session.commit()
        session.refresh(db_subscription)
        return db_subscription

@app.delete("/subscriptions/{id}", response_model=schemas.SubscriptionResponse)
def delete_subscriptions(id: int, current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscription = session.query(Subscriptions).get(id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        if subscription.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this subscription")
        session.delete(subscription)
        session.commit()
        return subscription

@app.put("/subscriptions/{id}", response_model=schemas.SubscriptionResponse)
def update_subscription(subscription_data: schemas.SubscriptionCreate, id: int, current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscription = session.query(Subscriptions).get(id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        if subscription.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this subscription")
        
        subscription.subscription_name = subscription_data.subscription_name
        subscription.deadline = subscription_data.deadline
        session.commit()
        session.refresh(subscription)
        return subscription

# ✅ Optional reset (dangerous in prod)
@app.post("/reset-db/")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Database reset successfully!"}

# ✅ Test email functionality
@app.post("/test-email/")
def test_email():
    """Test endpoint to check if email system is working"""
    try:
        from .email import send_reminder_email
        
        # Check if SendGrid is configured
        import os
        sendgrid_key = os.getenv("SENDGRID_API_KEY")
        
        if not sendgrid_key:
            return {
                "status": "error",
                "message": "SendGrid API key not configured",
                "details": "Please set SENDGRID_API_KEY in your environment variables"
            }
        
        # Try to send a test email
        success = send_reminder_email(
            to_email="test@example.com",  # This won't actually send, just tests the configuration
            sub_name="Test Subscription",
            deadline="2025-01-01"
        )
        
        if success:
            return {
                "status": "success",
                "message": "Email system is working properly",
                "details": "SendGrid configuration is correct"
            }
        else:
            return {
                "status": "error",
                "message": "Email system failed",
                "details": "Check SendGrid configuration and logs"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": "Email system error",
            "details": str(e)
        }

# ✅ Background job to check upcoming deadlines
def check_upcoming_deadlines():
    """Check for subscriptions due in 3 days and send reminder emails"""
    try:
        print("🔄 Checking for upcoming subscription deadlines...")
        
        with SessionLocal() as db:
            today = datetime.utcnow().date()
            reminder_date = today + timedelta(days=3)
            
            print(f"📅 Looking for subscriptions due on: {reminder_date}")
            
            # Find subscriptions due in 3 days
            subs = db.query(Subscriptions).filter(Subscriptions.deadline == reminder_date).all()
            print(f"📧 Found {len(subs)} subscriptions due in 3 days")
            
            for sub in subs:
                try:
                    # Get user info
                    user = db.query(User).filter(User.id == sub.user_id).first()
                    if user and user.is_verified:
                        print(f"📤 Sending reminder to {user.email} for subscription: {sub.subscription_name}")
                        success = send_reminder_email(user.email, sub.subscription_name, sub.deadline)
                        if success:
                            print(f"✅ Reminder sent successfully to {user.email}")
                        else:
                            print(f"❌ Failed to send reminder to {user.email}")
                    else:
                        print(f"⚠️ User {sub.user_id} not found or not verified for subscription: {sub.subscription_name}")
                except Exception as e:
                    print(f"❌ Error processing subscription {sub.id}: {str(e)}")
                    continue
                    
        print("✅ Finished checking upcoming deadlines")
        
    except Exception as e:
        print(f"❌ Error in check_upcoming_deadlines: {str(e)}")

# ✅ Start scheduler with error handling
try:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_upcoming_deadlines, 
        'interval', 
        days=1,
        id='subscription_reminders',
        name='Check subscription deadlines daily'
    )
    scheduler.start()
    print("✅ Scheduler started successfully for subscription reminders")
except Exception as e:
    print(f"❌ Failed to start scheduler: {str(e)}")
