from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_name = Column(String(), nullable=False)
    deadline = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)