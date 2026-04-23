from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def get_rules_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити документ (PDF)", callback_data="download_rules")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admission_menu")]
    ])
    return keyboard

def get_after_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до меню вступу", callback_data="admission_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "rules")
async def rules_main_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "📘 <b>Правила прийому до коледжу</b>\n\n"
        "У цьому документі ви знайдете детальну інформацію про:\n"
        "• Терміни подачі заяв\n"
        "• Перелік вступних випробувань\n"
        "• Порядок зарахування\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:",
        reply_markup=get_rules_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "download_rules")
async def download_rules_handler(callback: CallbackQuery):
    await callback.answer("Надсилаю файл...")
    await callback.message.delete()
    document = FSInputFile("assets/files/rules.pdf")
    try:
        await callback.message.answer_document(
        document=document,
        caption="📘 <b>Правила прийому 2026</b>\n\nВи можете повернутися назад за допомогою кнопки:",
        reply_markup=get_after_download_keyboard()
        )
    except Exception as e:
        await callback.message.answer(f"❌ Інформація оновлюється: {e}")
    await callback.answer()    
