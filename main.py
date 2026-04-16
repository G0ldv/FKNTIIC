import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from database import init_db
from handlers import router as start_router
from handlers.admission import router as admission_router
from handlers.admin import router as admin_router
from handlers.college import router as college_router

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
 
class ParseModeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Отримуємо об'єкт бота з даних
        bot = data.get("bot")
        if bot:
            # Примусово оновлюємо властивості для поточного запиту
            bot.default.parse_mode = "HTML"
        return await handler(event, data)

async def main():
    await init_db() 
    
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)

    bot = Bot(token=TOKEN, default_bot_properties=default_properties)
    dp = Dispatcher()

    dp.update.outer_middleware(ParseModeMiddleware())

    dp.include_router(start_router)
    dp.include_router(admission_router)
    dp.include_router(admin_router)
    dp.include_router(college_router)

    await bot.delete_my_commands()
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота 🚀"),
        BotCommand(command="restart", description="Перезапустити бота 🔄"),
        BotCommand(command="admin", description="Панель адміна")
    ])

    print("Бот запущений і готовий до роботи...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")