from database.models.user import Role
from aiogram.types import CallbackQuery
from aiogram import F

from .router import router
from filters.user_role_filter import UserRoleFilter
from keyboards.manage_resources.manage_resources_keyboard import manage_resources_keyboard
from config.bot_config import bot
from i18n import t

@router.callback_query(F.data=="manage_resources", UserRoleFilter([Role.admin, Role.manager]))
async def manage_resources(callback: CallbackQuery):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_resources.text", callback.from_user.language_code), 
        reply_markup=manage_resources_keyboard(callback.from_user.language_code)
    )