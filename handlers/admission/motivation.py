from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

router = Router()

def get_motivation_examples_keyboard():
    builder = InlineKeyboardBuilder()
    specialties = [
        ("📊 D5 Маркетинг", "D5"),
        ("🛒 D7 Торгівля", "D7"),
        ("🌱 E2 Екологія", "E2"),
        ("⚡ G3 Електрична інженерія", "G3"),
        ("🧪 G1 Хімічні технології та інженерія", "G1"),
        ("📡 G5 Електроніка, електронні комунікації, приладобудування та радіотехніка", "G5"),
        ("💻 G5(K) Комп’ютерні технології та електронні комунікації", "G5(K)"),
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

def get_after_file_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до списку", callback_data="motivation_examples_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "motivation_letter")
async def motivation_main(callback: CallbackQuery):
    await callback.message.delete() 
    text = (
        "<b>📝 Мотиваційний лист</b>\n\n"
        "Оберіть потрібний розділ. Ви можете ознайомитися з вимогами або завантажити готовий приклад для своєї спеціальності."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Вимоги до оформлення", callback_data="ml_requirements")],
        [InlineKeyboardButton(text="📂 Приклади за спеціальностями", callback_data="motivation_examples_menu")],
        [InlineKeyboardButton(text="⬅️ Повернутися до документів", callback_data="docs")]
    ])
    await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "ml_requirements")
async def show_requirements(callback: CallbackQuery):
    await callback.message.delete()
    text = (
        "<b>📋 Основні вимоги до листа:</b>\n\n"
        "• Обов'язкова наявність 'шапки' (ПІБ, адреса, контакти).\n"
        "• Зазначення місця попереднього навчання.\n"
        "• Обґрунтування вибору спеціальності.\n"
        "• Опис особистих якостей та прагнень.\n"
        "• Відсутність помилок та офіційний стиль."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити інструкцію (PDF)", callback_data="send_req_pdf")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="motivation_letter")]
    ])
    await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "motivation_examples_menu")
async def list_examples(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Оберіть спеціальність, щоб отримати відповідний приклад у форматі PDF:",
        reply_markup=get_motivation_examples_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("get_ml_") | (F.data == "send_req_pdf"))
async def send_motivation_file(callback: CallbackQuery):
    await callback.answer("Надсилаю документ...")
    await callback.message.delete()
    
    if callback.data == "send_req_pdf":
        file_path = "assets/files/requirements.pdf"
        caption = "📋 <b>Вимоги до написання мотиваційного листа</b>"
    else:
        code = callback.data.split("_")[2]
        file_path = f"assets/files/ml_{code}.pdf"
        caption = f"📄 <b>Приклад листа для спеціальності {code}</b>"

    if os.path.exists(file_path):
        await callback.message.answer_document(
            document=FSInputFile(file_path),
            caption=caption,
            reply_markup=get_after_file_download_keyboard(),
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            "❌ Файл тимчасово відсутній на сервері.",
            reply_markup=get_after_file_download_keyboard()
        )
    await callback.answer()