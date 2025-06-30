from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .models import Base
from .database import engine
from sqlalchemy.orm import Session
from .auth import get_current_user
from .auth import router as auth_router
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .models import Subscriptions, User
from .database import SessionLocal
from .email import send_reminder_email
load_dotenv()

app = FastAPI()

origins = [
    "https://app.re-mind.xyz/",
    "http://localhost:5173/"
]


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)


Base.metadata.create_all(bind=engine)

@app.get("/subscriptions/", response_model=list[schemas.SubscriptionResponse])
def get_subscriptions(current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscriptions = session.query(models.Subscriptions).filter(
            models.Subscriptions.user_id == current_user.id
        ).all()
    return subscriptions

@app.post("/subscriptions/", response_model=schemas.SubscriptionCreate)
def create_subscriptions(subscription: schemas.Subscription, current_user: models.User = Depends(get_current_user)):
    db_subscription = models.Subscriptions(
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
        subscription = session.query(models.Subscriptions).get(id)
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
        subscription = session.query(models.Subscriptions).get(id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        if subscription.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this subscription")
        
        subscription.subscription_name = subscription_data.subscription_name
        subscription.deadline = subscription_data.deadline

        session.commit()
        session.refresh(subscription)
        return subscription

@app.post("/reset-db/")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Database reset successfully!"}


def check_upcoming_deadlines():
    with SessionLocal() as db:
        today = datetime.utcnow().date()
        reminder_date = today + timedelta(days=3)
        subs = db.query(Subscriptions).filter(Subscriptions.deadline == reminder_date).all()
        for sub in subs:
            user = db.query(User).filter(User.id == sub.user_id).first()
            if user and user.is_verified:
                send_reminder_email(user.email, sub.subscription_name, sub.deadline)


scheduler = BackgroundScheduler()
scheduler.add_job(check_upcoming_deadlines, 'interval', days=1)
scheduler.start()