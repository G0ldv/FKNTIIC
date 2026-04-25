from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

router = Router()

def get_contacts_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Відкрити Google Maps", url="https://maps.app.goo.gl/C2hPmjdxBk8Xp7Y4A")],
        [InlineKeyboardButton(text="💬 Telegram", url="https://t.me/+380671030577")],
        [InlineKeyboardButton(text="🔙 Повернутися до головного меню", callback_data="back_to_main")]
    ])
    return keyboard

@router.message(F.text == "📍 Локація та контакти")
async def contacts_handler(message: Message, state: FSMContext):
    temp_msg = await message.answer("Завантажую контакти...", reply_markup=ReplyKeyboardRemove())
    await temp_msg.delete()
    data = await state.get_data()
    last_msg_id = data.get("last_menu_msg_id")
    if last_msg_id:
        try:
            await message.chat.delete_message(last_msg_id)
            await state.update_data(last_menu_msg_id=None)
        except:
            pass
    text = (
        "📍 <b>Наші контакти та розташування</b>\n\n"
        "🏢 <b>Адреса:</b>\n"
        "м. Одеса, вул. Левітана, 46-а\n"
        "(Наукова/Юннатів)\n\n"
        "🕒 <b>Загальний графік роботи:</b>\n"
        "<code>Пн–Чт: 09:00 – 16:00</code>\n"
        "<code>Пт:    09:00 – 15:00</code>\n"
        "<i>Сб–Нд: Вихідні</i>\n\n"
        "📞 <b>Приймальна комісія:</b>\n"
        "+380671030577 (Telegram, Viber)\n\n"
        # "📧 <i>vstup.kntiis@gmail.com</i>\n\n"
        "👤 <b>Приймальна директора:</b>\n"
        "+380487492932\n"
        "📧 <i>kntiis.od@gmail.com</i>\n\n"
        "З будь-яких питань звертайтеся у робочий час! 😊"
    )
    await message.answer(
        text,
        reply_markup=get_contacts_keyboard()
    )
    await message.delete()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    sent_message = await callback.message.answer(
        "Ви повернулися в головне меню. Оберіть розділ: 👇",
        reply_markup=main_menu
    )
    await state.update_data(last_menu_msg_id=sent_message.message_id)
    await callback.answer()