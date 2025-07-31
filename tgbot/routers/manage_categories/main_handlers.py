from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_categories.manage_categories_keyboard import manage_categories_keyboard
from config.bot_config import bot
from .router import router

@router.callback_query(F.data=="manage_categories", UserRoleFilter([Role.admin]))
async def manage_categories(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.text", callback.from_user.language_code), 
        reply_markup=manage_categories_keyboard(callback.from_user.language_code)
    )