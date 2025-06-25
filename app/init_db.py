# init_db.py

import asyncpg
import asyncio
from config import DB_CONFIG

CREATE_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    order_number INT NOT NULL,
    type TEXT DEFAULT 'text'
);
"""

CREATE_ANSWERS_TABLE = """
CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    answer TEXT,
    created_at TIMESTAMP DEFAULT now()
);
"""

async def init_db():
    conn = await asyncpg.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    )
    print("✅ اتصال برقرار شد")

    await conn.execute(CREATE_QUESTIONS_TABLE)
    await conn.execute(CREATE_ANSWERS_TABLE)

    print("✅ جدول‌ها بررسی و در صورت نیاز ایجاد شدند")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
