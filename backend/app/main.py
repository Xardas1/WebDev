from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .models import Base
from .database import engine
from sqlalchemy.orm import Session
from app import auth
from app.auth import get_current_user

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
Base.metadata.create_all(bind=engine)

@app.get("/subscriptions/", response_model=list[schemas.SubscriptionResponse])
def get_subscriptions(current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscriptions = session.query(models.Subscriptions).filter(
            models.Subscriptions.user_id == current_user.id
        ).all()
    return subscriptions


@app.post("/subscriptions/", response_model=schemas.SubscriptionCreate)
def create_subscriptions(subscription : schemas.Subscription, current_user: models.User = Depends(get_current_user)):
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
def delete_subscriptions(id : int, current_user: models.User = Depends(get_current_user)):
    with Session(engine) as session:
        subscription = session.query(models.Subscriptions).get(id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        if subscription.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="not authorized to delete this subscription")
        session.delete(subscription)
        session.commit()
        return subscription

@app.put("/subscriptions/{id}", response_model=schemas.SubscriptionResponse)
def update_subscription(subscription_data : schemas.SubscriptionCreate, id : int, current_user: models.User = Depends(get_current_user)):
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
    return {"message" : "Database reset successfully!"}


"""

so like if i'm building subscription reminder app and like i'm building MVP and in my backend i have
 functions for 

add / remove subscrioption


"""