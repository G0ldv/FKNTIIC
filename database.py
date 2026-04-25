from os import getenv
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = getenv("DATABASE_URL")

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                phone TEXT
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS section_stats (
                section_name TEXT PRIMARY KEY,
                click_count INTEGER DEFAULT 0
            )
        ''')

async def log_section_click(section_name: str):
    pool = await get_pool()
    await pool.execute('''
        INSERT INTO section_stats (section_name, click_count)
        VALUES ($1, 1)
        ON CONFLICT (section_name) 
        DO UPDATE SET click_count = section_stats.click_count + 1
    ''', section_name)

async def get_sections_stats():
    pool = await get_pool()
    rows = await pool.fetch('SELECT section_name, click_count FROM section_stats ORDER BY click_count DESC')
    return rows

async def add_user(user_id, full_name=None, username=None):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO users (user_id, full_name, username)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO UPDATE 
            SET full_name = EXCLUDED.full_name, 
                username = EXCLUDED.username
        ''', user_id, full_name, username)

async def get_users_count():
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval('SELECT COUNT(*) FROM users') or 0

async def get_all_users():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT user_id FROM users')
        return [row['user_id'] for row in rows]

async def get_all_users_full():
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT user_id, full_name, username, phone FROM users')