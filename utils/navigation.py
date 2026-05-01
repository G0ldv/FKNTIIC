from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

async def edit_nav(message: Message, state: FSMContext, text: str, reply_markup: InlineKeyboardMarkup):
    try: await message.delete()
    except: pass
    data = await state.get_data()
    last_id = data.get("last_menu_msg_id")
    if last_id:
        try:
            sent = await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_id,
                text=text,
                reply_markup=reply_markup
            )
            return sent
        except: 
            pass
    return await replace_nav(message, state, text, reply_markup)

async def replace_nav(message: Message, state: FSMContext, text: str, reply_markup=None, photo_path=None, save_history: bool = False, is_welcome: bool = False):
    if not save_history:
        try: await message.delete()
        except: pass
    data = await state.get_data()
    last_id = data.get("last_menu_msg_id")
    if last_id and not save_history:
        try: await message.bot.delete_message(message.chat.id, last_id)
        except: pass
    if photo_path:
        photo = FSInputFile(photo_path) if isinstance(photo_path, str) else photo_path
        sent = await message.answer_photo(photo, caption=text, reply_markup=reply_markup)
    else:
        sent = await message.answer(text=text, reply_markup=reply_markup)
    if is_welcome:
        await state.update_data(last_menu_msg_id=None)
    else:
        await state.update_data(last_menu_msg_id=sent.message_id)
    return sent