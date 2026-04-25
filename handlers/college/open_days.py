from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import log_section_click

router = Router()

def get_days_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Як нас знайти (Карта)", url="https://maps.app.goo.gl/C2hPmjdxBk8Xp7Y4A")],
        [InlineKeyboardButton(text="🔙 Повернутися до меню заходів", callback_data="events")]
    ])
    return keyboard

@router.callback_query(F.data == "days")
async def days_info_handler(callback: CallbackQuery):
    await log_section_click("📅 Дні відкритих дверей")
    await callback.message.edit_text(
        "📅 <b>Дні відкритих дверей у ФКНТІІС ОНТУ</b>\n\n"
        "Запрошуємо вас особисто познайомитися з коледжем та обрати майбутню професію!\n\n"
        "<b>Найближчі дати зустрічей:</b>\n"
        "• 25 квітня — <b>об 11:00</b>\n"
        "• 9 травня — <b>об 11:00</b>\n"
        "• 23 травня — <b>об 11:00</b>\n"
        "• 6 червня — <b>об 11:00</b>\n\n"
        "<b>На вас чекає:</b>\n"
        "✅ Екскурсія лабораторіями та аудиторіями.\n"
        "✅ Знайомство з викладачами та активними студентами.\n"
        "✅ Детальні консультації щодо вступу та спеціальностей.\n"
        "✅ Відповіді на запитання про навчання та дозвілля.\n\n"
        "📍 <i>Чекаємо на вас за адресою: м. Одеса, вул. Левітана, 46-а (Наукова/Юннатів).</i>",
        reply_markup=get_days_keyboard()
    )
    await callback.answer()