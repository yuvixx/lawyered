import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from dbcontroller import User, Chat

from urllib.request import Request, urlopen

import json

GEMINI_API_KEY = "AIzaSyBlgzboJRTvSHh952BGiyPQfdJJUEpUR9w"

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
async def index(_: fastapi.Request):
    return FileResponse("index.html", media_type="text/html")


@app.post("/api/signup")
async def signup(_: fastapi.Request, user: User):
    data, status = user.commit()
    headers = {"Set-Cookie": f"data={user.username}:{user.email}:{user.password}; Path=/;"}
    return JSONResponse(content=data, status_code=status, headers=headers)


@app.post("/api/signin")
async def signup(_: fastapi.Request, user: User):
    data, status = user.authenticate()
    headers = {"Set-Cookie": f"data={user.username}:{user.email}:{user.password}; Path=/;"}
    return JSONResponse(content=data, status_code=status, headers=headers)


@app.post("/api/chat")
async def chat_create(req: fastapi.Request, chat: Chat):
    user_data = req.cookies.get("data")
    if not user_data:
        return JSONResponse(content={"error": "user not authenticated"}, status_code=401)
    username, email, password = user_data.split(":")
    user = User(email=email, password=password, username=username)
    data, status = user.authenticate()
    # rest api stuff
    req = Request(
        f"https://generativelanguage.googleapis.com"
        f"/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}",
        method="POST"
    )
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req, json.dumps({"contents": [{"parts": [{"text": chat.message}]}]}).encode())
    return Response(content=resp.read(), status_code=200, media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
