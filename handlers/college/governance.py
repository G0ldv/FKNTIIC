from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import edit_nav

router = Router()

def get_governance_more_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Детальніше на сайті", url="https://www.kntiis.od.ua/uk/studentske-samovryaduvannya")],
        [InlineKeyboardButton(text="🔙 Назад до вибору", callback_data="open_about_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "governance_more")
async def governance_handler(callback: CallbackQuery, state: FSMContext):
    await log_section_click("🤝 Студентське самоврядування")
    text = (
        "🤝 <b>Студентське самоврядування: твій голос має значення!</b>\n\n"
        "У нашому коледжі студенти — це не просто слухачі, а реальна сила. "
        "<b>Рада студентського самоврядування</b> — це команда активістів, які роблять життя в коледжі яскравим.\n\n"
        "⚡ <b>Чим займається самоврядування?</b>\n"
        "• Організація крутих івентів: КВК, Дні відкритих дверей, спортивні змагання.\n"
        "• Захист прав студентів та допомога в адаптації першокурсників.\n"
        "• Благодійні ярмарки та волонтерські проєкти.\n\n"
        "Хочеш розвивати лідерські якості? Тобі точно до нас! Твоя ідея може стати наступним великим проєктом коледжу."
    )
    await edit_nav(callback.message, state, text=text, reply_markup=get_governance_more_keyboard())
    await callback.answer()