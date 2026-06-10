from math import ceil
from typing import List
from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_i18n import I18nContext
from aiogram_media_group import media_group_handler
from constants import CREATE_RESOURCE_CATEGORIES_ON_PAGE
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager, ResourceImageManager, ResourceManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.resources import (
    CreateResourceCallbackFactory,
    CreateResourceCategoryListKeyboardBuilder,
    ManageResourcesBackKeyboardBuilder,
)
from routers.manage_resources.router import router
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema
from schemas.resource_schema import BaseResourceItemSchema
from settings.config import bot


class CreateResourceState(StatesGroup):
    total_pages = State()
    categories = State()
    category_id = State()
    name = State()
    description = State()
    links = State()
    images = State()
    tags = State()


@router.callback_query(
    F.data == "create_resource",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_resource_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / CREATE_RESOURCE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = CreateResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-create-choose-category",
        ),
        reply_markup=keyboard,
    )
    await state.set_state("resource_item_id")


@router.callback_query(
    CreateResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_resource_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CreateResourceCallbackFactory,
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
        (current_page - 1) * CREATE_RESOURCE_CATEGORIES_ON_PAGE : current_page * (CREATE_RESOURCE_CATEGORIES_ON_PAGE)
    ]
    total_pages = categories_data["total_pages"]

    keyboard_builder = CreateResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=current_page,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-create-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_resource_choose(
    callback: CallbackQuery,
    callback_data: CreateResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-create-wait-name",
        ),
        reply_markup=keyboard,
    )

    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(CreateResourceState.name)


@router.message(
    CreateResourceState.name,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def new_resource_name_choose(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    await state.update_data(name=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-resources-create-wait-description",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateResourceState.description)


@router.message(
    CreateResourceState.description,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def new_resource_description_choose(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    await state.update_data(description=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-resources-create-wait-links",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateResourceState.links)


@router.message(
    CreateResourceState.links,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def new_resource_links_choose(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    await state.update_data(links=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage_resources.create.wait_images",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateResourceState.images)


@router.message(F.media_group_id)
@media_group_handler
async def new_resource_image_choose(messages: List[Message], state: FSMContext, i18n: I18nContext):
    if not messages[0].from_user or not messages[0].from_user.language_code:
        return
    await state.update_data(images=[message.photo[-1].file_id for message in messages if message.photo])

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await messages[0].answer(
        text=i18n.get(
            "manage-resources-create-wait-tags",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateResourceState.tags)


@router.message(CreateResourceState.tags, F.text)
async def new_resource_tags_choose(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    state_data = await state.get_data()
    resource_data = BaseResourceItemSchema(
        category_id=state_data["category_id"],
        resource_item_id=UUID(),
        name=state_data["name"],
        description=state_data["description"],
        links=state_data["links"],
        tags=message.html_text,
    )
    category_name = next(
        (category.name for category in state_data["categories"]),
        "Unknown",
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await ResourceManager.create(resource_data)
        for resource_image in state_data["images"]:
            image = ResourceImageWithoutResourceSchema(
                resource_image_id=UUID(),
                resource_item_id=resource_data.resource_item_id,
                image=resource_image,
            )
            await ResourceImageManager.create(image)
    except IntegrityError:
        await message.answer(
            text=i18n.get(
                "manage_resources.create.fail",
                message.from_user.language_code,
            ).format(
                resource_name=resource_data.name,
                resource_description=resource_data.description,
                resource_tags=resource_data.tags,
                category_name=category_name,
            ),
            reply_markup=keyboard,
        )
    else:
        if len(state_data["images"]) > 1:
            media_group = MediaGroupBuilder(
                caption=i18n.get(
                    "manage_resources.create.success",
                    resource_name=resource_data.name,
                    resource_description=resource_data.description,
                    resource_tags=resource_data.tags,
                    category_name=category_name,
                ),
            )
            for image in state_data["images"]:
                media_group.add_photo(type="photo", media=image)
            await message.answer_media_group(media=list(media_group.build()), reply_markup=keyboard)
        else:
            await message.answer_photo(
                photo=state_data["images"][0],
                caption=i18n.get(
                    "manage_resources.create.success",
                    resource_name=resource_data.name,
                    resource_description=resource_data.description,
                    resource_tags=resource_data.tags,
                    category_name=category_name,
                ),
                reply_markup=keyboard,
            )
