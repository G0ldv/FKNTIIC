import re
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import remove_menu, main_menu
from database import log_section_click

router = Router()

ADMIN_CHAT_ID = 1779431249 

def get_cancel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_question")]
    ])
    return keyboard

class QuestionState(StatesGroup):
    waiting_for_question = State()

@router.message(F.text == "❓ Поставити запитання")
async def ask_question_start(message: Message, state: FSMContext):
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    await state.clear()
    await log_section_click("❓ Поставити запитання")
    await message.delete()
    temp_msg = await message.answer("⏳", reply_markup=remove_menu)
    await temp_msg.delete()
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except:
            pass
    sent_message = await message.answer(
        "✍️ Напишіть своє запитання одним повідомленням.\n\n"
        "Якщо передумали, натисніть кнопку нижче 👇",
        reply_markup=get_cancel_keyboard()
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await state.set_state(QuestionState.waiting_for_question)

@router.callback_query(F.data == "cancel_question")
async def cancel_question_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    sent_message = await callback.message.answer("❌ Дію скасовано. Оберіть розділ:", reply_markup=main_menu)
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer()

@router.message(QuestionState.waiting_for_question)
async def forward_question_to_admin(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Будь ласка, надішліть питання текстом.")
        return
    data = await state.get_data()
    last_id = data.get("last_menu_msg_id")
    if last_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_id)
        except:
            pass
    username = f"@{message.from_user.username}" if message.from_user.username else "Без юзернейму"
    admin_text = (
        f"❓ <b>Нове запитання!</b>\n"
        f"👤 Від: {username} (ID: {message.from_user.id})\n\n"
        f"📝 <b>Текст:</b> {message.text}"
    )
    await message.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)
    await message.answer(
        "✅ Ваше запитання надіслано! Очікуйте на відповідь.",
        reply_markup=main_menu
    )
    await state.clear()


@router.message(F.from_user.id == ADMIN_CHAT_ID, F.reply_to_message)
async def admin_reply_handler(message: Message):
    original_text = message.reply_to_message.text
    if not original_text:
        return
    match = re.search(r"ID:\s*(\d+)", original_text)
    if match:
        user_id = int(match.group(1))
        try:
            await message.bot.send_message(
                chat_id=user_id,
                text="📩 <b>Відповідь від приймальної комісії:</b>"
            )
            await message.copy_to(chat_id=user_id)
            await message.reply("✅ Відповідь успішно надіслано абітурієнту!")
        except Exception as e:
            await message.reply(f"❌ Помилка надсилання: користувач заблокував бота або сталася помилка.\n{e}")