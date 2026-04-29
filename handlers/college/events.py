from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu
from database import log_section_click

router = Router()

def get_events_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Дні відкритих дверей", callback_data="days")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📅 Заходи")
async def open_events_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    await state.clear()
    await log_section_click("📅 Заходи")
    temp_msg = await message.answer("Завантажую...", reply_markup=ReplyKeyboardRemove())
    await temp_msg.delete()
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except:
            pass
    await message.answer(
        "✨ <b>Заходи нашого коледжу</b>\n\n"
        "Оберіть пункт, щоб дізнатися деталі:",
        reply_markup=get_events_keyboard()
    )
    await message.delete()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    sent_message = await callback.message.answer(
        "Ви повернулися в головне меню. Оберіть розділ: 👇",
        reply_markup=main_menu
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer()

@router.callback_query(F.data == "events")
async def events_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "✨ <b>Заходи нашого коледжу</b>\n\n"
        "Оберіть пункт, щоб дізнатися деталі:",
        reply_markup=get_events_keyboard()
    )
    await callback.answer()