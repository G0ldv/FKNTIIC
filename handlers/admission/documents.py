from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import log_section_click

router = Router()

def get_docs_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Після 9 класу", callback_data="docs_9cl")],
        [InlineKeyboardButton(text="🏫 Після 11 класу", callback_data="docs_11cl")],
        [InlineKeyboardButton(text="🛠 На базі диплома ПТУ", callback_data="docs_ptu")],
        [InlineKeyboardButton(text="🎗️ Пільгові категорії", callback_data="docs_benefits")],
        # [InlineKeyboardButton(text="📄 Мотиваційний лист", callback_data="motivation_letter")],
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

def get_back_to_docs_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до вибору категорій", callback_data="docs")]
    ])
    return keyboard

@router.callback_query(F.data == "docs")
async def docs_main_handler(callback: CallbackQuery):
    await log_section_click("📑 Необхідні документи")
    await callback.message.edit_text(
        "📑 <b>Перелік документів для вступу</b>\n\n"
        "Оберіть вашу категорію, щоб побачити повний список необхідних документів:",
        reply_markup=get_docs_main_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("docs_"))
async def docs_detail_handler(callback: CallbackQuery):
    data = callback.data
    text = ""
    common_items = (
        "• Паспорт (ID-картка + витяг про реєстрацію)\n"
        "• ІПН (ідентифікаційний код)\n"
        "• 4 кольорові фото (3х4)\n"
        "• Резерв+ pdf-файл (для хлопців)"
        # "• Мотиваційний лист (подається в ел. кабінеті)"
    )
    parent_docs = (
        "\n\n👤 <b>Для неповнолітніх (документи одного з батьків):</b>\n"
        "<i>Необхідні для укладання договору про навчання:</i>\n"
        "• Паспорт одного з батьків (якщо ID-картка — також потрібен витяг)\n"
        "• ІПН одного з батьків"
    )    
    if data == "docs_9cl":
        text = (
            "🎓 <b>Для вступників на базі 9 класів:</b>\n\n"
            f"{common_items}\n"
            "• Свідоцтво про базову середню освіту\n"
            "• Додаток до свідоцтва (з оцінками)\n"
            "• Свідоцтво про народження (якщо немає паспорта)\n"
            "• Медична довідка (форма 086-о)\n"
            f"{parent_docs}"   
        )
    elif data == "docs_11cl":
        text = (
            "🏫 <b>Для вступників на базі 11 класів:</b>\n\n"
            f"{common_items}\n"
            "• Атестат про повну загальну середню освіту\n"
            "• Додаток до атестату\n"
            "• Сертифікат НМТ або ЗНО (за наявності)\n"
            f"{parent_docs}"
        )
    elif data == "docs_ptu":
        text = (
            "🛠 <b>На базі диплома ПТУ:</b>\n\n"
            f"{common_items}\n"
            "• Диплом кваліфікованого робітника\n"
            "• Додаток до диплому\n"
            "• Сертифікат НМТ/ЗНО (за наявності)\n\n"
            "<i>*Можливий вступ на 2-й або 3-й курс.</i>\n"
            f"{parent_docs}"
        )
    elif data == "docs_benefits":
        text = (
            "🎗️ <b>Пільгові категорії:</b>\n\n"
            "Окрім основного списку, необхідно надати:\n"
            "• Документи, що підтверджують пільгу (оригінали та копії)\n"
            "• Для ВПО: довідка про взяття на облік\n"
            "• Для УБД/дітей УБД: посвідчення\n\n"
            "<i>Зверніться до приймальної комісії для перевірки пільги в ЄДЕБО.</i>"
        )
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_docs_keyboard()
    )
    await callback.answer()