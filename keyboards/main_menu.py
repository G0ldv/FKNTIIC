from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Вступнику")],
        [KeyboardButton(text="📄 Спеціальності"), KeyboardButton(text="💰 Вартість навчання")],
        [KeyboardButton(text="📅 Дні відкритих дверей"), KeyboardButton(text="🏫 Про коледж")],
        [KeyboardButton(text="📍 Локація та контакти"), KeyboardButton(text="📱 Соцмережі")],
        [KeyboardButton(text="❓ Поставити запитання")]
    ],
    resize_keyboard=True, is_persistent=True, one_time_keyboard=True
)