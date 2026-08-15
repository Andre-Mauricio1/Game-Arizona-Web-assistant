import fastapi
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os


app = fastapi.FastAPI()
# app.mount("/", StaticFiles(directory=os.path.dirname(os.path.abspath(__file__)), html=True), name="root")

@app.get("/")
async def responce_file():
    return FileResponse("./index.html")

@app.get('/admins')
async def admins():
    return await responce_file()

@app.get('/onlines')
async def onlines():
    return {'Online': "players" } # Заполнить FileResponce

@app.get('/interview')
async def interview():
    return {'Online11': "players" } # Заполнить FileResponce

@app.get('/inactives')
async def inactives():
    return {'Online22': "players" } # Заполнить FileResponce

@app.get('/shop')
async def shop():
    return {'Online33': "players" } # Заполнить FileResponce



if __name__ == "__main__":
    uvicorn.run(app)