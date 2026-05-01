from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_days_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Як нас знайти (Карта)", url="https://maps.app.goo.gl/C2hPmjdxBk8Xp7Y4A")],
        # [InlineKeyboardButton(text="🔙 Повернутися до головного", callback_data="events")]
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📅 Дні відкритих дверей")
async def days_info_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("📅 Дні відкритих дверей")
    text = (
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
        "📍 <i>Чекаємо на вас за адресою: м. Одеса, вул. Левітана, 46-а (Наукова/Юннатів).</i>"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_days_keyboard()
    )

# @router.callback_query(F.data == "days")
# async def days_info_handler(callback: CallbackQuery):
#     await log_section_click("📅 Дні відкритих дверей")
#     await callback.message.edit_text(
#         "📅 <b>Дні відкритих дверей у ФКНТІІС ОНТУ</b>\n\n"
#         "Запрошуємо вас особисто познайомитися з коледжем та обрати майбутню професію!\n\n"
#         "<b>Найближчі дати зустрічей:</b>\n"
#         "• 25 квітня — <b>об 11:00</b>\n"
#         "• 9 травня — <b>об 11:00</b>\n"
#         "• 23 травня — <b>об 11:00</b>\n"
#         "• 6 червня — <b>об 11:00</b>\n\n"
#         "<b>На вас чекає:</b>\n"
#         "✅ Екскурсія лабораторіями та аудиторіями.\n"
#         "✅ Знайомство з викладачами та активними студентами.\n"
#         "✅ Детальні консультації щодо вступу та спеціальностей.\n"
#         "✅ Відповіді на запитання про навчання та дозвілля.\n\n"
#         "📍 <i>Чекаємо на вас за адресою: м. Одеса, вул. Левітана, 46-а (Наукова/Юннатів).</i>",
#         reply_markup=get_days_keyboard()
#     )
#     await callback.answer()