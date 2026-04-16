from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

router = Router()

def get_specialties_keyboard():
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
        builder.button(text=name, callback_data=f"example_{code}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="motivation_letter"))
    return builder.as_markup()

@router.callback_query(F.data == "motivation_letter")
async def motivation_main(callback: CallbackQuery):
    text = (
        "<b>📝 Мотиваційний лист</b>\n\n"
        "Це документ, у якому ви обґрунтовуєте своє бажання навчатися на конкретній спеціальності. "
        "Він подається в електронному кабінеті при подачі заяви.\n\n"
        "💡 <b>Що ви знайдете тут:</b>\n"
        "• Загальні вимоги до оформлення та структури;\n"
        "• Приклади написання для кожної спеціальності нашого коледжу."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Вимоги до листа (PDF)", callback_data="motivation_req_file")],
        [InlineKeyboardButton(text="📂 Приклади за спеціальностями", callback_data="motivation_examples")],
        [InlineKeyboardButton(text="⬅️ Назад до документів", callback_data="docs")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "motivation_req_file")
async def send_requirements(callback: CallbackQuery):
    file_path = "assets/files/requirements.pdf"
    if os.path.exists(file_path):
        await callback.message.answer_document(
            FSInputFile(file_path),
            caption="📋 <b>Вимоги до написання мотиваційного листа</b>",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("⚠️ Файл з вимогами наразі відсутній.")
    await callback.answer()

@router.callback_query(F.data == "motivation_examples")
async def list_examples(callback: CallbackQuery):
    await callback.message.edit_text(
        "Оберіть спеціальність, щоб завантажити приклад мотиваційного листа:",
        reply_markup=get_specialties_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("example_"))
async def send_example(callback: CallbackQuery):
    spec_code = callback.data.split("_")[1]
    file_path = f"assets/files/ml_{spec_code}.pdf"
    if os.path.exists(file_path):
        await callback.message.answer_document(
            FSInputFile(file_path),
            caption=f"📄 <b>Приклад листа для спеціальності {spec_code}</b>",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(f"⚠️ Приклад для спеціальності {spec_code} ще не завантажено.")
    await callback.answer()