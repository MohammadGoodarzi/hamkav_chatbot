# app/db/queries.py
from sqlalchemy.sql import text
from .database import get_db
from fastapi import Depends

async def get_user_by_id(user_id: int, session = Depends(get_db)):
    result = await session.execute(
        text("SELECT * FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    )
    return result.fetchone()

async def get_products(session = Depends(get_db)):
    result = await session.execute(
        text("SELECT * FROM products")
    )
    return result.fetchall()