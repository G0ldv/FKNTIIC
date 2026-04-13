from os import getenv
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from handlers import router as start_router
from handlers.admission import router as admission_router
from handlers.admin import router as admin_router
from handlers.college import router as college_router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

session = AiohttpSession(proxy="http://proxy.server:3128")

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(admission_router)
dp.include_router(admin_router)
dp.include_router(college_router)

async def main():
    # bot = Bot(token=TOKEN)
    bot = Bot(token=TOKEN, session=session)
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота 🚀"),
        BotCommand(command="restart", description="🔄 Перезапустити бота"),
    ])
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())