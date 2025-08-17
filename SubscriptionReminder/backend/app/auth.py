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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],                 # FastApi automatycznie analizuje pola formularza logowania i ,,login fields" 
    db: Session = Depends(get_db),                                              # Ta część używa ,,dependency function" ,,get_db" by zdobyć database session.
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)        # Wywołujemy funkcję ,,authenticate_user", która szuka użytkownika poprzez email, weryfikuję hasło, zwraca użytkownika jeżeli jest ,,valid" lub False jeżel nie jest 
    if not user:                                                                # Jeżeli user został nie znaleziony FastApi zwróci tą część jako JSON error response. 
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(                                        # jeżeli logowanie powiodło się pomyślnie, tworzymy token JWT, w środku tego tokenu dodajemy ,,sub: user.email", później ten token będzie używany by zidentyfikować user'a.
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = JSONResponse(content={"message": "Login successful"})           # tutaj buduję się ,,response object", który wysyłamy z powrotem do frontendu
    response.set_cookie(                                                       # ustawiamy token JWT jako ciasteczko
        key="token",
        value=access_token,
        httponly=True,                                                         # java script w frontendzie nie ma do tego dostępu (for security)
        secure=True,                                                           # wysyłaj tylko po HTTPS
        samesite="none",                                                        # Protect against CSRF
        # domain=".re-mind.xyz",                                               # ❌ Remove this - let browser handle domain automatically
        max_age=60 * 60 * 24,                                                  # Ciasteczko trwa jeden dzień
    )
    return response

@router.post("/logout")                                                        # to towrzy POST API endpoint na /logout                                         
def logout_user():                                                             # standardowa funkcja nie asynchroniczna, nie potrzeba żadnych parametrów ponieważ nie ma znaczenia kto się wylogowywyję chcemy tylko zclearować token.
    response = JSONResponse(content={"message": "Logged out"})                 # tworzymy odpowiedź, która wyśle to z powrotem do front'endu.
    response.delete_cookie("token")                                             # usuwa ciasteczko o nazwie ,,token" co sprawia, że user zostaję wylogowany.
    return response                                                            # zwraca odpowiedź z powrotem do klienta, ciasteczko przestało istnieć i user 

@router.get("/users/me/", response_model=UserOut)                              # to tworzy ,,get route" na /users/me, w momencie gdy frontend wysyła GET request to /users/me ta funkcja się uruchamia
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]     # to mówi ,,przed uruchomieniem tej funkcji, uruchom funkcję ,,get_current_active_user()", następnie weź ,,returned user" i przydziel go do ,,current user" 
):
    return current_user

