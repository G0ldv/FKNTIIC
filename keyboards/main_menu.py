from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Вступ")],
        [KeyboardButton(text="📄 Спеціальності"), KeyboardButton(text="💰 Вартість навчання")],
        [KeyboardButton(text="📅 Заходи"), KeyboardButton(text="🏫 Про коледж")],
        [KeyboardButton(text="📍 Локація та контакти"), KeyboardButton(text="📱 Соцмережі")],
        [KeyboardButton(text="❓ Поставити запитання")]
    ],
    resize_keyboard=True
)

remove_menu = ReplyKeyboardRemove()

back_to_menu_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад у меню")]
    ],
    resize_keyboard=True
)