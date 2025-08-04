from aiogram import F
from aiogram.types import CallbackQuery

from database.models.user import Role
from .router import router
from config.bot_config import bot
from keyboards.manage_quizes.manage_quizes_keyboard import manage_quizes_keyboard
from filters.user_role_filter import UserRoleFilter
from i18n import t

@router.callback_query(F.data=="manage_quizes", UserRoleFilter([Role.admin, Role.manager]))
async def manage_quizes(callback: CallbackQuery):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_quizes.text", callback.from_user.language_code), 
        reply_markup=manage_quizes_keyboard(callback.from_user.language_code)
    )