from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu, remove_menu

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
    await message.delete()
    temp_msg = await message.answer("Завантажую розділ цін...", reply_markup=remove_menu)
    await temp_msg.delete()
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except:
            pass
    await message.answer(
        "💰 <b>Вартість навчання</b>\n\n"
        "Ознайомтеся з офіційним документом, де вказана вартість навчання для кожної спеціальності.\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:",
        reply_markup=get_prices_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "download_prices")
async def download_prices_handler(callback: CallbackQuery):
    await callback.answer("Надсилаю документ...")
    await callback.message.delete()
    document = FSInputFile("assets/files/price_2026.pdf")
    try:
        await callback.message.answer_document(
            document=document,
            caption="💰 <b>Актуальний прайс-лист ФКНТІІС ОНТУ</b>\n\n",
            reply_markup=get_after_prices_download_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        await callback.message.answer(
            f"❌ Не вдалося відправити файл. Технічна помилка: {e}"
        )
    await callback.answer()

@router.callback_query(F.data == "back_to_prices_main")
async def back_to_prices_main(callback: CallbackQuery):
    await callback.message.delete() 
    await callback.message.answer(
        "💰 <b>Вартість навчання</b>\n\n"
        "Ознайомтеся з офіційним документом, де вказана вартість навчання для кожної спеціальності.\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:",
        reply_markup=get_prices_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    sent_message = await callback.message.answer(
        "Ви повернулися в головне меню. Оберіть розділ: 👇",
        reply_markup=main_menu
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer()