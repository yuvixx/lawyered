import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from dbcontroller import User


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
async def index(_: fastapi.Request):
    return FileResponse("index.html", media_type="text/html")


@app.post("/api/signup")
async def signup(req: fastapi.Request, user: User):
    data, status = user.commit()
    return JSONResponse(content=data, status_code=status)


@app.post("/api/signin")
async def signup(req: fastapi.Request):
    return await req.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
