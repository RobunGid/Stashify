from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.categories import ManageCategoriesBackKeyboardBuilder
from schemas.category_schema import CategorySchema
from settings.config import bot

from .router import router


class CreateCategoryState(StatesGroup):
    choosing_category_name = State()


@router.callback_query(F.data == "create_category", UserRoleFilter([Role.admin]))
async def create_category_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage_categories.create.text"),
        reply_markup=keyboard,
    )
    await state.set_state(CreateCategoryState.choosing_category_name)


@router.message(
    CreateCategoryState.choosing_category_name,
    F.text,
    UserRoleFilter([Role.admin]),
)
async def create_category_final(message: Message, i18n: I18nContext):
    if not message.from_user:
        return
    category_data = CategorySchema(category_id=UUID(), name=message.html_text)

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await CategoryManager.create(category_data)
    except IntegrityError:
        await message.answer(
            text=i18n.get("manage_categories.create.fail", category_name=category_data.name),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get("manage_categories.create.success", category_name=category_data.name),
            reply_markup=keyboard,
        )
