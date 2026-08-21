
from http.client import HTTPException
from uuid import uuid4

import fastapi
from fastapi import Form
from pydantic import BaseModel
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path
app = fastapi.FastAPI()



#app.mount("/", StaticFiles(directory=os.path.dirname(os.path.abspath(__file__)), html=True), name="root")

@app.get("/")
async def responce_file():
    return FileResponse("index.html")

@app.get('/admins')
async def admins():
    return await responce_file()

@app.get('/onlines')
async def onlines():
    return {'Online': "players" } # Заполнить FileResponce



async def interview_File_Response(data_path: str) -> FileResponse:
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Фай {path} не найден")
    return FileResponse(path=str(path))

@app.get('/interview')
async def interview() -> FileResponse:
    return FileResponse(r'C:\Users\админ\PycharmProjects\PythonProject2\sobes\sobes_index.html')

@app.post('/add_sobes')
async def add_sobes(
    username: str = Form(...),
    rang: int = Form(...),
    fraction: str = Form(...),
    time: str = Form(...)
):

    from sobes.candidates import users_post, Users_Post

    payload = Users_Post(username=username, rang=rang, fraction=fraction, time=time)
    result = await users_post(payload)
    print(result)
    return result

async def add_sobes_file_responce(date_path: str) -> FileResponse:
    path = Path(date_path)
    if not path.exists():
        raise FileNotFoundError('File not found')
    return FileResponse(path=str(path))

@app.get('/add_sobes')
async def users():
    from sobes.candidates import users
    print(users)
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