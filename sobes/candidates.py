from uuid import uuid4
import fastapi
from fastapi import *
from pip._internal.resolution.resolvelib import candidates
from pydantic import BaseModel
from uvicorn import *
from dotenv import load_dotenv
from datetime import datetime
import os


app = FastAPI()

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


users: list[User] = []


@app.get("/")
async def window():
    return users

@app.post('/users')
async def users_post(payload: Users_Post) -> User:
    new_user = User(id=str(uuid4()), username=payload.username, rang=payload.rang, lvl=0, fraction=payload.fraction, data_time=payload.time)
    users.append(new_user)
    return new_user

@app.patch('/users/{user_id}')
async def users_patch(payload: Users_Patch, user_id: str):
    for user in users:
        if user.id == str(user_id):
            if payload.username is not None:
                user.username = payload.username
            if payload.rang is not None:
                user.rang = payload.rang
            if payload.fraction is not None:
                user.fraction = payload.fraction


@app.post("/question/{name}")
async def question_func(self) -> dict:

    load_dotenv()
    question_all = os.getenv('question')

    if self.username not in candidates:
        raise fastapi.HTTPException(status_code=400, detail=f"There is no such candidate. {self.candidates.items()}")

    if question_all is None:
        raise fastapi.HTTPException(status_code=400, detail="Question is required")

    for question in question_all:
        pass



if __name__ == '__main__':
    run(app=app)