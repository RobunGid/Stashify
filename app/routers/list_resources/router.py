from math import ceil
from uuid import UUID

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_i18n import I18nContext
from constants import (
    LIST_RESOURCES_CATEGORIES_ON_PAGE,
    LIST_RESOURCES_RESOURCES_ON_PAGE,
)
from formaters.resource_item import ResourceItemFormatter

from database.managers import (
    CategoryManager,
    FavoriteManager,
    ResourceImageManager,
    ResourceManager,
    ResourceRatingManager,
)
from keyboards.resources import (
    CategoryListKeyboardBuilder,
    ListResourcesChooseCategoryCallbackFactory,
    ListResourcesChooseResourceCallbackFactory,
    ListResourcesItemCallbackFactory,
    ResourceItemKeyboardBuilder,
    ResourceListKeyboardBuilder,
)
from schemas.favorite_schema import FavoriteSchema
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from settings.config import bot

router = Router()


@router.callback_query(F.data == "resources")
async def list_resources_callback_handler(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many(has_resources=True)
    total_categories_pages = ceil(len(categories) / LIST_RESOURCES_CATEGORIES_ON_PAGE)
    await state.update_data(
        total_categories_pages=total_categories_pages,
        categories=categories,
        current_page=1,
    )

    keyboard_builder = CategoryListKeyboardBuilder(
        i18n,
        items=categories,
        current_page=1,
        total_pages=total_categories_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesChooseCategoryCallbackFactory.filter(F.action == "change_page"),
)
async def list_resources_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseCategoryCallbackFactory,
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
        (current_page - 1) * LIST_RESOURCES_CATEGORIES_ON_PAGE : current_page * (LIST_RESOURCES_CATEGORIES_ON_PAGE)
    ]
    total_categories_pages = categories_data["total_categories_pages"]

    keyboard_builder = CategoryListKeyboardBuilder(
        i18n,
        items=categories,
        current_page=current_page,
        total_pages=total_categories_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesChooseCategoryCallbackFactory.filter(F.action == "select"),
)
async def list_resources_category_select(
    callback: CallbackQuery,
    callback_data: ListResourcesChooseCategoryCallbackFactory,
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
    await state.update_data(category_id=category_id)
    resources = await ResourceManager.get_many(category_id=category_id)
    total_resources_pages = ceil(len(resources) / LIST_RESOURCES_RESOURCES_ON_PAGE)

    keyboard_builder = ResourceListKeyboardBuilder(
        i18n,
        items=resources,
        current_page=1,
        total_pages=total_resources_pages,
    )
    keyboard = keyboard_builder.build()

    await state.update_data(
        category_id=category_id,
        resources=resources,
        total_resources_pages=total_resources_pages,
    )
    await callback.message.answer(
        text=i18n.get(
            "list-resources-choose-resource",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesChooseResourceCallbackFactory.filter(F.action == "change_page"),
)
async def list_resource_resource_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
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
        (current_page - 1) * LIST_RESOURCES_RESOURCES_ON_PAGE : current_page * (LIST_RESOURCES_RESOURCES_ON_PAGE)
    ]
    total_resources_pages = resources_data["total_resources_pages"]

    keyboard_builder = ResourceListKeyboardBuilder(
        i18n,
        items=resources,
        current_page=current_page,
        total_pages=total_resources_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-change-page",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesChooseResourceCallbackFactory.filter(F.action == "select"),
)
async def list_resource_resource_select(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
    i18n: I18nContext,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_item_id
    ):
        return

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    resource_item = await ResourceManager.get_one(resource_item_id=callback_data.resource_item_id)
    if not resource_item:
        return

    state_data = await state.get_data()

    category_id = state_data["category_id"]
    resources = await ResourceManager.get_many(category_id=category_id)
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_many(user_id=user_id)
    images = await ResourceImageManager.get_many(resource_item_id=callback_data.resource_item_id)
    is_favorite = any(resource_item.resource_item_id == favorite.resource_item_id for favorite in favorites)

    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_item_id=resource_item.resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None

    await state.update_data(resources=resources, resource_item=resource_item)

    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_item=resource_item,
        is_favorite=is_favorite,
        rating=resource_rating_number,
        quiz_percent=0,
        has_quiz=bool(resource_item.quiz),
    )
    keyboard = keyboard_builder.build()

    if images:
        media_group = MediaGroupBuilder()
        for photo in images:
            media_group.add_photo(type="photo", media=str(photo.image))

        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )

    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(resource_item=resource_item, i18n=i18n),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "change_page"),
)
async def list_resource_resource_change_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
    i18n: I18nContext,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_item_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item = await ResourceManager.get_one(resource_item_id=callback_data.resource_item_id)
    if not resource_item:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_many(user_id=user_id)
    images = await ResourceImageManager.get_many(resource_item_id=callback_data.resource_item_id)
    is_favorite = any(resource_item.resource_item_id == favorite.resource_item_id for favorite in favorites)
    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_item_id=resource_item.resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None
    await state.update_data(resources=resources, resource=resource_item)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_item=resource_item,
        is_favorite=is_favorite,
        rating=resource_rating_number,
        quiz_percent=0,
        has_quiz=bool(resource_item.quiz),
    )
    keyboard = keyboard_builder.build()
    if images:
        media_group = MediaGroupBuilder()
        for photo in images:
            media_group.add_photo(type="photo", media=photo)
        await callback.message.answer_media_group(
            media=list(media_group.build()),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=ResourceItemFormatter.translate_resource_item(resource_item=resource_item, i18n=i18n),
            reply_markup=keyboard,
        )