# ──────────────────────────────────────────────────────────────────────────────
# Registration + Email Verification
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserOut)
async def register_endpoint(
    registred_user: UserCreate,             # jako argument bierze typ ,,UserCreate" 
    db: Session = Depends(get_db)           # live connection to database 
):
    # Username + Email uniqueness
    print("Register payload:", registred_user)
    if db.query(User).filter(User.username == registred_user.username).first():                   # sprawdzamy czy username już istnieję, jeżeli tak : 
        raise HTTPException(status_code=400, detail="Username already exists")                    # zwracamy error
    if db.query(User).filter(User.email == registred_user.email).first():                         # sprawdzamy czy email istnieję, jeżeli tak : 
        raise HTTPException(status_code=400, detail="Email already exists")                       # podnosimy error 

    # Create user
    hashed_pw = get_password_hash(registred_user.password)                                        # instant hashujemy hasło.
    db_user = User(                                                                               # tutaj tworzymy nowy ,,user" object
        username=registred_user.username,                                                         # Podany username przypisujemy
        email=registred_user.email,                                                               # Podany email przypisujemy
        hashed_password=hashed_pw,                                                                # podane zhaszowane hasło przypisujemy
        is_active=True,                                                                           # is_active --> user ma prawo korzystać ze strony
        is_verified=False,                                                                        # nie jest zweryfikowany jeszcze
    )

    db.add(db_user)                                                                               # dodajemy usera do ,,current db session"
    db.commit()                                                                                   # faktycznie zapisujemy to w bazie danych
    db.refresh(db_user)                                                                           # reloadujemy usera, z auto-wygenerowanym id value

    # Optional: email verification
    verification_token = create_access_token(                                                     # ta część tworzy ,,short-lived token JWT", który przechowuję email użytkownika ,,sub" 
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=30),
    )
    send_verification_email(db_user.email, verification_token)                                    # ta funkcja wysyła ,,verification_token", który zostal stworzony powyżej.

    return db_user

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):                                      # jako parametr bierze token z ,,query parameter" , nastomiast db : Session znaczy, że podłączamy ,,live connection to database" 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                           # ta linijka deokduję token JWT używając ,,SECRET_KEY", sprawdza czy jest prawidłowy i nie został zmodyfikowany.
        email = payload.get("sub")                                                                # payload to jest dictionary, robiąc ,,paygload.get("sub"), wyjmujemy z niego część ,,sub"
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()                                 # szuka usera w databasie, przy pomocy emailu z tokena.
        if not user:
            raise HTTPException(status_code=404, detail="User not found")                         # jeżeli user nie istnieję ,,raiseujemy" eror 404 

        user.is_verified = True                                                                   # markujemy usera, że jest zweryfikowany jako ,,True" 
        db.commit()                                                                               # zapisujemy zmiany w bazie danych
    

        response = RedirectResponse(url="https://app.re-mind.xyz/product")                        # Po pomyślnej weryfikacji przekierowujemy użytkownika do interfejsu aplikacji
        access_token = create_access_token(data={"sub": user.email})                              # Automatycznie logujemy użytkownika, poprzez stworzenie tokenu JWT i ustawienie go jako ciasteczko. 
        response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        # domain=".re-mind.xyz",                                               # ❌ Remove this - let browser handle domain automatically
        max_age=60 * 60 * 24,
        )
        return response                                                                          # Wysyłamy odpowiedź z gotowym plikiem cookie do przekierowania. 
    except jwt.ExpiredSignatureError:                                                            # Obsługujemy błędy w dwóch przypadkach, gdy : 
        raise HTTPException(status_code=400, detail="Verification link expired")                 # Link do weryfikacji wygasł
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid verification link")                 # Link do wetyfikacji był ,,invalid" 

# ──────────────────────────────────────────────────────────────────────────────
# Forgot + Reset Password
# ──────────────────────────────────────────────────────────────────────────────

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(request: EmailRequest):                             # Funckja jako argument bierze typ ,,Email Request" zdefiniowany powyżej
    mail = request.email                                                # Extractujemy ,,email" string z request body, tzn. z tego dicta.
    with SessionLocal() as db:                                          # Tworzymy nową sesję DB.
        user = db.query(User).filter(User.email == mail).first()        # Ta część sprawdza czy ,,user" z tym emailem istnieje
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token_data = {                                                  # Jeżeli user faktycznie istnieje, tworzymy dane dla ,,JWT reset token" 
            "sub": user.email,                                          # "sub" --> subject --> Stores the email, 
            "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES), # "exp" --> expiration time --> Znaczy że ten token będzie działał tylko przez określony czas
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM) # Ta część tworzy token JWT z danych używając do tego ,,secret key" 
        send_password_reset_email(user.email, token) # wołamy customową ,,send email function", który wysyła nam link do resetowania hasła.
        return {"message": "Reset email sent"}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):             # Funkcja jako argument bierze typ ,,ResetPasswordRequest" zdefiniowany powyżej.
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])        # dekodujemy token JWT przy pomocy ,,secret key" 
        email = payload.get("sub")                                                  # payload to dict, dlatego używamy ,,get", by wyciągnć ,,email"
        if not email:                                                               # Jeżeli email jest niepoprawny albo wygasł:
            raise HTTPException(status_code=400, detail="Invalid token")            # Raisujemy error 
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")     

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()                   # To tworzy sesję i próbuję znaleźć usera poprzez podany email
        if not user:
            raise HTTPException(status_code=404, detail="User not found")           # jeżeli user nie zostanie znaleziony zwracamy ,,error" 

                                                                                    # jeżeli user został znaleziony to : 
        hashed = get_password_hash(data.new_password)                               # hashujemy hasło przy pomocy bcrypt'a 
        user.hashed_password = hashed                                               # zastępujemy stare hasło nowym 
        db.commit()                                                                 # zapisujemy wszystko do bazy danych. 

    return {"message": "Password reset successful"}                                 # wysyłamy wiadomosć do frontendu, że reset hasła przebiegł poprawnie 
