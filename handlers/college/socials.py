from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import replace_nav

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
async def socials_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("📱 Соцмережі")
    text = (
        "🔗 <b>Ми у соціальних мережах</b>\n\n"
        "Підписуйтесь, щоб бути в курсі всіх новин, подій та цікавинок із життя нашого коледжу! 🤩\n\n"
        "Обирайте зручну платформу нижче 👇"
    )
    await replace_nav(message, state, text=text, reply_markup=get_socials_keyboard())