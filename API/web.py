import json
from fastapi import FastAPI, Request
import uvicorn
from data import db_session

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# REGISTRATION
@app.post("/sign_up/")
async def create_user(request:  Request):
    body = await request.body()

    data = json.loads(body)
    username = data.get("username")
    password = data.get("password")

    print(username, password)
    return {"username": username, "password": password}


if __name__ == "__main__":
    db_session.global_init("db/db.db")
    uvicorn.run(
        "web:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоперезагрузка при изменениях
        log_level="info"
    )