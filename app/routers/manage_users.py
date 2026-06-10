from aiogram import F, Router
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.users import ManageUsersKeyboardBuilder
from settings.config import bot

router = Router()


@router.callback_query(F.data == "manage_users", UserRoleFilter([Role.admin]))
async def manage_users_users(callback: CallbackQuery, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    builder = ManageUsersKeyboardBuilder(i18n)
    keyboard = builder.build()
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text=i18n.get("manage-users-text"),
        reply_markup=keyboard,
    )
