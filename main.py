from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from database import engine, Article, user_id, TaskCreate
from sqlalchemy.orm import Session

app = FastAPI()




class Task(BaseModel):
    title: str
    done: bool

class ArticleInput(BaseModel):
    title : str
    content : str


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    

class UserInDB(User):
    hashed_password: str


# 8.5
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")         # ta linia tworzy ,,password hashing manager"

def verify_password(plain_password, hashed_password):                     # ta funkcja jest używana podczas logowania by sprawdzić czy hasło jest ,,poprawne".
    return pwd_context.verify(plain_password, hashed_password)                

def get_password_hash(password):                                          # ta funkcja hashuję hasło, kiedy user się rejestruję.
    return pwd_context.hash(password)

# 8.6
def get_user(db, username: str):                   # Ta funkcja --> 1. wyszukuję użytkownika w databas'e db
    if username in db:                             # 1. Jeżeli username istnieje wyciąga wartość (user_dict), czyli po prostu ten dict taki z userem
        user_dict = db[username]                   # 3. Buduję obiekt UserInDB z dictionary --> UserInDB(**user_dcit)
        return UserInDB(**user_dict)

# 8.7 
def authenticate_user(db, username: str, password: str):                             # Ta funkcja sprawdza, czy user jest prawdziwy i czy istnieje
    user = get_user(db, username)
    if not user:                                                                     # Jeżeli user nie istnieję w w bazie danych, zwróć false i odrzuć logowanie.
        return False
    if not verify_password(password, user.hashed_password):                          # Tutaj prównujesz to co wpisał user i hashed password, jeżeli nie jest takie same zwróć Fals
        return False
    return user              # Jeżeli wszystko jest dobrze (user jest dobry i password jest dobre), następnie zwracamy obiekt UserInDB, który może zostać użyty do wygenerowania tokenu

# 8.8
def create_access_token(data: dict, expires_delta: timedelta | None= None):                           # ta lini definuję funkcję, która bierze dane, python dictionary, info, które chcesz zakodowaćw tokenie.
    to_encode = data.copy()                                                                           # kopiujesz dane wejściowe by ograniczyć zmienianie orginału poza funkcją
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))                             # to ustawia jak długo JWT token powinien istnieć,używasz custom --> expires_delta, deafultowo jest 15 minut
    to_encode.update({"exp": expire})                                                                 # dodaję do danych ,,expire" czyli to co ustawiłeś w poprzedniej linijcę, znacznik czasu wygaśnięcia.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)                                     # To tworzy faktyczny token ,,JWT", bierze twoję dane, enkryptuję je przy pomocy ,,SECRET_KEY", używa algorytmu HS256, zwraca ,,secure token string (JWT)"

#8.9
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")                                                # ta linia bierze token JWT i ci go daję, gdy o nią poprosisz


#8.10
#ta funkcja bierze token JWT, z requesta weryfikuję go, dekoduję go i zwraca zalogowanego użytkownika
async def get_current_user(token: str = Depends(oauth2_scheme)):              #Jako input bierzę Depends(oauth2_scheme), to bierze Authorization : Bearer <TOKEN>. Teraz ,,token" zawiera surowy string z tokenem JWT                               
    credentials_exception = HTTPException(                                    # To jest typowy standardowy response, gdy coś się zepsuję
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"},
    )
    try:                                                                                  # Tutaj próbujemy zdekodować token.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                   # Dekodujemy token używając ,,SECRET_KEY"
        username: str = payload.get("sub")                                                # Jeżeli token jest walidny, dostajemy ,,payload" i dane, którę są w środku.
        if username is None:
            raise credentials_exception
    except JWTError:                                                                      # Jeżeli token jest zepsuty lub przeterminowany
        raise credentials_exception                                                       # podnieś error 401 Unauthorized

    user = get_user(fake_users_db, username)                                              # używamy już istniejącej funkcji get_user() by wydobyć użytkowników z ,,database"
    if user is None:
        raise credentials_exception                                                       # Jeżeli nie znaleziono żadnych użytkownikó podniosimy error 401
    return user


