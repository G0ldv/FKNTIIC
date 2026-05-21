import re
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from keyboards.main_menu import main_menu
from utils.navigation import replace_nav
import database as db

router = Router()

SUPPORT_GROUP_ID = -1003906546155 

class QuestionState(StatesGroup):
    waiting_for_question = State() 
    in_chat = State()              

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_question")]
    ])

def get_close_chat_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏁 Завершити діалог")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def create_new_topic(bot: Bot, message: Message, user_id: int) -> int:
    username = f" @{message.from_user.username}" if message.from_user.username else ""
    topic = await bot.create_forum_topic(
        chat_id=SUPPORT_GROUP_ID,
        name=f"{message.from_user.full_name}{username}"
    )
    topic_id = topic.message_thread_id
    await db.save_topic_id(user_id, topic_id)
    await bot.send_message(
        chat_id=SUPPORT_GROUP_ID,
        message_thread_id=topic_id,
        text=f"🆕 <b>Новий діалог!</b>\n👤 Користувач: {message.from_user.full_name}\n🆔 ID: <code>{user_id}</code>"
    )
    return topic_id

async def perform_close_chat(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    topic_id = await db.get_topic_id(user_id)
    if topic_id:
        try:
            await bot.send_message(
                chat_id=SUPPORT_GROUP_ID,
                message_thread_id=topic_id,
                text="🏁 <b>Користувач завершив діалог.</b>"
            )
        except Exception:
            pass
    await state.clear()
    await message.answer(
        text="Раді були допомогти! 😊\nЯкщо виникнуть якісь запитання — звертайтесь.", 
        reply_markup=main_menu
    )

@router.message(F.text == "❓ Поставити запитання")
async def ask_question_start(message: Message, state: FSMContext):
    await state.set_state(QuestionState.waiting_for_question)
    await db.log_section_click("❓ Поставити запитання")
    text = ("✍️ <b>Напишіть своє запитання одним повідомленням.</b>")
    await replace_nav(
        message, state, text=text, reply_markup=get_cancel_keyboard()
    )
    

@router.callback_query(F.data == "cancel_question")
async def cancel_question_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    except Exception:
        pass
    await state.set_state(None)
    await callback.message.answer(text="❌ Скасовано. Оберіть розділ:", reply_markup=main_menu)
    await callback.answer()

@router.message(QuestionState.in_chat)
async def chat_interaction(message: Message, state: FSMContext, bot: Bot):
    if message.text == "🏁 Завершити діалог":
        await perform_close_chat(message, state, bot)
        return
    user_id = message.from_user.id
    topic_id = await db.get_topic_id(user_id)
    if topic_id:
        try:
            await message.copy_to(chat_id=SUPPORT_GROUP_ID, message_thread_id=topic_id)
        except Exception:
            await message.answer("⚠️ Помилка доставки повідомлення адміністратору.")
    else:
        await message.answer("Діалог застарів. Будь ласка, скористайтеся кнопкою 'Поставити запитання' знову.")
        await state.clear()

@router.message(QuestionState.waiting_for_question)
async def forward_question_to_group(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user_data = await state.get_data()
    last_msg_id = user_data.get("last_menu_msg_id")
    if last_msg_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_msg_id)
        except Exception: 
            pass
    topic_id = await db.get_topic_id(user_id)
    if not topic_id:
        try:
            topic_id = await create_new_topic(bot, message, user_id)
        except Exception:
            await message.answer("❌ Помилка створення гілки підтримки. Спробуйте пізніше.")
            return
    try:
        await message.copy_to(chat_id=SUPPORT_GROUP_ID, message_thread_id=topic_id)
    except Exception:
        await message.answer("⚠️ Помилка надсилання запитання адміну. Можливо, гілку було видалено.")
        return
    await message.answer(
        text="✅ <b>Запитання надіслано!</b>\n\nАдміністратор уже отримав його та відповість найближчим часом.",
        reply_markup=main_menu
    )

@router.message(F.chat.id == SUPPORT_GROUP_ID, F.message_thread_id)
async def admin_group_reply_handler(message: Message, bot: Bot, state: FSMContext):
    if message.forum_topic_created or message.forum_topic_edited:
        return
    user_id = await db.get_user_id_by_topic(message.message_thread_id)
    if user_id:
        try:
            user_key = StorageKey(bot_id=bot.id, chat_id=user_id, user_id=user_id)
            current_state = await state.storage.get_state(user_key)
            if current_state == QuestionState.waiting_for_question:
                header_text = "📩 <b>Відповідь від адміністратора:</b>"
            else:
                header_text = "💬 <b>Нове повідомлення від адміністратора:</b>"
            if current_state != QuestionState.in_chat:
                await state.storage.set_state(user_key, QuestionState.in_chat)
                await bot.send_message(
                    chat_id=user_id,
                    text=header_text,
                    reply_markup=get_close_chat_kb()
                )
            await message.copy_to(chat_id=user_id)
        except Exception:
            pass