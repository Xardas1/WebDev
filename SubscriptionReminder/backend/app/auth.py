from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Cookie,
    Request,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import os

from .database import get_db, SessionLocal
from . import models
from .models import User
from .schemas import Token, UserCreate, UserOut
from .email import send_verification_email, send_password_reset_email
from fastapi.responses import RedirectResponse

# ──────────────────────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.email == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    print("User found:", user)
    if not user:
        return False
    print("Password check:", verify_password(password, user.hashed_password))
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ──────────────────────────────────────────────────────────────────────────────
# Dependencies
# ──────────────────────────────────────────────────────────────────────────────

async def get_current_user(
    request: Request,
    token: str = Cookie(None),
    db: Session = Depends(get_db),
):
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ──────────────────────────────────────────────────────────────────────────────
# Auth Routes
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain=".re-mind.xyz",
        max_age=60 * 60 * 24,
    )
    return response

@router.post("/logout")
def logout_user():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("token", domain=".re-mind.xyz")
    return response

@router.get("/users/me/", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user

# ──────────────────────────────────────────────────────────────────────────────
# Registration + Email Verification
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserOut)
async def register_endpoint(registred_user: UserCreate, db: Session = Depends(get_db)):
    # Username + Email uniqueness
    print("Register payload:", registred_user)
    if db.query(User).filter(User.username == registred_user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == registred_user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create user
    hashed_pw = get_password_hash(registred_user.password)
    db_user = User(
        username=registred_user.username,
        email=registred_user.email,
        hashed_password=hashed_pw,
        is_active=True,
        is_verified=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Optional: email verification
    verification_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=30),
    )
    send_verification_email(db_user.email, verification_token)

    return db_user

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_verified = True
        db.commit()
    

        response = RedirectResponse(url="https://app.re-mind.xyz/product")
        access_token = create_access_token(data={"sub": user.email})
        response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain=".re-mind.xyz",
        max_age=60 * 60 * 24,
        )
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification link expired")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid verification link")

# ──────────────────────────────────────────────────────────────────────────────
# Forgot + Reset Password
# ──────────────────────────────────────────────────────────────────────────────

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(request: EmailRequest):
    mail = request.email
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == mail).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token_data = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        send_password_reset_email(user.email, token)
        return {"message": "Reset email sent"}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed = get_password_hash(data.new_password)
        user.hashed_password = hashed
        db.commit()

    return {"message": "Password reset successful"}
