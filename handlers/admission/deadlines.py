from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from database import log_section_click

router = Router()

def get_deadlines_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "deadlines")
async def show_deadlines(callback: CallbackQuery):
    await callback.message.delete()
    await log_section_click("📅 Терміни вступу")
    photo = FSInputFile("assets/images/admission_dates.jpg")
    caption_text = (
        "📅 <b>Терміни вступної кампанії 2026</b>\n\n"
        "Щоб вчасно подати документи, зверніть увагу на ключові дати:\n\n"
        "• <b>Реєстрація кабінетів:</b> з 25.06 (9 кл) / 01.07 (11 кл)\n"
        "• <b>Подання заяв:</b> з 01.07 по 20.07 (бюджет) / до 15.10 (контракт)\n\n"
        "Детальна таблиця для 9, 11 класів та ПТУ наведена на зображенні 👆"
    )
    await callback.message.answer_photo(
        photo=photo,
        caption=caption_text,
        reply_markup=get_deadlines_keyboard()
    )
    await callback.answer()