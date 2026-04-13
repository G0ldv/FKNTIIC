import re
from aiogram import Router, F
from aiogram.types import Message

router = Router()

ADMIN_CHAT_ID = 1779431249 

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