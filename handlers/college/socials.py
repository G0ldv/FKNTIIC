from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from keyboards.main_menu import main_menu

router = Router()

def get_socials_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📸 Instagram", url="https://www.instagram.com/fkntiis/"),
            InlineKeyboardButton(text="🎬 TikTok", url="https://www.tiktok.com/@fkntiis?is_from_webapp=1&sender_device=pc")
        ],
        [
            InlineKeyboardButton(text="📱 Telegram канал", url="https://t.me/fkntiis"), 
            InlineKeyboardButton(text="🌐 Офіційний сайт", url="https://www.kntiis.od.ua/uk")
        ],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📱 Соцмережі")
async def socials_handler(message: Message):
    temp_msg = await message.answer("Відкриваю соцмережі...", reply_markup=ReplyKeyboardRemove())
    await temp_msg.delete()
    try:
        await message.chat.delete_message(message.message_id - 1)
    except:
        pass
    text = (
        "🔗 <b>Ми у соціальних мережах</b>\n\n"
        "Підписуйтесь, щоб бути в курсі всіх новин, подій та цікавинок із життя нашого коледжу! 🤩\n\n"
        "Обирайте зручну платформу нижче 👇"
    )
    await message.answer(
        text,
        reply_markup=get_socials_keyboard()
    )
    await message.delete()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Ви повернулися до головного меню:",
        reply_markup=main_menu
    )
    await callback.answer()