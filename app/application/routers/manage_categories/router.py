from math import ceil

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.filters.user_role_filter import UserRoleFilter
from application.filters_schemas.category_item import CategoryItemFiltersSchema
from application.keyboards.categories import (
    DeleteCategoryIdCallbackFactory,
    DeleteCategoryKeyboardBuilder,
    EditCategoryIdCallbackFactory,
    EditCategoryListKeyboardBuilder,
    EntryEditCategoryKeyboardBuilder,
    ManageCategoriesBackKeyboardBuilder,
)
from application.routers.constants import DELETE_CATEGORIES_ON_PAGE, EDIT_CATEGORIES_ON_PAGE
from application.schemas.category_item_schema import BaseCategoryItemSchema, CategoryItemUpdateSchema
from application.services.category_item import CategoryItemService
from dishka import FromDishka
from infrastructure.models.user_account import Role
from sqlalchemy.exc import IntegrityError

from settings.aiogram import bot

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


class EditCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    new_category_name = State()
    category_item_id = State()


@router.callback_query(F.data == "edit_category", UserRoleFilter([Role.admin]))
async def edit_category_callback_handler(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    filters = CategoryItemFiltersSchema(
        count=EDIT_CATEGORIES_ON_PAGE,
    )
    category_entities, count = await service.get_many(filters.to_entity())
    total_pages = ceil(count / EDIT_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, category_items=category_entities)

    keyboard_builder = EditCategoryListKeyboardBuilder(
        i18n=i18n,
        items=category_entities,
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
    await state.set_state("category_item_id")


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
    categories = categories_data["category_items"][
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

    await state.update_data(category_item_id=callback_data.category_item_id)
    await state.set_state(EditCategoryState.new_category_name)


@router.message(EditCategoryState.new_category_name)
async def new_category_name_choose(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return
    state_data = await state.get_data()
    category_item_id = state_data["category_item_id"]
    state_data["name"] = message.html_text

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        update_schema = CategoryItemUpdateSchema(name=message.html_text)
        await service.update(item_id=category_item_id, item=update_schema.to_entity())
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


class DeleteCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    category_item_id = State()


@router.callback_query(F.data == "delete_category", UserRoleFilter([Role.admin]))
async def delete_category_callback_handler(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    filters = CategoryItemFiltersSchema(
        count=DELETE_CATEGORIES_ON_PAGE,
    )
    category_entities, count = await service.get_many(filters.to_entity())
    total_pages = ceil(count / DELETE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, category_items=category_entities)

    keyboard_builder = DeleteCategoryKeyboardBuilder(
        i18n=i18n,
        total_pages=total_pages,
        current_page=1,
        items=category_entities,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-categories-delete-choose",
        ),
        reply_markup=keyboard,
    )
    await state.set_state("category_item_id")


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
    categories = categories_data["category_items"][
        (current_page - 1) * DELETE_CATEGORIES_ON_PAGE : current_page * (DELETE_CATEGORIES_ON_PAGE)
    ]
    total_pages = categories_data["total_pages"]

    keyboard_builder = DeleteCategoryKeyboardBuilder(
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
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    categories_data = await state.get_data()
    category_item = next(
        (
            category_item
            for category_item in categories_data["category_items"]
            if category_item.category_item_id == callback_data.category_item_id
        ),
        None,
    )
    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()
    try:
        if not callback_data.category_item_id:
            raise ValueError
        await service.delete_by_id(callback_data.category_item_id)
    except IntegrityError, ValueError:
        await callback.message.answer(
            text=i18n.get(
                "manage-categories-delete-fail",
                category_name=category_item.name if category_item else "Unknown",
            ),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=i18n.get(
                "manage-categories-delete-success",
                category_name=category_item.name if category_item else "Unknown",
            ),
            reply_markup=keyboard,
        )


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
        text=i18n.get("manage-categories-create-text"),
        reply_markup=keyboard,
    )
    await state.set_state(CreateCategoryState.choosing_category_name)


@router.message(
    CreateCategoryState.choosing_category_name,
    F.text,
    UserRoleFilter([Role.admin]),
)
async def create_category_final(message: Message, i18n: I18nContext, service: FromDishka[CategoryItemService]):
    if not message.from_user:
        return
    category_schema = BaseCategoryItemSchema(name=message.html_text)

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await service.create(category_schema.to_entity())
    except IntegrityError:
        await message.answer(
            text=i18n.get("manage-categories-create-fail", category_name=category_schema.name),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get("manage-categories-create-success", category_name=category_schema.name),
            reply_markup=keyboard,
        )
