from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
from keyboards.main_menu import main_menu
from database import add_user

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await add_user(
        user_id=message.from_user.id, 
        full_name=message.from_user.full_name, 
        username=message.from_user.username
    )
    photo = FSInputFile("assets/images/logo.jpg")
    welcome_text = (
        f"👋 <b>Вітаємо у ФКНТІІС ОНТУ!</b>\n\n"
        f"Привіт, {message.from_user.full_name}! 😊\n"
        f"Я — твій віртуальний помічник. Тут ти знайдеш усе необхідне для вступу до нашого коледжу:\n\n"
        f"🎓 <b>Спеціальності</b> — детально про кожний напрямок.\n"
        f"💰 <b>Вартість навчання</b> — актуальні ціни та документи.\n"
        f"📅 <b>Правила прийому</b> — терміни та умови.\n"
        f"📍 <b>Локація та контакти</b> — де ми та як зв'язатися.\n\n"
        f"Обери потрібний розділ у меню нижче 👇"
    )

    await message.answer_photo(
        photo=photo,
        caption=welcome_text,
        reply_markup=main_menu
    )

@router.message(Command("restart"))
async def command_restart_handler(message: Message):
    await message.answer(
        "🔄 <b>Бот перезапущений!</b>\n"
        "Головне меню активовано.",
        reply_markup=main_menu
    )    