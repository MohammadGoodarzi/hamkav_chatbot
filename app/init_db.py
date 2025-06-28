# init_db.py

import asyncpg
import asyncio
from config import DB_CONFIG

CREATE_SCHEMAS = """
    CREATE SCHEMA IF NOT EXISTS auth;
    CREATE SCHEMA IF NOT EXISTS dialog;
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS auth.users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    username VARCHAR(100) NOT NULL UNIQUE,
    fullname VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_shamsi_at integer,
    updated_shamsi_at integer
);
"""

CREATE_ROLES_TABLE = """
CREATE TABLE IF NOT EXISTS auth.roles (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_shamsi_at integer,
    updated_shamsi_at integer
);
"""

CREATE_USERS_ROLES_TABLE = """
CREATE TABLE auth.user_roles (
    user_id BIGINT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES auth.roles(id) ON DELETE CASCADE,
    created_shamsi_at integer,
    updated_shamsi_at integer
);
"""

CREATE_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS dialog.questions (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL,
    text TEXT NOT NULL,
    type TEXT DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_shamsi_at integer,
    updated_shamsi_at integer
);
"""

CREATE_ANSWERS_TABLE = """
CREATE TABLE IF NOT EXISTS dialog.answers (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id INTEGER NOT NULL,
    answer TEXT,
    created_at TIMESTAMP DEFAULT now(),
    created_shamsi_at integer
);
"""

async def init_db():
    conn = await asyncpg.connect(
        user=DB_CONFIG["db_user"],
        password=DB_CONFIG["db_password"],
        database=DB_CONFIG["db_database"],
        host=DB_CONFIG["db_host"],
        port=DB_CONFIG["db_port"],
    )
    print("✅ Connected to DataBase")

    await conn.execute(CREATE_SCHEMAS)
    await conn.execute(CREATE_USERS_TABLE)
    await conn.execute(CREATE_ROLES_TABLE)
    await conn.execute(CREATE_USERS_ROLES_TABLE)
    await conn.execute(CREATE_QUESTIONS_TABLE)
    await conn.execute(CREATE_ANSWERS_TABLE)

    print("✅ Tables are created ")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
