from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from .schemas import Token, TokenData, UserOut, UserCreate
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from .models import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
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
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : Session = Depends(get_db)):
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
        token_data = TokenData(sub=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=token_data.sub)
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return current_user

@router.get("/users/me/itmes/")
async def read_own_items(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/register", response_model=UserOut)
async def register_endpoint(registred_user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if db.query(User).filter(User.username == registred_user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if db.query(User).filter(User.email == registred_user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")


    hashed_pw = get_password_hash(registred_user.password)

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

    return db_user

