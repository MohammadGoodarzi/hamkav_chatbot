# app/main.py
from fastapi import FastAPI, Depends
from .db.database import engine
from .db.queries import get_user_by_id

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int, user = Depends(get_user_by_id)):
    return {"user": user}