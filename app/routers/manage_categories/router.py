from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.categories import EntryEditCategoryKeyboardBuilder
from settings.config import bot

router = Router()


@router.callback_query(F.data == "manage_categories", UserRoleFilter([Role.admin]))
async def manage_categories(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.clear()
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return

    keyboard_builder = EntryEditCategoryKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text=i18n.get("manage-categories-text"),
        reply_markup=keyboard,
    )
