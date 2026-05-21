from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
import os
from database import log_section_click
from utils.navigation import replace_nav

router = Router()

def get_exams_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Положення про співбесіду", callback_data="exams_rules")],
        [InlineKeyboardButton(text="📚 Програма співбесіди", callback_data="exams_program")],
        # [InlineKeyboardButton(text="📅 Розклад співбесід", callback_data="exams_schedule")], 
        [InlineKeyboardButton(text="🔙 Повернутися в розділ вступника", callback_data="admission_menu")]
    ])
    return keyboard

def get_download_keyboard(file_type):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Завантажити файл", callback_data=f"dl_exam_{file_type}")],
        [InlineKeyboardButton(text="🔙 Назад до меню випробувань", callback_data="entrance_exams")]
    ])
    return keyboard

def get_after_exams_download_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Повернутися до випробувань", callback_data="entrance_exams")]
    ])
    return keyboard

@router.callback_query(F.data == "entrance_exams")
async def entrance_exams_handler(callback: CallbackQuery, state: FSMContext):
    await log_section_click("📝 Вступні випробування")
    text = (
        "<b>📝 Вступні випробування (Співбесіда)</b>\n\n"
        "Індивідуальна усна співбесіда — це форма вступного випробування, яка передбачає "
        "оцінювання знань та навичок вступника.\n\n"
        "🔹 <b>З чого складається:</b> цього року випробування проводиться у формі відповідей на питання "
        "виключно з <b>української мови</b>. Вам буде задано щонайменше три питання з програми.\n\n"
        "🔹 <b>Формат проведення:</b> співбесіда може проходити як <b>очно</b>, так і <b>дистанційно</b>. \n\n"
        "🔹 <b>Час:</b> на спілкування з кожним вступником відводиться орієнтовно 15 хвилин.\n\n"
        "Нижче ви можете завантажити офіційну програму та положення:"
    )
    await replace_nav(callback.message, state, text=text, reply_markup=get_exams_keyboard())

@router.callback_query(F.data == "exams_rules")
async def exams_rules_info(callback: CallbackQuery, state: FSMContext):
    text = (
        "📄 <b>Положення про співбесіду</b>\n\n"
        "У цьому документі ви знайдете офіційні правила: як створюється комісія, "
        "як проходить процедура та як виставляються бали. "
        "Важливо: апеляція на результати не передбачена."
    )
    await replace_nav(callback.message, state, text=text, reply_markup=get_download_keyboard("rules"))

@router.callback_query(F.data == "exams_program")
async def exams_program_info(callback: CallbackQuery, state: FSMContext):
    text = (
        "📚 <b>Програма співбесіди (Українська мова)</b>\n\n"
        "Тут зібрані всі теми та розділи мови, з яких будуть ставитися запитання. "
        "Ознайомтеся з ними, щоб знати, що саме повторити перед візитом до коледжу."
    )
    await replace_nav(callback.message, state, text=text, reply_markup=get_download_keyboard("program"))

@router.callback_query(F.data == "exams_schedule")
async def exams_schedule_info(callback: CallbackQuery, state: FSMContext):
    text = (
        "📅 <b>Розклад співбесід</b>\n\n"
        "Офіційний графік із зазначенням дати, часу та місця проведення вашого випробування."
    )
    await replace_nav(callback.message, state, text=text, reply_markup=get_download_keyboard("schedule"))

@router.callback_query(F.data.startswith("dl_exam_"))
async def download_exam_files_handler(callback: CallbackQuery, state: FSMContext):
    file_type = callback.data.replace("dl_exam_", "")
    paths = {
        "rules": "assets/files/Положення про провдення індивідуальної усної співбесіди.pdf",
        "program": "assets/files/Програма індивідуальної усної співбесіди.pdf",
        "schedule": "assets/files/Розклад індивідуальних устних співбесід.pdf"
    }
    document_path = paths.get(file_type)
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
            caption="✅ Файл завантажено. Для повернення до інших документів натисніть кнопку нижче.",
            reply_markup=get_after_exams_download_keyboard()
        )
        await state.update_data(last_menu_msg_id=sent_doc.message_id)
    else:
        await callback.answer("❌ Файл тимчасово відсутній.", show_alert=True)
    await callback.answer()