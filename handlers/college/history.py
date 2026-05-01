from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import log_section_click
from utils.navigation import edit_nav

router = Router()

def get_history_more_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Детальніше на сайті", url="https://www.kntiis.od.ua/uk/istoriya")],
        [InlineKeyboardButton(text="🔙 Назад до вибору", callback_data="open_about_menu")]
    ])
    return keyboard

@router.callback_query(F.data == "history_more")
async def history_handler(callback: CallbackQuery, state: FSMContext):
    await log_section_click("📜 Історія та заснування")
    text = (
        "📜 <b>Історія заснування та становлення</b>\n\n"
        "Наш коледж розпочав свій шлях ще у <b>1944 році</b>. Уявіть, Одеса тільки-но була звільнена, "
        "а країні вже потрібні були фахівці для відбудови нафтогазової галузі.\n\n"
        "За ці десятиліття ми пройшли шлях від технікуму до потужного структурного підрозділу <b>ОНТУ</b>. "
        "Сьогодні ми готуємо «технологічну еліту»: від айтішників та екологів до фахівців нафтогазової справи "
        "та готельно-ресторанного бізнесу.\n\n"
        "🎓 <b>Гордість коледжу:</b> Тисячі випускників, які сьогодні керують підприємствами не тільки в Україні, а й за кордоном. "
        "Ми зберігаємо традиції класичної освіти, поєднуючи їх з діджиталізацією."
   )
    await edit_nav(callback.message, state, text=text, reply_markup=get_history_more_keyboard())
    await callback.answer()