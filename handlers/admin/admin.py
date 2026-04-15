from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import io
from aiogram.types import BufferedInputFile
from database import get_all_users_full, get_users_count, get_all_users

router = Router()
ADMIN_IDS = [1779431249]

class BroadcastStates(StatesGroup):
    waiting_for_content = State()
    confirm_broadcast = State()

def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Так, надсилати", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="confirm_no")]
    ])

@router.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def admin_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Створити розсилку", callback_data="start_broadcast")],
        [InlineKeyboardButton(text="📄 Завантажити список", callback_data="download_users")]
    ])
    await message.answer("🛠 <b>Панель керування</b>", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "admin_stats")
async def stats(callback: CallbackQuery):
    count = await get_users_count()
    await callback.message.answer(f"👥 Всього користувачів: {count}")
    await callback.answer()

@router.callback_query(F.data == "start_broadcast")
async def broadcast_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📥 <b>Надішліть або перешліть</b> повідомлення для розсилки.\n"
        "Це може бути текст, фото, відео або документ.",
        parse_mode="HTML"
    )
    await state.set_state(BroadcastStates.waiting_for_content)
    await callback.answer()

@router.message(BroadcastStates.waiting_for_content)
async def ask_confirm(message: Message, state: FSMContext):
    await state.update_data(msg_id=message.message_id, chat_id=message.chat.id)
    await message.reply("☝️ Ви точно хочете надіслати ЦЕ повідомлення всім користувачам?", reply_markup=confirm_kb())
    await state.set_state(BroadcastStates.confirm_broadcast)

@router.callback_query(F.data == "confirm_yes", BroadcastStates.confirm_broadcast)
async def send_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    users = await get_all_users()
    count = 0
    
    await callback.message.edit_text("🚀 Розсилка розпочата...")
    
    for user_id in users:
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=data['chat_id'], message_id=data['msg_id'])
            count += 1
        except Exception:
            continue
            
    await callback.message.answer(f"✅ Успішно надіслано <b>{count}</b> користувачам.", parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data == "confirm_no")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Розсилку скасовано.")

@router.callback_query(F.data == "download_users")
async def send_users_list(callback: CallbackQuery):
    users = await get_all_users_full()
    
    if not users:
        await callback.answer("База даних поки що порожня.")
        return

    report = "СПИСОК КОРИСТУВАЧІВ БОТА\n"
    report += "="*40 + "\n"
    for u in users:
        username = f"@{u[2]}" if u[2] else "немає"
        phone = u[3] if u[3] else "не вказано"
        report += f"👤 {u[1]} | ID: {u[0]} | Юзер: {username} | Тел: {phone}\n"

    file_bytes = io.BytesIO(report.encode('utf-8'))
    file_for_tg = BufferedInputFile(file_bytes.getvalue(), filename="users_list.txt")

    await callback.message.answer_document(
        document=file_for_tg, 
        caption="📂 Ось актуальний список усіх користувачів."
    )
    await callback.answer()