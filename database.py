from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URL
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from pydantic import BaseModel

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

conn = engine.connect()

Base = declarative_base()

user_id = Column(String, ForeignKey("users.username"))       # 9.1

class TaskCreate(BaseModel):
    title : str
    done : bool



class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)

first_article = Article (
    title = "jak pokonać Olka",
    content = "Walka z Olkiem 1vs1 wymaga dużej sprawności, głównie fizycznej ale również intelektualnej"
)


second_article = Article (
    title = "jak zażywac marihuanę i nie zwariować?",
    content = "Jeżeli chcesz zażywać marihuanę i nie zwariować najlepiej łącz ją z CBD to polepsze efekt "
)




with Session(engine) as session:
   session.add(first_article)
   session.add(second_article)
   session.commit()


#Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)