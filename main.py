"""
Chuda
"""

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="./web"), name="static")


@app.get("/")
async def index(_: fastapi.Request):
    """index page"""
    return FileResponse("./web/index.html", media_type="text/html")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
