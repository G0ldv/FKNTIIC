from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu
from database import log_section_click
from utils.navigation import replace_nav, edit_nav

router = Router()

def get_admission_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Правила вступу", callback_data="rules")],
        [InlineKeyboardButton(text="📅 Терміни вступу", callback_data="deadlines")],
        [InlineKeyboardButton(text="📑 Необхідні документи", callback_data="docs")],
        [InlineKeyboardButton(text="🎓 Підготовчі курси", callback_data="prep_courses")],
        [InlineKeyboardButton(text="📝 Вступні випробування", callback_data="entrance_exams")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")],
    ])
    return keyboard

@router.message(F.text == "🎓 Вступнику")
async def admission_menu(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("🎓 Вступнику")
    text = (
        "🎓 <b>Розділ вступника</b>\n\nОберіть потрібний пункт: 👇"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_admission_keyboard()
    )

@router.callback_query(F.data == "admission_menu")
async def back_to_admission_handler(callback: CallbackQuery, state: FSMContext):
    text = "🎓 <b>Розділ вступника</b>\n\nОберіть потрібний пункт: 👇"
    await edit_nav(
        callback.message, state, text=text, reply_markup=get_admission_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    text = (
        "Ви повернулися в головне меню. Оберіть розділ: 👇"
    )
    await replace_nav(
        callback.message, state, text=text, reply_markup=main_menu
    )
    await callback.answer() 