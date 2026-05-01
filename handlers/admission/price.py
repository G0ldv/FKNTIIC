from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
import os
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_prices_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити прайс (PDF)", callback_data="download_prices")],
        [InlineKeyboardButton(text="🌐 На сайті", url="https://www.kntiis.od.ua/uk/vartist-navchannya-2025")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

def get_after_prices_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до цін", callback_data="back_to_prices_main")]
    ])
    return keyboard

@router.message(F.text == "💰 Вартість навчання")
async def prices_main_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await log_section_click("💰 Вартість навчання")
    text = (
        "💰 <b>Вартість навчання</b>\n\n"
        "Ознайомтеся з офіційним документом, де вказана вартість навчання для кожної спеціальності.\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:"
    )
    await replace_nav(
        message, state, text=text, reply_markup=get_prices_keyboard()
    )

@router.callback_query(F.data == "download_prices")
async def download_prices_handler(callback: CallbackQuery, state: FSMContext):
    document_path = "assets/files/price_2026.pdf"
    if os.path.exists(document_path):
        data = await state.get_data()
        last_id = data.get("last_menu_msg_id")
        if last_id:
            try:
                await callback.message.bot.delete_message(callback.message.chat.id, last_id)
            except:
                pass
        sent_doc = await callback.message.answer_document(
            document=FSInputFile(document_path),
            caption="💰 <b>Актуальний прайс-лист ФКНТІІС ОНТУ</b>\n\n",
            reply_markup=get_after_prices_download_keyboard()
        )
        await state.update_data(last_menu_msg_id=sent_doc.message_id)
    else:
        await replace_nav(
            callback.message, state,
            text="❌ Файл з цінами тимчасово відсутній. Зверніться до приймальної комісії.",
            reply_markup=get_after_prices_download_keyboard()
        )
    await callback.answer()

@router.callback_query(F.data == "back_to_prices_main")
async def back_to_prices_main(callback: CallbackQuery, state: FSMContext):
    text = (
        "💰 <b>Вартість навчання</b>\n\n"
        "Ознайомтеся з офіційним документом, де вказана вартість навчання для кожної спеціальності.\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:"
    )
    await replace_nav(
        callback.message, state, text=text, reply_markup=get_prices_keyboard()
    )
    await callback.answer()