import fractions
from contextlib import asynccontextmanager
from email.policy import default
from http.client import HTTPException
from uuid import uuid4

import fastapi
from fastapi import Form, FastAPI
from pip._internal.cli import status_codes
from pydantic import BaseModel
from starlette import status
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from pathlib import Path
from pydantic import BaseModel
import candidates

class ScoreData(BaseModel):
    candidate: str
    score: float
    fractions: str




app = fastapi.FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/", StaticFiles(directory=os.path.dirname(os.path.abspath(__file__)), html=True), name="root")

async def File_Response1(data_path: str) -> FileResponse:
    """1. Проверка файла, при его отсутствии возращает ошибку 404 (File not found), если этот файл есть,
    то мы возращаем FileResponse, в котором находится расположенный файл (будущая ссылка)"""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {path} не найден")
    return FileResponse(path=str(path))



@app.get("/")
async def responce_file():
    """Возращает главное окно приложение"""
    return await File_Response1(r"C:\Users\админ\PycharmProjects\PythonProject2\index.html")

@app.get('/admins')
async def admins():
    """Возращает главное окно приложение"""
    return await responce_file()

@app.get('/onlines')
async def onlines():
    """В будущем принаджелит удалению из-за бесполезности этой функции"""
    return {'Online': "players" } # Заполнить FileResponce

# /interview


@app.get('/interview')
async def interview() -> FileResponse:
    """2. Возращаем функцию, но туда вставляем ссылку """
    return await File_Response1(r'C:\Users\админ\PycharmProjects\PythonProject2\sobes_index.html')



@app.post('/add_sobes/score', status_code=status.HTTP_201_CREATED)
async def scores1( data: ScoreData):
    print(f"📥 Получены данные: {data}")
    print(f"📥 candidate: {data.candidate}, score: {data.score}")
    from Qustion_scores import Add_scores, scores_add, main_score
    payload = Add_scores(scores=data.score, lvl=1)
    result = await scores_add(payload)
    print('Result ', result)
    return result
    ...
    # score = await Qustion_scores.score
    # print(f'Score: {score}, max_score: max_score')
    # return await Qustion_scores.main_score()
    #     #Qustion_scores.scores_add()


@app.post('/add_sobes', status_code=status.HTTP_201_CREATED)
async def add_sobes(username: str = Form(...),rang: int = Form(...),fraction: str = Form(...),time: str = Form(...)):
    """Обработка post запроса, работает вместе с функцией users_post и с классом Users_Post в файле candidates.py,
    создаем переменную, туда мы закидываем из класса поля присваивая параметры функции,
     потом мы создаем новую переменную и присваиваем асинхронную функцию, после этого возращаем эту переменную"""
    from candidates import users_post, Users_Post

    payload = Users_Post(username=username, rang=rang, fraction=fraction, time=time)
    result = await users_post(payload)
    print('Result ', result)
    return  await File_Response1(r'C:\Users\админ\PycharmProjects\PythonProject2\sobes_index2.html')

@app.post('/add_sobes/users', status_code=status.HTTP_201_CREATED)
async def add_sobes(username: str = Form(...)) -> FileResponse:
    """добавление участника в таблицу"""
    from candidates import add_candidates_post, users_add, users
    payload = add_candidates_post(
        username=username,
        # fraction=data
        # rang=users.set().get('rang'),
        # fraction=
    )


    result = await users_add(payload)
    print("result")
    return result


@app.patch('/add_sobes/users/{user_id}')
async def user_patch(payload: candidates.Users_Patch, user_id:str):
    """Изменение ника,планируется еще добавить изменение ранга, фракции"""
    return await candidates.users_patch(payload,user_id=user_id)

@app.delete('/add_sobes/users/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(task_id:str):
    """Удаление кандидата из таблицы"""
    return await candidates.users_delete(task_id=task_id)


@app.get('/add_sobes')
async def users():
    """возращаем юзеров"""
    from candidates import users
    print('Users ', users)
    return users

@app.get('/inactives')
async def inactives():
    return {'Online22': "players" } # Заполнить FileResponce

@app.get('/shop')
async def shop():
    return {'Online33': "players" } # Заполнить FileResponce


if __name__ == "__main__":
    print('ЗАПУСК')
    uvicorn.run(app, host="127.0.0.1", port=8000)