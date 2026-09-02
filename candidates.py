from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapped, mapped_column, sessionmaker
from uvicorn import lifespan


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class UserORM(Base):
    __tablename__ = 'users'

    username: Mapped[str]
    rang: Mapped[int]
    fraction: Mapped[str]
    lvl: Mapped[int]
    data_time: Mapped[str]


class User(BaseModel):
    id: str
    username: str
    rang: int
    fraction: str
    lvl: int
    data_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # год-месяц-день час:минута:секунда

class Users_Post(BaseModel):
    username: str
    rang: int
    fraction: str
    time: str

class Users_Patch(BaseModel):
    username: str | None = None
    rang: int | None = None
    fraction: str | None = None


class add_candidates_post(BaseModel):
    username: str
    # rang: int | None = None
    # fraction: str | None = None

users: List[User] = []


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield
async def get_db():
    with session() as db:
        yield db


async def window(db: Session = Depends(get_db)):
    """Возращение списка users(SELECT * FROM users)"""
    users_db = db.scalars(select(UserORM)).all()
    print('UsersDB ', users_db)
    return users, users_db

async def users_post(payload: Users_Post) -> User:
    """Добавление пользователей через main Form"""
    new_user = User(username=payload.username, rang=payload.rang, lvl=0, fraction=payload.fraction, data_time=payload.time)
    return new_user


async def users_add(payload: add_candidates_post) -> User:
    """Добавление в табоицу кандидатов"""
    new_user = User(id=str(uuid4()),username=payload.username,rang=0,lvl=0,fraction="Не указано",data_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    users.append(new_user)
    return new_user

async def users_patch(payload: Users_Patch, user_id: str):
    """Изменение ника, ранга, фракции, можно выбирать один из этих"""
    for user in users:
        if user.id == str(user_id):
            if payload.username is not None:
                user.username = payload.username
            if payload.rang is not None:
                user.rang = payload.rang
            if payload.fraction is not None:
                user.fraction = payload.fraction
            return user
    return None


async def users_delete(task_id: str):
    for task in users:
        if task.id == task_id:
            users.remove(task)
        return task
    return None