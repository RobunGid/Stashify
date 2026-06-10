from math import ceil

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext
from constants import (
    DELETE_RESOURCE_CATEGORIES_ON_PAGE,
    DELETE_RESOURCE_RESOURCES_ON_PAGE,
)
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager, ResourceManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.manage_resources.manage_resources_delete_resource_list_keyboard import (
    DeleteResourceChooseResourceCallbackFactory,
    manage_resources_delete_resource_list_keyboard,
)
from keyboards.resources import (
    DeleteResourceCategoryListKeyboardBuilder,
    DeleteResourceChooseCategoryCallbackFactory,
    DeleteResourceConfirmKeyboardBuilder,
    ManageResourcesBackKeyboardBuilder,
)
from schemas.resource_schema import ResourceItemSchema
from settings.config import bot

from .router import router


class DeleteResourceState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_item_id = State()
    confirm = State()


@router.callback_query(
    F.data == "delete_resource",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / DELETE_RESOURCE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = DeleteResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        total_pages=total_pages,
        current_page=1,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-delete-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteResourceChooseCategoryCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_categories_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: DeleteResourceChooseCategoryCallbackFactory,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    current_page = callback_data.page

    resources_data = await state.get_data()
    categories = resources_data["categories"][
        (current_page - 1) * DELETE_RESOURCE_CATEGORIES_ON_PAGE : current_page * (DELETE_RESOURCE_CATEGORIES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    keyboard_builder = DeleteResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        total_pages=total_pages,
        current_page=current_page,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-delete-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteResourceChooseCategoryCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_category_select(
    callback: CallbackQuery,
    callback_data: DeleteResourceChooseCategoryCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    current_page = callback_data.page
    resources_data = await state.get_data()
    category_id = callback_data.category_id
    resources = await ResourceManager.get_many(category_id=category_id)
    total_pages = resources_data["total_pages"]
    await state.update_data(category_id=category_id, resources=resources)
    await callback.message.answer(
        text=i18n.get(
            "manage-resources-delete-choose-resource",
        ),
        reply_markup=manage_resources_delete_resource_list_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code,
            total_pages=total_pages,
            page=int(current_page),
        ),
    )


@router.callback_query(
    DeleteResourceChooseResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: DeleteResourceChooseResourceCallbackFactory,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    current_page = callback_data.page

    resources_data = await state.get_data()
    resources = resources_data["resources"][
        (current_page - 1) * DELETE_RESOURCE_RESOURCES_ON_PAGE : current_page * (DELETE_RESOURCE_RESOURCES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-delete-choose-resource",
        ),
        reply_markup=manage_resources_delete_resource_list_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code,
            total_pages=total_pages,
            page=int(current_page),
        ),
    )


@router.callback_query(
    DeleteResourceChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_select(
    callback: CallbackQuery,
    callback_data: DeleteResourceChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    state_data = await state.get_data()
    resource_item: ResourceItemSchema = next(
        (resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id),
    )

    keyboard_builder = DeleteResourceConfirmKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await state.update_data(resource_item_id=resource_item_id)
    await callback.message.answer(
        text=i18n.get("manage-resources-delete-choose-to-delete", name=resource_item.name),
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == "delete_resource_confirm",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_name_confirm(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_data = await state.get_data()
    resource: ResourceItemSchema = next(
        (
            resource
            for resource in resource_data["resources"]
            if resource.resource_item_id == resource_data["resource_item_id"]
        ),
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await ResourceManager.delete(resource_item_id=resource_data["resource_item_id"])
    except IntegrityError, ValueError:
        await callback.message.answer(
            text=i18n.get(
                "manage_resources.delete.fail",
                callback.from_user.language_code,
            ).format(name=resource.name),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=i18n.get(
                "manage_resources.delete.success",
                callback.from_user.language_code,
            ).format(name=resource.name),
            reply_markup=keyboard,
        )
