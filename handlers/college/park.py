from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import edit_nav

router = Router()

def get_park_more_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Детальніше на сайті", url="https://www.kntiis.od.ua/uk/dendropark")],
        [InlineKeyboardButton(text="🔙 Назад до вибору", callback_data="open_about_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "park_more")
async def park_handler(callback: CallbackQuery, state: FSMContext):
    await log_section_click("🌳 Дендропарк «Студентський»")
    text = (
        "🌳 <b>Дендропарк «Студентський» — наша зелена перлина</b>\n\n"
        "Чи багато навчальних закладів можуть похвалитися власним заповідником? А ми можемо! 😎\n\n"
        "Дендропарк займає <b>4,2 гектари</b>. Він був заснований разом із коледжем, щоб створити "
        "ідеальні умови для навчання та відпочинку. Тут ростуть десятки видів рідкісних рослин, "
        "багато з яких занесені до Червоної книги.\n\n"
        "🦜 <b>Це жива екосистема:</b> Студенти часто проводять тут час між парами. Парк має статус "
        "заповідної території, тому повітря тут — як у лісі, хоча ми знаходимося в самому серці Одеси (вул. Левітана)."
    )
    await edit_nav(callback.message, state, text=text, reply_markup=get_park_more_keyboard())
    await callback.answer()