# FAVORITES
# TODO: Make multiple callback factories for pagination, select, etc.


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "add_favorite"),
)
async def list_resource_resource_add_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
    i18n: I18nContext,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_item_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item = await ResourceManager.get_one(resource_item_id=callback_data.resource_item_id)
    if not resource_item:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    user_id = str(callback.from_user.id)
    favorite = FavoriteSchema(user_id=user_id, resource_item_id=resource_item.resource_item_id)
    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_item_id=resource_item.resource_item_id,
    )
    await FavoriteManager.create(favorite)
    images = await ResourceImageManager.get_many(resource_item_id=callback_data.resource_item_id)
    resource_rating_number = resource_rating.rating if resource_rating else None
    await state.update_data(resources=resources)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_item=resource_item,
        has_quiz=bool(resource_item.quiz),
        is_favorite=True,
        quiz_percent=0,
        rating=resource_rating_number,
    )
    keyboard = keyboard_builder.build()
    # TODO: MAKE QUIZ_PERCENT GETTING!!
    if images:
        media_group = MediaGroupBuilder()
        for photo in images:
            media_group.add_photo(type="photo", media=photo)
        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(resource_item=resource_item, i18n=i18n),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "remove_favorite"),
)
async def list_resource_resource_remove_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
    i18n: I18nContext,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_item_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item = await ResourceManager.get_one(resource_item_id=callback_data.resource_item_id)
    images = await ResourceImageManager.get_many(resource_item_id=callback_data.resource_item_id)
    if not resource_item:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    user_id = str(callback.from_user.id)
    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_item_id=resource_item.resource_item_id,
    )

    await FavoriteManager.delete(user_id=user_id, resource_item_id=resource_item.resource_item_id)
    resource_rating_number = resource_rating.rating if resource_rating else None
    await state.update_data(resources=resources)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_item=resource_item,
        has_quiz=bool(resource_item.quiz),
        is_favorite=True,
        quiz_percent=0,
        rating=resource_rating_number,
    )
    keyboard = keyboard_builder.build()
    if images:
        media_group = MediaGroupBuilder()
        for photo in images:
            media_group.add_photo(type="photo", media=str(photo.image))

        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(resource_item=resource_item, i18n=i18n),
        reply_markup=keyboard,
    )


@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action == "rate"))
async def list_resource_resource_rate(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesItemCallbackFactory,
    i18n: I18nContext,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_item_id
        or not callback_data.rating
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    resource_item = await ResourceManager.get_one(resource_item_id=resource_item_id)
    if not resource_item:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_many(user_id=user_id)
    is_favorite = any(resource_item.resource_item_id == favorite.resource_item_id for favorite in favorites)
    rating = callback_data.rating
    existing_resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_item_id=resource_item.resource_item_id,
    )
    if existing_resource_rating:
        await ResourceRatingManager.delete(user_id=user_id, resource_item_id=resource_item.resource_item_id)
    resource_rating = ResourceRatingWithoutUserAndResourceSchema(
        resource_rating_id=UUID(),
        resource_item_id=resource_item_id,
        rating=rating,
        user_id=user_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_item=resource_item,
        has_quiz=bool(resource_item.quiz),
        is_favorite=is_favorite,
        quiz_percent=0,
        rating=resource_rating_number,
    )
    keyboard = keyboard_builder.build()
    await ResourceRatingManager.create(resource_rating)
    await state.update_data(resources=resources)
    images = await ResourceImageManager.get_many(resource_item_id=callback_data.resource_item_id)
    if images:
        media_group = MediaGroupBuilder()
        for photo in images:
            media_group.add_photo(type="photo", media=photo)
        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(resource_item=resource_item, i18n=i18n),
        reply_markup=keyboard,
    )
