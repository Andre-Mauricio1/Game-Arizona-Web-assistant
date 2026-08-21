import fastapi
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path

app = fastapi.FastAPI()
app.mount("/", StaticFiles(directory=os.path.dirname(os.path.abspath(__file__)), html=True), name="root")


@app.get("/")
async def root():
    return FileResponse("static/sobes_index.html")


if __name__ == "__main__":
    uvicorn.run(app)