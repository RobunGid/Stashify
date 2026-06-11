from math import ceil

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from constants import EDIT_CATEGORIES_ON_PAGE

from database.managers import CategoryManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.categories import (
    EditCategoryIdCallbackFactory,
    EditCategoryListKeyboardBuilder,
    ManageCategoriesBackKeyboardBuilder,
)
from settings.config import bot

from .router import router


class EditCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    new_category_name = State()
    category_id = State()


@router.callback_query(F.data == "edit_category", UserRoleFilter([Role.admin]))
async def edit_category_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / EDIT_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = EditCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        total_pages=total_pages,
        current_page=1,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-categories-edit-text",
        ),
        reply_markup=keyboard,
    )
    await state.set_state("category_id")


@router.callback_query(
    EditCategoryIdCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin]),
)
async def edit_category_page(
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
        (current_page - 1) * EDIT_CATEGORIES_ON_PAGE : current_page * (EDIT_CATEGORIES_ON_PAGE)
    ]
    total_pages = categories_data["total_pages"]

    keyboard_builder = EditCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        total_pages=total_pages,
        current_page=current_page,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-categories-edit-choose",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditCategoryIdCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin]),
)
async def edit_category_choose(
    callback: CallbackQuery,
    callback_data: EditCategoryIdCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-categories-edit-text",
        ),
        reply_markup=keyboard,
    )

    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(EditCategoryState.new_category_name)


@router.message(EditCategoryState.new_category_name)
async def new_category_name_choose(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    state_data = await state.get_data()
    category_id = state_data["category_id"]
    state_data["name"] = message.html_text

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await CategoryManager.update(category_id, **state_data)
    except ValueError:
        await message.answer(
            text=i18n.get("manage-categories-edit-fail", category_name=message.html_text),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get("manage-categories-edit-success", category_name=message.html_text),
            reply_markup=keyboard,
        )
    await state.clear()
