from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
from keyboards.main_menu import main_menu
from database import add_user
from utils.navigation import replace_nav

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await add_user(
        user_id=message.from_user.id, 
        full_name=message.from_user.full_name, 
        username=message.from_user.username
    )
    photo = "assets/images/logo.jpg"
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
    await replace_nav(message, state, text=welcome_text, photo_path=photo, reply_markup=main_menu, is_welcome=True)

@router.message(Command("restart"))
async def command_restart_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    text = (
        "🔄 <b>Бот перезапущений!</b>\n"
        "Головне меню активовано."
    )
    await replace_nav(message, state, text=text, reply_markup=main_menu)

@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(None)
    text = (
        "Ви повернулися в головне меню. Оберіть розділ: 👇"
    )
    await replace_nav(message, state, text=text, reply_markup=main_menu)