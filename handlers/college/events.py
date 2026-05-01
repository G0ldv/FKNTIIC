from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_events_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Дні відкритих дверей", callback_data="days")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📅 Заходи")
async def open_events_menu(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("📅 Заходи")
    text = (
        "✨ <b>Заходи нашого коледжу</b>\n\n"
        "Оберіть пункт, щоб дізнатися деталі:"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_events_keyboard()
    )

@router.callback_query(F.data == "events")
async def events_menu_callback(callback: CallbackQuery, state: FSMContext):
    text = (
        "✨ <b>Заходи нашого коледжу</b>\n\n"
        "Оберіть пункт, щоб дізнатися деталі:"
    )
    await replace_nav(
        callback.message, state, text=text, reply_markup=get_events_keyboard()
    )
    await callback.answer()