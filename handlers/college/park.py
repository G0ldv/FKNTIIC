from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "park_more")
async def park_handler(callback: CallbackQuery):
    text = (
        "🌳 <b>Дендропарк «Студентський» — наша зелена перлина</b>\n\n"
        "Чи багато навчальних закладів можуть похвалитися власним заповідником? А ми можемо! 😎\n\n"
        "Дендропарк займає <b>4,2 гектари</b>. Він був заснований разом із коледжем, щоб створити "
        "ідеальні умови для навчання та відпочинку. Тут ростуть десятки видів рідкісних рослин, "
        "багато з яких занесені до Червоної книги.\n\n"
        "🦜 <b>Це жива екосистема:</b> Студенти часто проводять тут час між парами. Парк має статус "
        "заповідної території, тому повітря тут — як у лісі, хоча ми знаходимося в самому серці Одеси (вул. Левітана)."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Детальніше на сайті", url="https://www.kntiis.od.ua/uk/dendropark")],
        [InlineKeyboardButton(text="🔙 Назад до вибору", callback_data="open_about_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)