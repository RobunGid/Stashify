from math import ceil
from uuid import uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_i18n import I18nContext
from application.exceptions.category_item import CategoryItemNotFoundException
from application.exceptions.quiz_item import QuizItemNotFoundException
from application.exceptions.quiz_question import QuizQuestionNotFoundException
from application.exceptions.resource_item import ResourceItemNotFoundException
from application.filters_schemas.category_item import CategoryItemFiltersSchema
from application.filters_schemas.resource_favorite import ResourceFavoriteFiltersSchema
from application.filters_schemas.resource_image import ResourceImageFiltersSchema
from application.filters_schemas.resource_item import ResourceItemFiltersSchema
from application.formaters.resource_item import ResourceItemFormatter
from application.keyboards.resource_quizes import (
    ListResourcesQuizQuestionCallbackFactory,
    ResourceQuizFinalKeyboardBuilder,
    ResourceQuizQuestionKeyboardBuilder,
)
from application.keyboards.resources import (
    CategoryListKeyboardBuilder,
    ListResourcesChooseCategoryCallbackFactory,
    ListResourcesChooseResourceCallbackFactory,
    ListResourcesItemCallbackFactory,
    ResourceItemKeyboardBuilder,
    ResourceListKeyboardBuilder,
    ResourceQuizConfirmKeyboardBuilder,
)
from application.schemas.quiz_result_schema import BaseQuizResultSchema
from application.schemas.resource_favorite_schema import BaseResourceFavoriteSchema
from application.schemas.resource_rating_schema import BaseResourceRatingSchema
from application.schemas.user_account_schema import UserAccountSchema
from application.services.category_item import CategoryItemService
from application.services.quiz_item import QuizItemService
from application.services.quiz_question import QuizQuestionService
from application.services.quiz_result import QuizResultService
from application.services.resource_favorite import ResourceFavoriteService
from application.services.resource_image import ResourceImageService
from application.services.resource_item import ResourceItemService
from application.services.resource_rating import ResourceRatingService
from constants import (
    LIST_RESOURCES_CATEGORIES_ON_PAGE,
    LIST_RESOURCES_RESOURCES_ON_PAGE,
)
from dishka import FromDishka

from settings.aiogram import bot

router = Router()


