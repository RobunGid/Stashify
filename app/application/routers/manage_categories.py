from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.exceptions.category_item import CategoryItemNotFoundException
from application.filters.user_role_filter import UserRoleFilter
from application.keyboards.manage_category import (
    DeleteCategoryChooseCategoryCallbackFactory,
    DeleteCategoryConfirmCallbackFactory,
    DeleteCategoryConfirmKeyboardBuilder,
    EditCategoryChooseCategoryCallbackFactory,
    EntryEditCategoryKeyboardBuilder,
    ManageCategoriesBackKeyboardBuilder,
)
from application.schemas.category_item_schema import BaseCategoryItemSchema, CategoryItemUpdateSchema
from application.services.category_item import CategoryItemService
from dishka import FromDishka
from infrastructure.models.user_account import Role

from settings.aiogram import bot

router = Router()


@router.callback_query(F.data == "manage_categories", UserRoleFilter([Role.admin]))
async def manage_categories_entry_handler(callback: CallbackQuery, i18n: I18nContext):
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
    name = State()
    category_item_id = State()


@router.callback_query(
    EditCategoryChooseCategoryCallbackFactory.filter(),
    UserRoleFilter([Role.admin]),
)
async def edit_category_choose(
    callback: CallbackQuery,
    callback_data: EditCategoryChooseCategoryCallbackFactory,
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

    category_item_id = callback_data.category_item_id
    category_item = await service.get_one(category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(category_item_id)

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    answer_message = await callback.message.answer(
        text=i18n.get("manage-categories-edit-text", category_name=category_item.name),
        reply_markup=keyboard,
    )

    await state.update_data(
        category_item_id=category_item_id,
        message_ids_to_delete=[answer_message.message_id],
    )
    await state.set_state(EditCategoryState.name)


@router.message(EditCategoryState.name)
async def new_category_name_choose(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return

    await message.delete()

    state_data = await state.get_data()
    category_item_id = state_data["category_item_id"]
    category_item_entity = await service.get_one(category_item_id)
    if not category_item_entity:
        raise CategoryItemNotFoundException(category_item_id)

    state_data["name"] = message.html_text

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    update_schema = CategoryItemUpdateSchema(name=message.html_text)
    await service.update(item_id=category_item_id, item=update_schema.to_entity())
    await message.answer(
        text=i18n.get("manage-categories-edit-success", category_name=message.html_text),
        reply_markup=keyboard,
    )
    await state.clear()


class DeleteCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    category_item_id = State()


@router.callback_query(
    DeleteCategoryChooseCategoryCallbackFactory.filter(),
    UserRoleFilter([Role.admin]),
)
async def delete_category_choose(
    callback: CallbackQuery,
    callback_data: DeleteCategoryChooseCategoryCallbackFactory,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    category_item_id = callback_data.category_item_id
    category_item_entity = await service.get_one(category_item_id)
    if not category_item_entity:
        raise CategoryItemNotFoundException(category_item_id)
    keyboard_builder = DeleteCategoryConfirmKeyboardBuilder(i18n=i18n, category_item_id=category_item_id)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage-categories-delete-choose-to-delete", name=category_item_entity.name),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteCategoryConfirmCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_name_confirm(
    callback: CallbackQuery,
    callback_data: DeleteCategoryConfirmCallbackFactory,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    category_item_id = callback_data.category_item_id
    category_item_entity = await service.get_one(category_item_id)
    if not category_item_entity:
        raise CategoryItemNotFoundException(category_item_id)

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.delete_by_id(item_id=category_item_id)
    await callback.message.answer(
        text=i18n.get("manage-categories-delete-success", category_name=category_item_entity.name),
        reply_markup=keyboard,
    )


class CreateCategoryState(StatesGroup):
    name = State()


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
    await state.set_state(CreateCategoryState.name)


@router.message(
    CreateCategoryState.name,
    F.text,
    UserRoleFilter([Role.admin]),
)
async def create_category_final(message: Message, i18n: I18nContext, service: FromDishka[CategoryItemService]):
    if not message.from_user:
        return
    category_schema = BaseCategoryItemSchema(name=message.html_text, resource_item_count=0)

    keyboard_builder = ManageCategoriesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.create(category_schema.to_entity())
    await message.answer(
        text=i18n.get("manage-categories-create-success", category_name=category_schema.name),
        reply_markup=keyboard,
    )
