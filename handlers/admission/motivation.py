from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from database import log_section_click
from utils.navigation import replace_nav, edit_nav

router = Router()

def get_motivation_letter_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Вимоги до оформлення", callback_data="ml_requirements")],
        [InlineKeyboardButton(text="📂 Приклади за спеціальностями", callback_data="motivation_examples_menu")],
        [InlineKeyboardButton(text="⬅️ Повернутися до документів", callback_data="docs")]
    ])
    return keyboard

def get_motivation_pdf_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити інструкцію (PDF)", callback_data="send_req_pdf")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="motivation_letter")]
    ])
    return keyboard

def get_motivation_letter_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до меню", callback_data="motivation_letter")]
    ])
    return keyboard

def get_motivation_example_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до списку", callback_data="motivation_examples_menu")]
    ])
    return keyboard

def get_motivation_examples_keyboard():
    builder = InlineKeyboardBuilder()
    specialties = [
        ("📊 D5 Маркетинг", "D5"),
        ("🛒 D7 Торгівля", "D7"),
        ("🌱 E2 Екологія", "E2"),
        ("⚡ G3 Електрична інженерія", "G3"),
        ("🧪 G1 Хімічні технології та інженерія", "G1"),
        ("📡 G5 Електроніка, електронні комунікації, приладобудування та радіотехніка", "G5"),
        ("💻 G5(K) Комп’ютерні технології та електронні комунікації", "G5_K"),
        ("🤖 G7 Автоматизація, комп`ютерно-інтегровані технології та робототехніка", "G7"),
        ("🍞 G13 Харчові технології", "G13"),
        ("⛏️ G16 Гірництво та нафтогазові технології", "G16"),
        ("🍽️ J2 Готельно-ресторанна справа та кейтеринг", "J2"),
        ("🌍 J3 Туризм та рекреація", "J3")
    ]
    for name, code in specialties:
        builder.button(text=name, callback_data=f"get_ml_{code}")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Назад до меню", callback_data="motivation_letter"))
    return builder.as_markup()

@router.callback_query(F.data == "motivation_letter")
async def motivation_main(callback: CallbackQuery, state: FSMContext):
    await log_section_click("📄 Мотиваційний лист") 
    text = (
        "<b>📝 Мотиваційний лист</b>\n\n"
        "Оберіть потрібний розділ. Ви можете ознайомитися з вимогами або завантажити готовий приклад для своєї спеціальності."
    )
    await edit_nav(
        callback.message, state, text=text, reply_markup=get_motivation_letter_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "ml_requirements")
async def show_requirements(callback: CallbackQuery, state: FSMContext):
    text = (
        "<b>📋 Основні вимоги до листа:</b>\n\n"
        "• Обов'язкова наявність 'шапки' (ПІБ, адреса, контакти).\n"
        "• Зазначення місця попереднього навчання.\n"
        "• Обґрунтування вибору спеціальності.\n"
        "• Опис особистих якостей та прагнень.\n"
        "• Відсутність помилок та офіційний стиль."
    )
    await edit_nav(
        callback.message, state, text=text, reply_markup=get_motivation_pdf_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "motivation_examples_menu")
async def list_examples(callback: CallbackQuery, state: FSMContext):
    text = (
        "Оберіть спеціальність, щоб отримати відповідний приклад у форматі PDF:"
    )
    await edit_nav(
        callback.message, state, text=text, reply_markup=get_motivation_examples_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("get_ml_") | (F.data == "send_req_pdf"))
async def send_motivation_file(callback: CallbackQuery, state: FSMContext):
    if callback.data == "send_req_pdf":
        file_path = "assets/files/requirements.pdf"
        caption = "📋 <b>Вимоги до написання мотиваційного листа</b>"
        kb = get_motivation_letter_menu_keyboard() 
    else:
        code = callback.data.split("_")[2]
        file_path = f"assets/files/ml_{code}.pdf"
        caption = f"📄 <b>Приклад листа для спеціальності {code}</b>"
        kb = get_motivation_example_menu_keyboard()
    if os.path.exists(file_path):
        sent = await callback.message.answer_document(
            document=FSInputFile(file_path),
            caption=caption,
            reply_markup=kb
        )
    else:
        await replace_nav(
            callback.message, state,
            text="❌ Файл тимчасово відсутній на сервері.",
            reply_markup=kb
        )
    await callback.answer()