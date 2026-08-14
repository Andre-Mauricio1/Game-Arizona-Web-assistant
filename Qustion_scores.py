from http.client import HTTPException

import fastapi
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os
import random

load_dotenv()
app = FastAPI()

class Question(BaseModel):
    question: str
    scores: float
    lvl: int

class ADD_Question(BaseModel):
    Question: str
    scores: float
    lvl: int

# question_super = []


async def question_func_get():
    question_all =  os.getenv('questions')
    question = question_all.split('?')
    question1 = random.choice(question) + "?"

    # question_super.append(question)

    print(question1)
    return question, question1 #, question_super

@app.get('/questions')
async def main():
    return await question_func_get()

@app.post('/question')
async def add_question(payload: ADD_Question):
    quest, quest1 = await question_func_get()
    if payload.lvl >= 1:
        add_question_a = Question(question=payload.Question, scores=payload.scores, lvl=payload.lvl)
        quest.append(payload.Question)
        # question_super.append(payload.Question)
        return add_question_a, quest
    else:
        raise fastapi.HTTPException(status_code=403, detail='Forbidden')

if __name__ == "__main__":
    uvicorn.run(app)

