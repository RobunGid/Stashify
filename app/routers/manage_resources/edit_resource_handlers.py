from math import ceil

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, PhotoSize

from aiogram_i18n import I18nContext
from constants import EDIT_RESOURCE_CATEGORIES_ON_PAGE, EDIT_RESOURCE_RESOURCES_ON_PAGE
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager, ResourceManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.resources import (
    EditResourceCategoryListKeyboardBuilder,
    EditResourceChooseCategoryCallbackFactory,
    EditResourceChooseFieldKeyboardBuilder,
    EditResourceChooseResourceCallbackFactory,
    EditResourceResourceListKeyboardBuilder,
    ManageResourcesBackKeyboardBuilder,
)
from settings.config import bot

from .router import router


class EditResourceState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_item_id = State()
    name = State()
    description = State()
    image = State()
    tags = State()


@router.callback_query(
    F.data == "edit_resource",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / EDIT_RESOURCE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = EditResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditResourceChooseCategoryCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: EditResourceChooseCategoryCallbackFactory,
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

    state_data = await state.get_data()
    categories = state_data["categories"][
        (current_page - 1) * EDIT_RESOURCE_CATEGORIES_ON_PAGE : current_page * (EDIT_RESOURCE_CATEGORIES_ON_PAGE)
    ]
    total_pages = state_data["total_pages"]

    keyboard_builder = EditResourceCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=current_page,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditResourceChooseCategoryCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_category_choose(
    callback: CallbackQuery,
    callback_data: EditResourceChooseCategoryCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    category_id = callback_data.category_id
    resources = await ResourceManager.get_many(category_id=category_id)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources) / EDIT_RESOURCE_RESOURCES_ON_PAGE)

    keyboard_builder = EditResourceResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-choose-to-change",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditResourceChooseResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: EditResourceChooseResourceCallbackFactory,
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

    resources_data = await state.get_data()
    resources = resources_data["resources"][
        (current_page - 1) * EDIT_RESOURCE_RESOURCES_ON_PAGE : current_page * (EDIT_RESOURCE_RESOURCES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    keyboard_builder = EditResourceResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=current_page,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-choose",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditResourceChooseResourceCallbackFactory.filter(F.action == "select"),
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
async def edit_resource_name(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_name = next(
        (
            resource.name
            for resource in state_data["resources"]
            if resource.resource_item_id == state_data["resource_item_id"]
        ),
        "Unknown",
    )

    keyboard_builder = EditResourceChooseFieldKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage-resources-edit-name-text", name=resource_name),
        reply_markup=keyboard,
    )
    await state.set_state(EditResourceState.name)


@router.message(
    EditResourceState.name,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_name_success(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return

    resource_item_data = await state.get_data()

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        resource_item_data["name"] = message.html_text
        await ResourceManager.update(**resource_item_data)
    except IntegrityError, ValueError:
        await message.answer(
            text=i18n.get("manage-resources-edit-name-fail", name=message.html_text),
            reply_markup=keyboard,
        )
        await state.set_state(EditResourceState.name)
    else:
        await message.answer(
            text=i18n.get("manage-resources-edit-name-success", name=message.html_text),
            reply_markup=keyboard,
        )


@router.callback_query(
    F.data == "edit_resource_description",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_description(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_description = next(
        (
            resource.description
            for resource in state_data["resources"]
            if resource.resource_item_id == state_data["resource_item_id"]
        ),
        "Unknown",
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage_resources.edit.description.text", description=resource_description),
        reply_markup=keyboard,
    )
    await state.set_state(EditResourceState.description)


@router.message(
    EditResourceState.description,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_description_success(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    resource_data = await state.get_data()

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        resource_data["description"] = message.html_text
        await ResourceManager.update(**resource_data)
    except IntegrityError, ValueError:
        await message.answer(
            text=i18n.get("manage-resources-edit-description-fail", description=message.html_text),
            reply_markup=keyboard,
        )
        await state.set_state(EditResourceState.description)
    else:
        await message.answer(
            text=i18n.get("manage-resources-edit-description-success", description=message.html_text),
            reply_markup=keyboard,
        )


@router.callback_query(
    F.data == "edit_resource_tags",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_tags(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_tags = next(
        (
            resource.tags
            for resource in state_data["resources"]
            if resource.resource_item_id == state_data["resource_item_id"]
        ),
        "Unknown",
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-resources-edit-tags-text",
            tags=resource_tags,
        ),
        reply_markup=keyboard,
    )
    await state.set_state(EditResourceState.tags)


@router.message(
    EditResourceState.tags,
    UserRoleFilter([Role.admin, Role.manager]),
    F.text,
)
async def edit_resource_tags_success(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return
    resource_data = await state.get_data()
    resource_data["tags"] = message.html_text

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await ResourceManager.update(**resource_data)
    except IntegrityError, ValueError:
        await message.answer(
            text=i18n.get(
                "manage_resources.edit.tags.fail",
                tags=message.html_text,
            ),
            reply_markup=keyboard,
        )
        await state.set_state(EditResourceState.tags)
    else:
        await message.answer(
            text=i18n.get(
                "manage_resources.edit.tags.success",
                tags=message.html_text,
            ),
            reply_markup=keyboard,
        )


@router.callback_query(
    F.data == "edit_resource_image",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_image(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_image = next(
        (
            resource.image
            for resource in state_data["resources"]
            if resource.resource_item_id == state_data["resource_item_id"]
        ),
        "Unknown",
    )

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer_photo(
        photo=resource_image,
        caption=i18n.get("manage-resources-edit-image-text"),
        reply_markup=keyboard,
    )
    await state.set_state(EditResourceState.image)


@router.message(
    EditResourceState.image,
    UserRoleFilter([Role.admin, Role.manager]),
    F.photo[-1].as_("resource_image"),
)
async def edit_resource_image_success(
    message: Message,
    state: FSMContext,
    resource_image: PhotoSize,
    i18n: I18nContext,
):
    if not message.from_user or not message.from_user.language_code:
        return
    resource_data = await state.get_data()
    resource_data["image"] = resource_image.file_id

    keyboard_builder = ManageResourcesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await ResourceManager.update(**resource_data)
    except IntegrityError, ValueError:
        await message.answer_photo(
            photo=resource_image.file_id,
            caption=i18n.get(
                "manage-resources-edit-image-fail",
            ),
            reply_markup=keyboard,
        )
        await state.set_state(EditResourceState.image)
    else:
        await message.answer_photo(
            photo=resource_image.file_id,
            caption=i18n.get(
                "manage-resources-edit-image-success",
            ),
            reply_markup=keyboard,
        )
