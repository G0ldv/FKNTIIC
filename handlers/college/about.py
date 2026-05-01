from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_about_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Історія та заснування", callback_data="history_more")],
        [InlineKeyboardButton(text="🌳 Дендропарк «Студентський»", callback_data="park_more")],
        [InlineKeyboardButton(text="🤝 Студентське самоврядування", callback_data="governance_more")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "🏫 Про коледж")
async def about_main_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("🏫 Про коледж")
    text = (
        "🏛 <b>Ласкаво просимо до нашого Коледжу!</b>\n\n"
        "КНТІІС ОНТУ — це не просто навчальний заклад, це місце з історією, "
        "власним заповідником та активним студентським життям.\n\n"
        "Оберіть, що саме вас цікавить: 👇"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_about_menu_keyboard()
    )

@router.callback_query(F.data == "open_about_menu")
async def open_about_menu(callback: CallbackQuery, state: FSMContext):
    text = (
        "🏛 <b>Розділ про коледж:</b>\n\nОберіть цікавий для вас пункт:"
    )
    await replace_nav(
        callback.message, state, text=text, reply_markup=get_about_menu_keyboard()
    )
    await callback.answer()