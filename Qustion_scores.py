from http.client import HTTPException
from typing import List

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
    question: str | None
    scores: float
    lvl: int =1

class Add_scores(BaseModel):
    scores: float
    lvl: int =1


class ADD_Question(BaseModel):
    Question: str
    scores: float
    lvl: int =1

# question_super = []
score = []


#
# @app.get("/add_scores")
async def main():
    return score

# @app.post("/add_scores")
async def scores_add(payload: Add_scores):
    """Изменение баллов кандидату"""
    if payload.lvl >= 1:
        new_score = Question(question=None, scores=payload.scores, lvl=payload.lvl)
        score.append(payload.scores)
        max_score = max(score)
        print(f'Score: {score}, max_score: {max_score}' )


async def question_func_get():
    """Меняется вопрос РАНДОМНО"""
    question_all =  os.getenv('questions')
    question = question_all.split('?')
    question1 = random.choice(question) + "?"

    # question_super.append(question)

    print(question1)
    return question, question1 #, question_super

@app.get("/add_question")
async def main():
    return await question_func_get()


async def add_question(payload: ADD_Question):
    """Берем 1 часть вопроса(quest)"""
    quest, quest1 = await question_func_get()
    if payload.lvl >= 1:
        add_question_a = Question(question=payload.Question, scores=payload.scores, lvl=payload.lvl)
        quest.append(payload.Question)
        # question_super.append(payload.Question)
        return add_question_a, quest
    else:
        raise fastapi.HTTPException(status_code=403, detail='Forbidden')
#
# if __name__ == "__main__":
#     uvicorn.run(app)

