from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

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
    await message.delete()
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except: pass
    temp_msg = await message.answer("⌛", reply_markup=ReplyKeyboardRemove())
    await temp_msg.delete()
    await message.answer(
        "🏛 <b>Ласкаво просимо до нашого Коледжу!</b>\n\n"
        "КНТІІС ОНТУ — це не просто навчальний заклад, це місце з історією, "
        "власним заповідником та активним студентським життям.\n\n"
        "Оберіть, що саме вас цікавить: 👇",
        reply_markup=get_about_menu_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "open_about_menu")
async def open_about_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏛 <b>Розділ про коледж:</b>\n\nОберіть цікавий для вас пункт:",
        reply_markup=get_about_menu_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    sent_message = await callback.message.answer(
        "Ви повернулися до головного меню. Оберіть розділ: 👇",
        reply_markup=main_menu
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer()