import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await get_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            phone TEXT
        )
    ''')
    await conn.close()

async def add_user(user_id, full_name=None, username=None):
    conn = await get_connection()
    try:
        await conn.execute('''
            INSERT INTO users (user_id, full_name, username)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO UPDATE 
            SET full_name = EXCLUDED.full_name, 
                username = EXCLUDED.username
        ''', user_id, full_name, username)
    finally:
        await conn.close()

async def get_users_count():
    conn = await get_connection()
    count = await conn.fetchval('SELECT COUNT(*) FROM users')
    await conn.close()
    return count or 0

async def get_all_users():
    conn = await get_connection()
    rows = await conn.fetch('SELECT user_id FROM users')
    await conn.close()
    return [row['user_id'] for row in rows]

async def get_all_users_full():
    conn = await get_connection()
    rows = await conn.fetch('SELECT user_id, full_name, username, phone FROM users')
    await conn.close()
    return rows