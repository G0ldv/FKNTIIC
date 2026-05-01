from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import io
from aiogram.types import BufferedInputFile
from utils.navigation import replace_nav
from database import get_all_users_full, get_users_count, get_all_users, get_sections_stats

router = Router()
ADMIN_IDS = [1779431249]

class BroadcastStates(StatesGroup):
    waiting_for_content = State()
    confirm_broadcast = State()

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Створити розсилку", callback_data="start_broadcast")],
        [InlineKeyboardButton(text="📄 Завантажити список", callback_data="download_users")]
    ])

def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Так, надсилати", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="confirm_no")]
    ])

@router.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(None)
    await replace_nav(
        message, state, 
        text="🛠 <b>Панель керування</b>", 
        reply_markup=admin_kb(),save_history=True 
    )

@router.callback_query(F.data == "admin_stats")
async def stats(callback: CallbackQuery, state: FSMContext):
    count = await get_users_count()
    sections = await get_sections_stats()
    msg = f"👥 <b>Загальна кількість користувачів:</b> {count}\n\n"
    if sections:
        msg += "📊 <b>Популярність розділів:</b>\n"
        msg += "━━━━━━━━━━━━━━━━━━\n"
        for i, row in enumerate(sections, 1):
            msg += f"{i}. {row[0]}: <b>{row[1]}</b>\n"
    else:
        msg += "ℹ️ Дані про активність поки що відсутні."
    await replace_nav(callback.message, state, text=msg, reply_markup=admin_kb())
    await callback.answer()

@router.callback_query(F.data == "start_broadcast")
async def broadcast_request(callback: CallbackQuery, state: FSMContext):
    await replace_nav(
        callback.message, state, 
        text="📥 <b>Надішліть повідомлення</b> для розсилки.\nЦе може бути будь-який тип контенту."
    )
    await state.set_state(BroadcastStates.waiting_for_content)
    await callback.answer()

@router.message(BroadcastStates.waiting_for_content)
async def ask_confirm(message: Message, state: FSMContext):
    await state.update_data(msg_id=message.message_id, chat_id=message.chat.id)
    await message.reply("☝️ Ви впевнені?", reply_markup=confirm_kb())
    await state.set_state(BroadcastStates.confirm_broadcast)

@router.callback_query(F.data == "confirm_yes", BroadcastStates.confirm_broadcast)
async def send_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    users = await get_all_users()
    count = 0
    await callback.message.delete()
    status_msg = await callback.message.answer("🚀 Розсилка розпочата...")
    for user_id in users:
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=data['chat_id'], message_id=data['msg_id'])
            count += 1
        except Exception:
            continue
    await status_msg.edit_text(f"✅ Успішно надіслано <b>{count}</b> користувачам.")
    await state.set_state(None)
    await callback.answer()

@router.callback_query(F.data == "download_users")
async def send_users_list(callback: CallbackQuery, state: FSMContext):
    users = await get_all_users_full()
    if not users:
        await callback.answer("База даних порожня.", show_alert=True)
        return
    report = "СПИСОК КОРИСТУВАЧІВ\n" + "="*25 + "\n"
    for u in users:
        report += f"👤 {u[1]} | ID: {u[0]} | Юзер: @{u[2] if u[2] else '—'}\n"
    file_bytes = io.BytesIO(report.encode('utf-8'))
    file_for_tg = BufferedInputFile(file_bytes.getvalue(), filename="users.txt")
    await callback.message.answer_document(document=file_for_tg, caption="📂 Список користувачів")
    await callback.answer()