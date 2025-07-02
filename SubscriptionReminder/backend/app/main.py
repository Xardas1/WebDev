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

# ✅ Regex to catch subdomains like app.re-mind.xyz
origin_regex = r"^https:\/\/(?:.*\.)?re\-mind\.xyz$"

# ✅ CORS middleware (MUST come before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "*"],
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

# ✅ Background job to check upcoming deadlines
def check_upcoming_deadlines():
    with SessionLocal() as db:
        today = datetime.utcnow().date()
        reminder_date = today + timedelta(days=3)
        subs = db.query(Subscriptions).filter(Subscriptions.deadline == reminder_date).all()
        for sub in subs:
            user = db.query(User).filter(User.id == sub.user_id).first()
            if user and user.is_verified:
                send_reminder_email(user.email, sub.subscription_name, sub.deadline)

# ✅ Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_upcoming_deadlines, 'interval', days=1)
scheduler.start()
