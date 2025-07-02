from pydantic import BaseModel, EmailStr
from datetime import date


class Subscription(BaseModel):
    subscription_name : str
    deadline : date

class SubscriptionCreate(Subscription):
    pass


class SubscriptionResponse(Subscription):
    id: int
    user_id: int
    subscription_name : str
    deadline: date

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None


class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserInDB(UserOut):
    hashed_password : str