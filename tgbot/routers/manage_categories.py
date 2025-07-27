from uuid import uuid4
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_categories_keyboard import manage_categories_keyboard
from config.bot_config import bot
from database.operations.create_category import create_category
from schemas.category_schema import CategorySchema
from keyboards.manage_categories_back_keyboard import manage_categories_back_keyboard

router = Router()

@router.callback_query(F.data=="manage_categories", UserRoleFilter([Role.admin]))
async def manage_categories(callback: CallbackQuery):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.text", callback.from_user.language_code), 
        reply_markup=manage_categories_keyboard(callback.from_user.language_code)
    )
    
class CreateCategoryState(StatesGroup):
    choosing_category_name = State()
    
@router.callback_query(F.data=="create_category", UserRoleFilter([Role.admin]))
async def create_category_callback_handle(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.create.text", callback.from_user.language_code), 
    )
    await state.set_state(CreateCategoryState.choosing_category_name)
    
@router.message(CreateCategoryState.choosing_category_name, F.text, UserRoleFilter([Role.admin]))
async def create_category_final(message: Message, state: FSMContext):
    if not message.from_user: return
    category_data = CategorySchema(id=str(uuid4()), name=message.html_text)
    try:
        await create_category(category_data)
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