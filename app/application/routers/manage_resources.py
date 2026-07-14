from typing import List
from uuid import uuid4

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_i18n import I18nContext
from aiogram_media_group import media_group_handler
from application.exceptions.category_item import CategoryItemNotFoundException
from application.exceptions.resource_item import ResourceItemNotFoundException
from application.filters.user_role_filter import UserRoleFilter
from application.filters_schemas.resource_image import ResourceImageFiltersSchema
from application.keyboards.manage_resources import (
    CreateResourceCallbackFactory,
    DeleteResourceChooseResourceCallbackFactory,
    DeleteResourceConfirmCallbackFactory,
    DeleteResourceConfirmKeyboardBuilder,
    EditResourceChooseFieldKeyboardBuilder,
    EditResourceChooseResourceCallbackFactory,
    ManageResourcesBackKeyboardBuilder,
    ResourceManageEntryKeyboardBuilder,
)
from application.schemas.resource_image_schema import BaseResourceImageSchema
from application.schemas.resource_item_schema import BaseResourceItemSchema, ResourceItemUpdateSchema
from application.services.category_item import CategoryItemService
from application.services.resource_image import ResourceImageService
from application.services.resource_item import ResourceItemService
from dishka import FromDishka
from infrastructure.models.user_account import Role

from settings.aiogram import bot

router = Router()


