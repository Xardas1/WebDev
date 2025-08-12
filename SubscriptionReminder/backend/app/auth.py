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
    return pwd_context.verify(plain, hashed)  # Ta funkcja sprawdza, czy hasło, które wpisujemy w przeglądarce jest takie samo, jak zachaszowane w databasie.

def get_password_hash(password):
    return pwd_context.hash(password) # Ta funkcja hashuję hasło

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()         # Ta funkcja patrzy w databasie i szuka pierwszej tabelki, gdzie podany string jest taki sam jak adres email, po czym zwraca usera z tej tabelki

def authenticate_user(db: Session, email : str, password: str):                   # Ta funkcja sprawdza usera                  
    user = get_user(db, email)                                                   # Na początku szuka pierwszej tabelki w databasie, gdzie podany email jest taki sam jak email w databasie, następnie przypisuję usera z tego database do zmiennej ,,user" 
    print("User found:", user)
    if not user:
        return False                                                                    # Jeżeli user nie istnieję i adres nie istnieję zwraca false 
    print("Password check:", verify_password(password, user.hashed_password))
    if not verify_password(password, user.hashed_password):                                         
        return False                                                                    # Jeżeli hasło nie jest takie same jak zhaszowane wcześniej, zwraca false
    return user                                                                         # Jeżeli wszystko się zgadza user istnieje i hasło z wcześniej jest takie samo zwraca usera. 

def create_access_token(data: dict, expires_delta: timedelta | None = None):            # Ta funkcja tworzy token JWT
    to_encode = data.copy()                                                             # Ta linijka tworzy kopię danych, które chcemy zakodować, nie używamy orginału ponieważ wtedy w dalszych krokach zmienialibyśmy orginalne dane
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))      # Ta linijka mówi, kiedy token powinien wygasnąć.
    to_encode.update({"exp": expire})                                                   # Dodaję do tokenu część ,,exp", mówi to dekoderowi, kiedy token powinien wygasnąć
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)                       # Zwraca zakodowany token jwt, zakodowany przy pomocy secret key oraz algorytmu HS256

# ──────────────────────────────────────────────────────────────────────────────
# Dependencies
# ──────────────────────────────────────────────────────────────────────────────

async def get_current_user(      # ta funkcja pozwala na to by, jakby każdemu userowi przypisywały się rzeczy jakich on potrzebuję.
    token: str = Cookie(None),   # jako pierwszy argument dajemy zakodowany token JWT w postaci ciasteczka, jeżeli on nie istnieję jest przypisywany None
    db: Session = Depends(get_db), # drugi argument mówi o tym, że db będzie posiadało zwróconą wartość funkcji get_db.
):
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")                        # jeżeli token nie istnieje i server http ci go nie wysłał zwracamy error'a

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])         # dekoduję payload czyli token JWT zakodowany w ciasteczku z HTTP jest tutaj dekodowany
        username = payload.get("sub")                                           # payload to jest dictionary, przy pomocy payload.get("sub") wyjmujemy z niego część "sub", czyli w sumie dostajemy adres email.
        if username is None:                                                    # jeżeli to nie istnieję i dostajemy None to wtedy zwraca się nam error
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(db, username)                                               # Przy pomocy adresu email robimy ,,query" w databasie co sprawia, że dostajemy wszystkie dane 'user'
    if user is None:                                                            
        raise HTTPException(status_code=401, detail="User not found")    
    return user

async def get_current_active_user(                                              # ta funkcja sprawdza, czy zalogowany użytkownik jest aktywny, jeżeli nie jest blokuję go
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
