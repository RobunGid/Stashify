from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from config.bot_config import bot
from schemas.category_schema import CategorySchema
from keyboards.manage_categories.manage_categories_back_keyboard import manage_categories_back_keyboard
from .router import router
from database.managers import CategoryManager

class CreateCategoryState(StatesGroup):
    choosing_category_name = State()

@router.callback_query(F.data=="create_category", UserRoleFilter([Role.admin]))
async def create_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.create.text", callback.from_user.language_code), 
        reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(CreateCategoryState.choosing_category_name)
    
@router.message(CreateCategoryState.choosing_category_name, F.text, UserRoleFilter([Role.admin]))
async def create_category_final(message: Message):
    if not message.from_user: 
        return
    category_data = CategorySchema(id=uuid4(), name=message.html_text)
    try:
        await CategoryManager.create(category_data)
    except IntegrityError:
        await message.answer(
            text=t("manage_categories.create.fail", message.from_user.language_code).format(category_name=category_data.name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )
    else:
        await message.answer(
            text=t("manage_categories.create.success", message.from_user.language_code).format(category_name=category_data.name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )