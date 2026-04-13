from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def get_prep_courses_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записатися на курси", callback_data="enroll_prep")],
        [InlineKeyboardButton(text="🔙 Повернутися до вступу", callback_data="admission_menu")],
    ])
    return keyboard

def get_enroll_prep_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Заповнити форму", url="https://docs.google.com/forms/d/e/1FAIpQLScD-AOugswgwQi3Ob0GeQHcUn9K-5Ir2BZ590DLGD8GuNQ92Q/viewform?usp=header")],
        [InlineKeyboardButton(text="🔙 Повернутись до підготовчих курсів", callback_data="prep_courses")],
    ])
    return keyboard

@router.callback_query(F.data == "prep_courses")
async def prep_courses_handler(callback: CallbackQuery):
    text = (
        "🎓 <b>Твій тест-драйв студентського життя!</b>\n\n"
        "Запрошуємо учнів 9-х класів на підготовчі курси. Це не просто навчання — це можливість відчути себе частиною нашої родини ще до вступу! ✨\n\n"
        "🚀 <b>Що на тебе чекає:</b>\n"
        "• <b>Справжні пари:</b> Забудь про 40-хвилинні уроки. У нас заняття тривають <b>80 хвилин</b> — як у справжньому університеті.\n"
        "• <b>Знайомство:</b> Ти зустрінеш майбутніх однокурсників. На курсах зазвичай формуються найміцніші дружні компанії!\n"
        "• <b>Викладачі:</b> Ти познайомишся з тими, хто буде навчати тебе в майбутньому.\n\n"
        "📅 <b>Період:</b> з 15 червня по 10 липня\n"
        "📚 <b>Предмети:</b> Українська мова та Математика\n"
        "🌍 <b>Формат:</b> Обирай сам — Офлайн (у коледжі) чи Онлайн\n\n"
        "💰 <b>Вартість:</b> <i>1950 грн.</i>\n\n"
        "🤝 <b>Це твій шанс знайти перших друзів у коледжі!</b>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_prep_courses_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "enroll_prep")
async def enroll_prep_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "📝 <b>Запис на курси</b>\n\n"
        "Для реєстрації, будь ласка, зверніться до приймальної комісії або заповніть форму нижче.\n\n"
        "📞 Контакти: +380671030577 (Telegram, Viber)",
        reply_markup=get_enroll_prep_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()