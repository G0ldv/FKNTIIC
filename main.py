import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from database import init_db
from handlers import router as start_router
from handlers.admission import router as admission_router
from handlers.admin import router as admin_router
from handlers.college import router as college_router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

async def main():
    init_db()
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(admission_router)
    dp.include_router(admin_router)
    dp.include_router(college_router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота 🚀"),
        BotCommand(command="restart", description="Перезапустити бота 🔄"),
        BotCommand(command="admin", description="Панель адміна 🔐")
    ])

    print("Бот запущений і готовий до роботи...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")