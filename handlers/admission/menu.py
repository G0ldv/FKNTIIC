from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import remove_menu, main_menu
from database import log_section_click

router = Router()

def get_admission_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Правила вступу", callback_data="rules")],
        [InlineKeyboardButton(text="📑 Необхідні документи", callback_data="docs")],
        [InlineKeyboardButton(text="🎓 Підготовчі курси", callback_data="prep_courses")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")],
    ])
    return keyboard

@router.message(F.text == "🎓 Вступ")
async def admission_menu(message: Message, state: FSMContext):
    await log_section_click("🎓 Вступ")
    await message.delete()
    temp_msg = await message.answer("Завантажую розділ вступу...", reply_markup=remove_menu)
    await temp_msg.delete()
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except:
            pass
    await message.answer(
        "🎓 <b>Розділ вступника</b>\n\nОберіть потрібний пункт: 👇",
        reply_markup=get_admission_keyboard()
    )

@router.callback_query(F.data == "admission_menu")
async def back_to_admission_handler(callback: CallbackQuery):
    text = "🎓 <b>Розділ вступника</b>\n\nОберіть потрібний пункт: 👇"
    kb = get_admission_keyboard()
    if callback.message.document:
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=kb)
    else:
        await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    sent_message = await callback.message.answer(
        "Ви повернулися в головне меню. Оберіть розділ: 👇",
        reply_markup=main_menu
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer() 