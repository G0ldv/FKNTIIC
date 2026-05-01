from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_contacts_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Відкрити Google Maps", url="https://maps.app.goo.gl/C2hPmjdxBk8Xp7Y4A")],
        [InlineKeyboardButton(text="💬 Telegram", url="https://t.me/+380671030577")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📍 Локація та контакти")
async def contacts_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("📍 Локація та контакти")
    text = (
        "📍 <b>Наші контакти та розташування</b>\n\n"
        "🏢 <b>Адреса:</b>\n"
        "м. Одеса, вул. Левітана, 46-а\n"
        "(Наукова/Юннатів)\n\n"
        "🕒 <b>Загальний графік роботи:</b>\n"
        "<code>Пн–Чт: 09:00 – 16:00</code>\n"
        "<code>Пт:    09:00 – 15:00</code>\n"
        "<i>Сб–Нд: Вихідні</i>\n\n"
        "📞 <b>Приймальна комісія:</b>\n"
        "+380671030577 (Telegram, Viber)\n"
        "📧 <i>prijmalnakomisia2@gmail.com</i>\n\n"
        "👤 <b>Приймальна директора:</b>\n"
        "+380487492932\n"
        "📧 <i>kntiis.od@gmail.com</i>\n\n"
        "З будь-яких питань звертайтеся у робочий час! 😊"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_contacts_keyboard()
    )