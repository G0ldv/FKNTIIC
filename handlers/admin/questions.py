import re
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import main_menu
from database import log_section_click
from utils.navigation import replace_nav

router = Router()
ADMIN_CHAT_ID = 1779431249 

class QuestionState(StatesGroup):
    waiting_for_question = State()

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_question")]
    ])

@router.message(F.text == "❓ Поставити запитання")
async def ask_question_start(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("❓ Поставити запитання")
    await replace_nav(
        message, state,
        text="✍️ <b>Напишіть своє запитання одним повідомленням.</b>\n\n"
             "Адміністратор отримає його і надасть відповідь найближчим часом.\n"
             "Якщо передумали — тисніть кнопку нижче 👇",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(QuestionState.waiting_for_question)

@router.callback_query(F.data == "cancel_question")
async def cancel_question_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await replace_nav(
        callback.message, state,
        text="❌ Дію скасовано. Оберіть розділ:",
        reply_markup=main_menu
    )
    await callback.answer()

@router.message(QuestionState.waiting_for_question)
async def forward_question_to_admin(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Будь ласка, надішліть питання саме текстом.")
        return
    username = f"@{message.from_user.username}" if message.from_user.username else "Без юзернейму"
    admin_text = (
        f"❓ <b>Нове запитання!</b>\n"
        f"👤 Від: {username} (ID: {message.from_user.id})\n\n"
        f"📝 <b>Текст:</b> {message.text}"
    )
    await message.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)
    await replace_nav(
        message, state,
        text="✅ <b>Ваше запитання надіслано!</b>\n\n"
             "Ми отримали ваше звернення. Очікуйте на відповідь у цьому чаті. 😊",
        reply_markup=main_menu,
        save_history=True 
    )
    await state.set_state(None)

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
            await message.reply("✅ Відповідь успішно надіслано!")
        except Exception as e:
            await message.reply(f"❌ Помилка: {e}")