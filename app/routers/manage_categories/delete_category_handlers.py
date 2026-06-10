from math import ceil

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext
from constants import DELETE_CATEGORIES_ON_PAGE
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.categories import (
    DeleteCategoryIdCallbackFactory,
    ManageCategoriesBackKeyboardBuilder,
    ManageCategoriesDeleteKeyboardBuilder,
)
from keyboards.manage_categories.manage_categories_edit_keyboard import (
    EditCategoryIdCallbackFactory,
)
from settings.config import bot

from .router import router


class DeleteCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    category_id = State()


@router.callback_query(F.data == "delete_category", UserRoleFilter([Role.admin]))
async def delete_category_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / DELETE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = ManageCategoriesDeleteKeyboardBuilder(
        i18n=i18n,
        total_pages=total_pages,
        current_page=1,
        items=categories,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-categories-delete-choose",
        ),
        reply_markup=keyboard,
    )
    await state.set_state("category_id")


@router.callback_query(
    DeleteCategoryIdCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin]),
)
async def delete_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: EditCategoryIdCallbackFactory,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    current_page = callback_data.page

    await state.update_data(current_page=current_page)

    categories_data = await state.get_data()
    categories = categories_data["categories"][
        (current_page - 1) * DELETE_CATEGORIES_ON_PAGE : current_page * (DELETE_CATEGORIES_ON_PAGE)
    ]
    total_pages = categories_data["total_pages"]

    keyboard_builder = ManageCategoriesDeleteKeyboardBuilder(
        i18n=i18n,
        total_pages=total_pages,
        current_page=current_page,
        items=categories,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(text=i18n.get("manage-categories-delete-choose"), reply_markup=keyboard)


@router.callback_query(
    DeleteCategoryIdCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin]),
)
async def delete_category_choose(
    callback: CallbackQuery,
    callback_data: DeleteCategoryIdCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    categories_data = await state.get_data()
    category = next(
        (category for category in categories_data["categories"] if category.category_id == callback_data.category_id),
        None,
    )
    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()
    try:
        if not callback_data.category_id:
            raise ValueError
        await CategoryManager.delete(callback_data.category_id)
    except IntegrityError, ValueError:
        await callback.message.answer(
            text=i18n.get("manage_categories.delete.fail", category_name=category.name if category else "Unknown"),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=i18n.get("manage_categories.delete.success", category_name=category.name if category else "Unknown"),
            reply_markup=keyboard,
        )
