from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery


from database.operations.get_user_role import get_user_role
from keyboards.main_menu_keyboard import main_menu_keyboard
from i18n import t
from config.bot_config import bot

router = Router()

@router.message(Command("menu"))
async def main_menu_command(message: Message):
    if not message.from_user or not message.from_user.id: return

    user_role = await get_user_role(str(message.from_user.id))
    
    reply_keyboard = main_menu_keyboard(user_role, message.from_user.language_code)
    await message.answer(t("main_menu.text", message.from_user.language_code), reply_markup=reply_keyboard)
    
@router.callback_query(F.data=="menu")
async def main_menu_callback_handler(callback: CallbackQuery):
    if not callback.from_user or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    user_role = await get_user_role(str(callback.from_user.id))
    reply_keyboard = main_menu_keyboard(user_role, callback.from_user.language_code)
    
    await callback.message.answer(t("main_menu.text", callback.from_user.language_code), reply_markup=reply_keyboard)