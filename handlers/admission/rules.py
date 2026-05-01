from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import os
from database import log_section_click
from utils.navigation import replace_nav, edit_nav

router = Router()

def get_rules_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити документ (PDF)", callback_data="download_rules")],
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

def get_after_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "rules")
async def rules_main_handler(callback: CallbackQuery, state: FSMContext):
    await log_section_click("📘 Правила вступу")
    text = (
        "📘 <b>Правила прийому до коледжу</b>\n\n"
        "У цьому документі ви знайдете детальну інформацію про:\n"
        "• Терміни подачі заяв\n"
        "• Перелік вступних випробувань\n"
        "• Порядок зарахування\n\n"
        "Натисніть кнопку нижче, щоб отримати файл:"
    )
    await edit_nav(
        callback.message, state, text=text, reply_markup=get_rules_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "download_rules")
async def download_rules_handler(callback: CallbackQuery, state: FSMContext):
    document_path = "assets/files/rules.pdf"
    if os.path.exists(document_path):
        await callback.answer("Надсилаю файл...")
        sent_doc = await callback.message.answer_document(
            document=FSInputFile(document_path),
            caption="📘 <b>Правила прийому 2026</b>\n\nВи можете повернутися назад за допомогою кнопки:",
            reply_markup=get_after_download_keyboard()
        )
        await state.update_data(last_menu_msg_id=sent_doc.message_id)
    else:
        await replace_nav(
            callback.message, state,
            text="❌ Файл з правилами тимчасово відсутній. Зверніться до Приймальної комісії.",
            reply_markup=get_after_download_keyboard()
        )
        await callback.answer()