# 8.11
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):   # Tworzy punkt końcowy ,,POST" w /token, ta droga jest wzywana, gdy user próbuję się zalogować. form_data to jest login form, który przychodzi z frontendu, automatycznie analizuję nazwę użytkownika i hasło z żądania logowania
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)   # Używa funkcji ,,authenticate_user(), próbuję znaleźć użytkownika po username, sprawdza czy hasło jest poprawnę, jeżeli nie jest zwraca False                           
    if not user:
        raise HTTPException(            # Jeżeli  user nie istnieję lub hasło jest niepoprawnę zwraca error 401.
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)     # ta linijka, mówi jak długo token powinien istnieć
    access_token = create_access_token(              # tutaj jest używana funkcja, która tworzy token
        data={"sub": user.username},                 # tutaj są dane, które należą do JWT, sub = 'subject', to jest użytkownik, do którego należy token
        expires_delta=access_token_expires           # tutaj jest opisane jak długo będzie trwał token
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 8.12
@app.get("/users/me")    # tworzy endpoint pod /users/me, jeżeli jakiś user się zaloguję dostanie swoję info
async def read_users_me(current_user: User = Depends(get_current_user)):           # Definiuję rzeczywistą funkcję pytona, gdy ktoś wejdzie pod /users/me               # Depends(get_current_user) --> jest to sposób by automatycznie uruchomić inną funkcję i przekazać jej wartość do funkcji końcowej
    return current_user   # To jest parametr, który zostanie wypełniony automatycznie z aktualnie zalogowanym użytkownikiem 


#9.2
@app.post("/tasks/")
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    db_task = Task(
        title=task.title,
        done=task.done,
        user_id=current_user.username
    )
    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        return db_task  

#9.3
@app.get("/tasks/")
def get_my_tasks(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        tasks = session.query(Task).filter(Task.user_id == current_user.username).all()
        return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    with Session(engine) as session:
        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task



tasks = [
        {"id": 1, "title": "Learn FastAPI", "done": False},
        {"id": 2, "title": "Build a project", "done": False}
        ]

@app.get("/tasks/")
async def return_list():
    return tasks


@app.post("/tasks/")
async def add_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": task.done
    }
    tasks.append(new_task)
    return new_task

@app.get("/tasks/{item_id}")
async def get_single_task(item_id: int):
    for task in tasks:
        if task["id"] == item_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
async def delete_task(id : int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted", "task": deleted_task}
        

@app.get("/articles/{article_id}")
async def fetch_from_database(article_id : int):
    with Session(engine) as session:
        article = session.query(Article).filter_by(id=article_id).first()
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return {
            "id": article.id,
            "title": article.title,
            "content": article.content
        }
    

@app.post("/articles/")
async def add_new_article(article: ArticleInput):
    new_article = Article(
        title=article.title,
        content=article.content
    )


    with Session(engine) as session:
        session.add(new_article)
        session.commit()
        session.refresh(new_article)

    return {
        "id": new_article.id,
        "title": new_article.title,
        "content": new_article.content
    }


@app.get("/articles/{article_id}")
async def get_single_article(article_id : int):
    with Session(engine) as session:
        article = session.query(Article).filter_by(id=article_id).first()

        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return {
            "id": article_id,
            "title" : article.title,
            "content": article.content
        }


@app.put("/articles/{article_id}")
async def update_task(article_id : int, updated_data: ArticleInput):
    
    with Session(engine) as session:
        article = session.query(Article).filter_by(id=article_id).first()

        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        
        article.title = updated_data.title
        article.content = updated_data.content

        session.commit()
        session.refresh(article)

        return {
            "id": article.id,
            "title": article.title,
            "content": article.content
        }
    


@app.delete("/article/{article_id}")
async def update_task(article_id : int):
    with Session(engine) as session:
        article = session.query(Article).filter_by(id=article_id).first()

        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        
        session.delete(article)
        session.commit()
        session.refresh(article)

        return "Article deleted"
    


@app.get("/articles")
async def return_articles():
    with Session(engine) as session:
        articles = session.query(Article).all()
        return articles