@router.callback_query(
    F.data == "manage_resources",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def manage_resources_entry_handler(
    callback: CallbackQuery,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    keyboard_builder = ResourceManageEntryKeyboardBuilder(i18n)
    keyboard = keyboard_builder.build()
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text=i18n.get(
            "manage-resources-text",
        ),
        reply_markup=keyboard,
    )


class CreateResourceState(StatesGroup):
    name = State()
    description = State()
    links = State()
    images = State()
    tags = State()
    category_item_id = State()


@router.callback_query(
    CreateResourceCallbackFactory.filter(),
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

    await state.set_state(CreateResourceState.name)
    await state.update_data(category_item_id=callback_data.category_item_id)


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
            "manage-resources-create-wait-images",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateResourceState.images)


@router.message(F.media_group_id, CreateResourceState.images)
@media_group_handler
async def new_resource_image_choose(messages: List[Message], state: FSMContext, i18n: I18nContext):
    if not messages[0].from_user or not messages[0].from_user.language_code:
        return

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
async def new_resource_tags_choose(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
    resource_image_service: FromDishka[ResourceImageService],
    category_item_service: FromDishka[CategoryItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return
    state_data = await state.get_data()
    category_item_entity = await category_item_service.get_one(state_data["category_item_id"])
    if not category_item_entity:
        raise CategoryItemNotFoundException(state_data["category_item_id"])

    resource_data = BaseResourceItemSchema(
        category_item_id=state_data["category_item_id"],
        resource_item_id=uuid4(),
        name=state_data["name"],
        description=state_data["description"],
        links=state_data["links"],
        tags=message.html_text,
        verified=False,
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await resource_item_service.create(resource_data.to_entity())
    for resource_image in state_data["images"]:
        image = BaseResourceImageSchema(
            resource_image_id=uuid4(),
            resource_item_id=resource_data.resource_item_id,
            image=resource_image,
        )
        await resource_image_service.create(image.to_entity())

    if len(state_data["images"]) > 1:
        media_group = MediaGroupBuilder()

        for image in state_data["images"]:
            media_group.add_photo(type="photo", media=image)

        await message.answer_media_group(
            media=list(media_group.build()),
        )
    else:
        await message.answer_photo(
            photo=state_data["images"][0],
        )

    await message.answer(
        i18n.get(
            "manage-resources-create-success",
            resource_name=resource_data.name,
            resource_description=resource_data.description,
            resource_tags=resource_data.tags,
            category_name=category_item_entity.name,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteResourceChooseResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_select(
    callback: CallbackQuery,
    callback_data: DeleteResourceChooseResourceCallbackFactory,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = DeleteResourceConfirmKeyboardBuilder(i18n=i18n, resource_item_id=resource_item_id)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage-resources-delete-choose-to-delete", name=resource_item_entity.name),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteResourceConfirmCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_resource_name_confirm(
    callback: CallbackQuery,
    callback_data: DeleteResourceConfirmCallbackFactory,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    resource_item_entity = await service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.delete_by_id(item_id=resource_item_id)
    await callback.message.answer(
        text=i18n.get("manage-resources-delete-success", name=resource_item_entity.name),
        reply_markup=keyboard,
    )


class EditResourceState(StatesGroup):
    resource_item_id = State()
    name = State()
    description = State()
    images = State()
    tags = State()


@router.callback_query(
    EditResourceChooseResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_choose(
    callback: CallbackQuery,
    callback_data: EditResourceChooseResourceCallbackFactory,
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
    await state.update_data(resource_item_id=resource_item_id)

    keyboard_builder = EditResourceChooseFieldKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-choose-to-change",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == "edit_resource_name",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_name(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    resource_item = await service.get_one(resource_item_id)
    if resource_item is None:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    answer_message = await callback.message.answer(
        text=i18n.get("manage-resources-edit-name-text", name=resource_item.name),
        reply_markup=keyboard,
    )
    await state.update_data(
        message_ids_to_delete=[answer_message.message_id],
    )
    await state.set_state(EditResourceState.name)


@router.message(
    EditResourceState.name,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_name_success(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return

    await message.delete()

    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]

    resource_item_update_schema = ResourceItemUpdateSchema(name=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.update(item_id=resource_item_id, item=resource_item_update_schema.to_entity())
    await message.answer(
        text=i18n.get("manage-resources-edit-name-success", name=message.html_text),
        reply_markup=keyboard,
    )
    await state.clear()


@router.callback_query(
    F.data == "edit_resource_description",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_description(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    resource_item = await service.get_one(resource_item_id)
    if resource_item is None:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    answer_message = await callback.message.answer(
        text=i18n.get("manage-resources-edit-description-text", description=resource_item.description),
        reply_markup=keyboard,
    )
    await state.update_data(
        message_ids_to_delete=[answer_message.message_id],
    )
    await state.set_state(EditResourceState.description)


@router.message(
    EditResourceState.description,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_description_success(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return

    await message.delete()

    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]

    resource_item_update_schema = ResourceItemUpdateSchema(description=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.update(item_id=resource_item_id, item=resource_item_update_schema.to_entity())
    await message.answer(
        text=i18n.get("manage-resources-edit-description-success", description=message.html_text),
        reply_markup=keyboard,
    )
    await state.clear()


@router.callback_query(
    F.data == "edit_resource_tags",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_tags(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    resource_item = await service.get_one(resource_item_id)
    if resource_item is None:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    answer_message = await callback.message.answer(
        text=i18n.get("manage-resources-edit-tags-text", tags=resource_item.tags),
        reply_markup=keyboard,
    )
    await state.update_data(
        message_ids_to_delete=[answer_message.message_id],
    )
    await state.set_state(EditResourceState.tags)


@router.message(
    EditResourceState.tags,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_tags_success(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceItemService],
):
    if not message.from_user or not message.from_user.language_code:
        return

    await message.delete()

    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]

    resource_item_update_schema = ResourceItemUpdateSchema(tags=message.html_text)

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await service.update(item_id=resource_item_id, item=resource_item_update_schema.to_entity())
    await message.answer(
        text=i18n.get("manage-resources-edit-tags-success", tags=message.html_text),
        reply_markup=keyboard,
    )
    await state.clear()


@router.callback_query(
    F.data == "edit_resource_image",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_image(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    resource_image_service: FromDishka[ResourceImageService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id, count=10)
    resource_image_entities, count = await resource_image_service.get_many(filters.to_entity())

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    if count > 1:
        media_group = MediaGroupBuilder()

        for resource_image_entity in resource_image_entities:
            media_group.add_photo(type="photo", media=resource_image_entity.image)

        answer_photos = await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
        bot_photo_ids = [m.message_id for m in answer_photos]
    else:
        answer_photo = await callback.message.answer_photo(
            photo=resource_image_entities[0].image,
        )
        bot_photo_ids = [answer_photo.message_id]

    answer_text_message = await callback.message.answer(
        text=i18n.get("manage-resources-edit-image-text"),
        reply_markup=keyboard,
    )

    await state.update_data(
        message_ids_to_delete=bot_photo_ids + [answer_text_message.message_id],
    )
    await state.set_state(EditResourceState.images)


@router.message(
    EditResourceState.images,
    UserRoleFilter([Role.admin, Role.manager]),
    F.media_group_id,
    F.content_type.in_({"photo"}),
)
@media_group_handler
async def edit_resource_image_success(
    messages: list[Message],
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceImageService],
):
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]

    for message in messages:
        try:
            await message.delete()
        except TelegramAPIError:
            pass
    resource_item_id = state_data["resource_item_id"]

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    new_images = [m.photo[-1].file_id for m in messages if m.photo]
    if not new_images:
        await messages[0].answer(
            text=i18n.get(
                "manage-resources-edit-image-fail",
            ),
            reply_markup=keyboard,
        )
        return

    filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id, count=10)
    existing_resource_image_entities, _ = await service.get_many(filters.to_entity())

    for existing_resource_image_entity in existing_resource_image_entities:
        await service.delete_by_id(existing_resource_image_entity.resource_image_id)

    for resource_image in new_images:
        resource_image_schema = BaseResourceImageSchema(
            resource_image_id=uuid4(),
            resource_item_id=resource_item_id,
            image=resource_image,
        )
        await service.create(resource_image_schema.to_entity())

    if len(new_images) > 1:
        media_group = MediaGroupBuilder()

        for resource_image in new_images:
            media_group.add_photo(type="photo", media=resource_image)

        answer_image_messages = await messages[0].answer_media_group(
            media=list(media_group.build()),
        )
    else:
        answer_image_message = await messages[0].answer_photo(
            photo=new_images[0],
        )
        answer_image_messages = [answer_image_message]

    answer_image_message_ids = [message.message_id for message in answer_image_messages]
    await messages[0].answer(
        text=i18n.get(
            "manage-resources-edit-image-success",
        ),
        reply_markup=keyboard,
    )
    await state.clear()
    await state.update_data(
        message_ids_to_delete=answer_image_message_ids,
    )


@router.message(
    EditResourceState.images,
    UserRoleFilter([Role.admin, Role.manager]),
    ~F.media_group_id,
    F.content_type.in_({"photo"}),
)
async def edit_resource_image_single_success(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[ResourceImageService],
):
    await message.delete()
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    if not message.photo:
        await message.answer(
            text=i18n.get(
                "manage-resources-edit-image-fail",
            ),
            reply_markup=keyboard,
        )
        return

    new_image = message.photo[-1].file_id

    filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id, count=10)
    existing_resource_image_entities, count = await service.get_many(filters.to_entity())

    for existing_resource_image_entity in existing_resource_image_entities:
        await service.delete_by_id(existing_resource_image_entity.resource_image_id)

    resource_image_schema = BaseResourceImageSchema(
        resource_image_id=uuid4(),
        resource_item_id=resource_item_id,
        image=new_image,
    )
    await service.create(resource_image_schema.to_entity())

    answer_image_message = await message.answer_photo(
        photo=new_image,
    )

    await message.answer(
        text=i18n.get(
            "manage-resources-edit-image-success",
        ),
        reply_markup=keyboard,
    )
    await state.clear()
    await state.update_data(
        message_ids_to_delete=[answer_image_message.message_id],
    )
