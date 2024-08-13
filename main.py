import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
async def index(_: fastapi.Request):
    return FileResponse("index.html", media_type="text/html")

@app.post("/api/signup")
async def signup(_: fastapi.Request):
    return FileResponse("signup.html", media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
