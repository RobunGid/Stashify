from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.filters.user_role_filter import UserRoleFilter
from application.filters.valid_callback_filter import ValidCallbackFilter
from application.keyboards.users import UserManageEntryKeyboardBuilder
from infrastructure.models.user_account import Role

from settings.aiogram import bot

router = Router()


@router.callback_query(F.data == "manage_users", UserRoleFilter([Role.admin]), ValidCallbackFilter())
async def manage_users_users(callback: CallbackQuery, i18n: I18nContext, message: Message):
    builder = UserManageEntryKeyboardBuilder(i18n)
    keyboard = builder.build()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await message.answer(
        text=i18n.get("manage-users-text"),
        reply_markup=keyboard,
    )
