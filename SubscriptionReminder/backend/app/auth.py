from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from .schemas import Token, TokenData, UserOut, UserCreate
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from .models import User
from .email import send_verification_email
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .email import send_password_reset_email
from .database import SessionLocal
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Cookie

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQ0OTIwNjU0fQ.DKwJMlp2f-IaTgFIIMwUsGe2772KYSHHLsrFeV11o0E"



fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$Q0Woe0K0OTTxpdXwdS38EelHZr7SvnlsX9QVLd7rPS.S18R0h/W0C",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

"""
Funkcja verify_password, sprawda czy hasło jakie podał użytkownik jest takie same jak zhaszowane hasło w databasie.

pwd_context tworzy hashing context przy użyciu passlib, bezpiecznej biblioteki do hashowania. Tutaj mówi kontekstowi, by użyć algorytmu bcrypt, do contextu.

"deprecated='auto'" ta część mówi Passlib'owi by automatycznie detektował i upgreadował, przestarzał formy hash.

verify() działa w następujący sposób : 

1. Bierze plain_password czyli np. "mypassword123"

2. Hashuję je wewnętrznie używając tych samych ustawień, które były do stworzenia ,,hashed_password"

3. Porównuję stworzony hash z ,,hash_password", które jest w data'basie.

4. Zwraca True, jeżeli hasła są takie same, w przeciwnym wypadku zwraca false.


"""




def get_password_hash(password):
    return pwd_context.hash(password)


"""
Funkcja get_password_hash, bierze plain password np. "secret123" i zwraca bezpieczną zhaszowaną wersję używając bcrypt.

Co się dzieję ,,under the hood".

1.Bcrypt automatycznie generuję ,,random salt" (e.g., "$2b$12$ZV1IV...Qwekl").

2.Salt to losowy string, dodany do hasła przed hashowaniem by zapewnić unikatowość

3.Dzięki temu nawet identyczne hasła generują różnę hashe.

Następnie używamy Bcrypt Hashing Algorithm, by zhashować hasło po zhashowaniu wygląda ono np. tak : 

$2b$12$ZV1IVMbSTQOScov9tNPKeOeAEXhBc90z4S82STxk1sBpYIN3wPbDu


"""


def get_user(db : Session, username: str):
    return db.query(models.User).filter(models.User.email == username).first()

def authenticate_user(db: Session, username: str, password: str):
    print(f"Authenticating: {username} with password: {password}")
    user = get_user(db, username)
    if not user:
        print("User not found")
        return False
    if not verify_password(password, user.hashed_password):
        print("Password does not match")
        return False
    print("User authenticated!")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(
    token: str = Cookie(None),            # ✅ token from cookie instead of OAuth header
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    response = JSONResponse(content={"message": "Login Successful"})
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain=".re-mind.xyz",
        max_age=60 * 60 * 24
    )
    return response


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return current_user

@router.get("/users/me/itmes/")
async def read_own_items(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

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
        return {"message" : "✅ Email verified successfully!"}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification link expired")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid verification link")



@router.post("/register", response_model=UserOut)
async def register_endpoint(registred_user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Received registration data: {registred_user}")
        
        # Check for existing username
        existing_user = db.query(User).filter(User.username == registred_user.username).first()
        if existing_user:
            print("Username already exists")
            raise HTTPException(status_code=400, detail="Username already exists")

        # Check for existing email
        existing_email = db.query(User).filter(User.email == registred_user.email).first()
        if existing_email:
            print("Email already exists")
            raise HTTPException(status_code=400, detail="Email already exists")

        # Hash the password
        hashed_pw = get_password_hash(registred_user.password)
        print(f"Hashed password: {hashed_pw}")

        # Create the user
        db_user = User(
            username=registred_user.username,
            email=registred_user.email,
            hashed_password=hashed_pw,
            is_active=True,
            is_verified=False
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Send verification email here
        verification_token = create_access_token(
            data={"sub": db_user.email},
            expires_delta=timedelta(minutes=30)
        )
        send_verification_email(db_user.email, verification_token)

        print(f"User registered successfully: {db_user.username}")
        return db_user

    except Exception as e:
        print("Error during registration:", str(e))
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30


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
            "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
        } 
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        send_password_reset_email(user.email, token)
        return {"message": "Reset email sent"}


class ResetPasswordRequest(BaseModel):
    token: str
    new_password : str


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed = pwd_context.hash(data.new_password)
        user.hashed_password = hashed
        db.commit()

    return {"message": "Password reset successful"}