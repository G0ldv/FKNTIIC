import re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

ADMIN_CHAT_ID = 1779431249 

class QuestionState(StatesGroup):
    waiting_for_question = State()

@router.message(F.text == "❓ Поставити запитання")
async def ask_question_start(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(
        "✍️ Напишіть своє запитання одним повідомленням.\n\n"
        "Якщо передумали, напишіть <b>Скасувати</b>.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove() 
    )
    await state.set_state(QuestionState.waiting_for_question)

@router.message(QuestionState.waiting_for_question)
async def forward_question_to_admin(message: Message, state: FSMContext):
    from keyboards.main_menu import main_menu 
    if message.text and message.text.lower() == "скасувати":
        await message.answer("❌ Дію скасовано.", reply_markup=main_menu)
        await state.clear()
        return
    if not message.text:
        await message.answer("Будь ласка, надішліть питання текстом або напишіть <b>Скасувати</b>.", parse_mode="HTML")
        return
    username = f"@{message.from_user.username}" if message.from_user.username else "Без юзернейму"
    admin_text = (
        f"❓ <b>Нове запитання!</b>\n"
        f"👤 Від: {username} (ID: {message.from_user.id})\n\n"
        f"📝 <b>Текст:</b> {message.text}"
    )
    await message.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_text,
        parse_mode="HTML"
    )
    await message.answer(
        "✅ Ваше запитання успішно надіслано! Очікуйте на відповідь у цьому чаті.",
        reply_markup=main_menu
    )
    await state.clear()


@router.message(F.chat.id == ADMIN_CHAT_ID, F.reply_to_message)
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
                text="📩 <b>Відповідь від приймальної комісії:</b>",
                parse_mode="HTML"
            )
            await message.copy_to(chat_id=user_id)
            await message.reply("✅ Відповідь успішно надіслано абітурієнту!")
        except Exception as e:
            await message.reply(f"❌ Помилка надсилання: користувач заблокував бота або сталася помилка.\n{e}")