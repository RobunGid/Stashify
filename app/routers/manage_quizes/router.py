from aiogram import F, Router
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.manage_quizes.manage_quizes_keyboard import manage_quizes_keyboard
from settings.config import bot

router = Router()


@router.callback_query(
    F.data == "manage_quizes",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def manage_quizes(callback: CallbackQuery, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-text",
        ),
        reply_markup=manage_quizes_keyboard(callback.from_user.language_code),
    )