@router.callback_query(F.data == "resources")
async def list_resources_callback_handler(
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

    filters = CategoryItemFiltersSchema(count=LIST_RESOURCES_CATEGORIES_ON_PAGE, has_resource_items=True)
    category_items, count = await service.get_many(filters.to_entity())
    total_category_items_pages = ceil(count / LIST_RESOURCES_CATEGORIES_ON_PAGE)
    await state.update_data(
        total_categories_pages=total_category_items_pages,
        categories=category_items,
        current_page=1,
    )

    keyboard_builder = CategoryListKeyboardBuilder(
        i18n,
        items=category_items,
        current_page=1,
        total_pages=total_category_items_pages,
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
    service: FromDishka[ResourceItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    category_item_id = callback_data.category_item_id
    await state.update_data(category_item_id=category_item_id)
    filters = ResourceItemFiltersSchema(count=LIST_RESOURCES_RESOURCES_ON_PAGE, category_item_id=category_item_id)
    resource_items, count = await service.get_many(filters.to_entity())
    total_resources_pages = ceil(count / LIST_RESOURCES_RESOURCES_ON_PAGE)

    keyboard_builder = ResourceListKeyboardBuilder(
        i18n,
        items=resource_items,
        current_page=1,
        total_pages=total_resources_pages,
    )
    keyboard = keyboard_builder.build()

    await state.update_data(
        category_item_id=category_item_id,
        resources=resource_items,
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
    resource_item_service: FromDishka[ResourceItemService],
    category_item_service: FromDishka[CategoryItemService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    resource_rating_service: FromDishka[ResourceRatingService],
    quiz_item_service: FromDishka[QuizItemService],
    user_account: UserAccountSchema,
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
    resource_item_id = callback_data.resource_item_id

    resource_item = await resource_item_service.get_one(resource_item_id)
    if not resource_item:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    category_item = await category_item_service.get_one(resource_item.category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(resource_item.category_item_id)

    resource_entities_filters = ResourceItemFiltersSchema(
        category_item_id=resource_item.category_item_id,
        count=LIST_RESOURCES_RESOURCES_ON_PAGE,
    )
    resource_entities, _ = await resource_item_service.get_many(resource_entities_filters.to_entity())

    resource_favorite_filters = ResourceFavoriteFiltersSchema(user_account_id=user_account.user_account_id)
    resource_favorite_entities, _ = await resource_favorite_service.get_many(resource_favorite_filters.to_entity())

    resource_image_filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)
    resource_image_entities, _ = await resource_image_service.get_many(resource_image_filters.to_entity())
    is_favorite = any(
        resource_item.resource_item_id == favorite.resource_item_id for favorite in resource_favorite_entities
    )

    resource_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item.resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None

    await state.update_data(resources=resource_entities, resource_item=resource_item)

    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resource_entities,
        current_item=resource_item,
        is_favorite=is_favorite,
        rating=resource_rating_number,
        quiz_percent=0,
        has_quiz=bool(quiz_item),
    )
    keyboard = keyboard_builder.build()

    if resource_image_entities:
        media_group = MediaGroupBuilder()
        for photo in resource_image_entities:
            media_group.add_photo(type="photo", media=str(photo.image))

        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )

    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(
            resource_item=resource_item,
            category_item=category_item,
            i18n=i18n,
        ),
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
    resource_item_service: FromDishka[ResourceItemService],
    category_item_service: FromDishka[CategoryItemService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    resource_rating_service: FromDishka[ResourceRatingService],
    quiz_item_service: FromDishka[QuizItemService],
    user_account: UserAccountSchema,
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
    resource_item_id = callback_data.resource_item_id

    resource_item = await resource_item_service.get_one(resource_item_id)
    if not resource_item:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    category_item = await category_item_service.get_one(resource_item.category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(resource_item.category_item_id)

    resource_entities_filters = ResourceItemFiltersSchema(
        category_item_id=resource_item.category_item_id,
        count=LIST_RESOURCES_RESOURCES_ON_PAGE,
    )
    resource_entities, _ = await resource_item_service.get_many(resource_entities_filters.to_entity())

    resource_favorite_filters = ResourceFavoriteFiltersSchema(user_account_id=user_account.user_account_id)
    resource_favorite_entities, _ = await resource_favorite_service.get_many(resource_favorite_filters.to_entity())

    resource_image_filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)
    resource_image_entities, _ = await resource_image_service.get_many(resource_image_filters.to_entity())
    is_favorite = any(
        resource_item.resource_item_id == favorite.resource_item_id for favorite in resource_favorite_entities
    )

    resource_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item.resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None

    await state.update_data(resources=resource_entities, resource_item=resource_item)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resource_entities,
        current_item=resource_item,
        is_favorite=is_favorite,
        rating=resource_rating_number,
        quiz_percent=0,
        has_quiz=bool(quiz_item),
    )
    keyboard = keyboard_builder.build()
    if resource_image_entities:
        media_group = MediaGroupBuilder()
        for image in resource_image_entities:
            media_group.add_photo(type="photo", media=image.image)
        await callback.message.answer_media_group(
            media=list(media_group.build()),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=ResourceItemFormatter.translate_resource_item(
                resource_item=resource_item,
                category_item=category_item,
                i18n=i18n,
            ),
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
    resource_item_service: FromDishka[ResourceItemService],
    resource_rating_service: FromDishka[ResourceRatingService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    quiz_item_service: FromDishka[QuizItemService],
    category_item_service: FromDishka[CategoryItemService],
    user_account: UserAccountSchema,
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
    resource_item_id = callback_data.resource_item_id
    resource_item = await resource_item_service.get_one(resource_item_id)
    if not resource_item:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)

    category_item = await category_item_service.get_one(resource_item.category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(resource_item.category_item_id)

    state_data = await state.get_data()
    resource_entities = state_data["resources"]
    favorite = BaseResourceFavoriteSchema(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item.resource_item_id,
    )
    resource_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account.user_account_id,
        resource_item_id,
    )
    await resource_favorite_service.create(favorite.to_entity())

    filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)
    resource_images, _ = await resource_image_service.get_many(filters.to_entity())
    resource_rating_number = resource_rating.rating if resource_rating else None
    await state.update_data(resources=resource_entities)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resource_entities,
        current_item=resource_item,
        has_quiz=bool(quiz_item),
        is_favorite=True,
        quiz_percent=0,
        rating=resource_rating_number,
    )
    keyboard = keyboard_builder.build()
    # TODO: MAKE QUIZ_PERCENT GETTING!!
    if resource_images:
        media_group = MediaGroupBuilder()
        for image in resource_images:
            media_group.add_photo(type="photo", media=image.image)
        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(
            resource_item=resource_item,
            category_item=category_item,
            i18n=i18n,
        ),
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
    resource_item_service: FromDishka[ResourceItemService],
    resource_rating_service: FromDishka[ResourceRatingService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    quiz_item_service: FromDishka[QuizItemService],
    category_item_service: FromDishka[CategoryItemService],
    user_account: UserAccountSchema,
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
    resource_item_id = callback_data.resource_item_id

    resource_item = await resource_item_service.get_one(resource_item_id)
    if not resource_item:
        raise ResourceItemNotFoundException(resource_item_id)
    category_item = await category_item_service.get_one(resource_item.category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(resource_item.category_item_id)

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)

    filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)
    resource_images, _ = await resource_image_service.get_many(filters.to_entity())

    state_data = await state.get_data()
    resourc_entities = state_data["resources"]
    resource_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item.resource_item_id,
    )

    await resource_favorite_service.delete_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None
    await state.update_data(resources=resourc_entities)
    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resourc_entities,
        current_item=resource_item,
        has_quiz=bool(quiz_item),
        is_favorite=True,
        quiz_percent=0,
        rating=resource_rating_number,
    )
    keyboard = keyboard_builder.build()
    if resource_images:
        media_group = MediaGroupBuilder()
        for photo in resource_images:
            media_group.add_photo(type="photo", media=str(photo.image))

        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )
    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(
            resource_item=resource_item,
            category_item=category_item,
            i18n=i18n,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "rate"),
)
async def list_resource_resource_rate(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesItemCallbackFactory,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
    resource_rating_service: FromDishka[ResourceRatingService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    quiz_item_service: FromDishka[QuizItemService],
    category_item_service: FromDishka[CategoryItemService],
    user_account: UserAccountSchema,
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
    rating = callback_data.rating

    resource_item = await resource_item_service.get_one(resource_item_id)
    if not resource_item:
        raise ResourceItemNotFoundException(resource_item_id)

    category_item = await category_item_service.get_one(resource_item.category_item_id)
    if not category_item:
        raise CategoryItemNotFoundException(resource_item.category_item_id)

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)

    state_data = await state.get_data()
    resource_entities = state_data["resources"]

    existing_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item_id,
    )
    if existing_rating:
        await resource_rating_service.delete_by_user_account_id_and_resource_item_id(
            user_account_id=user_account.user_account_id,
            resource_item_id=resource_item_id,
        )

    new_rating = BaseResourceRatingSchema(
        resource_rating_id=uuid4(),
        resource_item_id=resource_item_id,
        rating=rating,
        user_account_id=user_account.user_account_id,
    )
    await resource_rating_service.create(new_rating.to_entity())

    resource_favorite_filters = ResourceFavoriteFiltersSchema(user_account_id=user_account.user_account_id)
    favorites, _ = await resource_favorite_service.get_many(resource_favorite_filters.to_entity())

    is_favorite = any(resource_item.resource_item_id == favorite.resource_item_id for favorite in favorites)

    resource_images_filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)
    resource_images, _ = await resource_image_service.get_many(resource_images_filters.to_entity())

    await state.update_data(resources=resource_entities)

    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        items=resource_entities,
        current_item=resource_item,
        has_quiz=bool(quiz_item),
        is_favorite=is_favorite,
        quiz_percent=0,
        rating=rating,
    )
    keyboard = keyboard_builder.build()

    if resource_images:
        media_group = MediaGroupBuilder()
        for image in resource_images:
            media_group.add_photo(type="photo", media=image.image)

        await callback.message.answer_media_group(
            media=list(media_group.build()),
        )

    await callback.message.answer(
        text=ResourceItemFormatter.translate_resource_item(
            resource_item=resource_item,
            category_item=category_item,
            i18n=i18n,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "start_quiz"),
)
async def list_resource_start_quiz(
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
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    state_data = await state.get_data()
    resource_item = state_data["resource_item"]
    state_data = await state.get_data()

    keyboard_builder = ResourceQuizConfirmKeyboardBuilder(i18n=i18n, current_item=resource_item)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-start-quiz-question",
            question_count=len(resource_item.quiz.questions),
            resource_name=resource_item.name,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "start_quiz_cnfrm"),
)
async def list_resource_start_quiz_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesItemCallbackFactory,
    i18n: I18nContext,
    quiz_item_service: FromDishka[QuizItemService],
    resource_item_service: FromDishka[ResourceItemService],
    quiz_question_service: FromDishka[QuizQuestionService],
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
    resource_item_id = callback_data.resource_item_id

    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)

    state_data = await state.get_data()
    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz_item:
        raise QuizItemNotFoundException(resource_item_id)

    quiz_question_entity = await quiz_question_service.get_one_by_question_number(
        resource_item_id=resource_item_id,
        quiz_question_number=0,
    )
    if not quiz_question_entity:
        raise QuizQuestionNotFoundException(resource_item_id)

    page = state_data["current_page"]
    await state.update_data(quiz=quiz_item)
    await state.update_data(quiz_answers=[])
    keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
        i18n=i18n,
        item=resource_item_entity,
        question=quiz_question_entity,
        page=page,
        question_number=0,
    )
    keyboard = keyboard_builder.build()

    if quiz_question_entity.image:
        await callback.message.answer_photo(
            photo=quiz_question_entity.image,
            text=quiz_question_entity.text,
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(text=quiz_question_entity.text, reply_markup=keyboard)


@router.callback_query(
    ListResourcesQuizQuestionCallbackFactory.filter(F.action == "answer"),
)
async def list_resource_quiz_question_answer(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesQuizQuestionCallbackFactory,
    i18n: I18nContext,
    quiz_result_service: FromDishka[QuizResultService],
    user_account: UserAccountSchema,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    current_quiz_answers = state_data["quiz_answers"]
    resource_item = state_data["resource"]
    question_number = callback_data.question_number
    page = state_data["current_page"]

    if question_number + 1 < len(quiz.questions):
        keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
            i18n=i18n,
            item=resource_item,
            page=page,
            question=quiz.questions[question_number + 1],
            question_number=question_number,
        )
        keyboard = keyboard_builder.build()
        await state.update_data(
            quiz_answers=current_quiz_answers + [callback_data.option_number],
        )
        if quiz.questions[question_number + 1].image:
            await callback.message.answer_photo(
                photo=quiz.questions[question_number + 1].image,
                text=quiz.questions[question_number + 1].text,
                reply_markup=keyboard,
            )
        else:
            await callback.message.answer(text=quiz.questions[question_number + 1].text, reply_markup=keyboard)
    else:
        quiz_answers = current_quiz_answers + [callback_data.option_number]
        right_answers = [question.right_options for question in quiz.questions]
        right_answers_len = len(
            [quiz_answers[i] for i in range(len(quiz_answers)) if quiz_answers[i] in right_answers[i]],
        )
        right_answer_percent = int(100 * right_answers_len / len(quiz_answers))

        state_data = await state.get_data()
        resource_item = state_data["resource"]
        existing_quiz_result = await quiz_result_service.get_one_by_user_account_id_and_resource_item_id(
            resource_item.resource_item_id,
            user_account.user_account_id,
        )
        if existing_quiz_result:
            await quiz_result_service.delete_by_user_account_id_and_resource_item_id(
                resource_item.resource_item_id,
                user_account.user_account_id,
            )
        quiz_result = BaseQuizResultSchema(
            quiz_result_id=uuid4(),
            quiz_item_id=quiz.quiz_item_id,
            user_account_id=user_account.user_account_id,
            percent=right_answer_percent,
        )
        await quiz_result_service.create(quiz_result.to_entity())

        keyboard_builder = ResourceQuizFinalKeyboardBuilder(i18n=i18n, item=resource_item, page=page)
        keyboard = keyboard_builder.build()
        await callback.message.answer(
            text=i18n.get("start-quiz-final", percent=right_answer_percent),
            reply_markup=keyboard,
        )
