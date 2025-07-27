from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_users_keyboard import manage_users_keyboard
from config.bot_config import bot

router = Router()

@router.callback_query(F.data=="manage_users", UserRoleFilter([Role.admin]))
async def manage_users_users(callback: CallbackQuery):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_users.text", callback.from_user.language_code), 
        reply_markup=manage_users_keyboard(callback.from_user.language_code)
    )