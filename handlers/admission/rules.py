from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import os
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_rules_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити документ (PDF)", callback_data="dl_adm_rules")],
        [InlineKeyboardButton(text="🌐 На сайті", url="https://www.kntiis.od.ua/uk/pravila-priyomu-do-kntiis-ontu-v-2026-roci")],
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

def get_after_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до правил прийому", callback_data="rules")]
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
    await replace_nav(
        callback.message, state, text=text, reply_markup=get_rules_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "dl_adm_rules")
async def download_rules_handler(callback: CallbackQuery, state: FSMContext):
    document_path = "assets/files/Правила прийому 2026.pdf"
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