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
from application.filters_schemas.quiz_question import QuizQuestionFiltersSchema
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
    ListCategoriesItemCallbackFactory,
    ListResourcesItemCallbackFactory,
    ResourceItemDetailsCallbackFactory,
    ResourceItemKeyboardBuilder,
    ResourceListKeyboardBuilder,
    ResourceQuizConfirmKeyboardBuilder,
)
from application.routers.constants import LIST_RESOURCES_CATEGORIES_ON_PAGE, LIST_RESOURCES_RESOURCES_ON_PAGE
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
from dishka import FromDishka

from settings.aiogram import bot

router = Router()


@router.callback_query(F.data == "resources")
async def list_resources_category_page_init(
    callback: CallbackQuery,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    filters = CategoryItemFiltersSchema(count=LIST_RESOURCES_CATEGORIES_ON_PAGE, has_resource_items=True)
    category_item_entities, count = await service.get_many(filters.to_entity())
    total_category_items_pages = ceil(count / LIST_RESOURCES_CATEGORIES_ON_PAGE)

    keyboard_builder = CategoryListKeyboardBuilder(
        i18n,
        items=category_item_entities,
        current_page=0,
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
    ListCategoriesItemCallbackFactory.filter(F.action == "change_page"),
)
async def list_resources_category_page(
    callback: CallbackQuery,
    callback_data: ListCategoriesItemCallbackFactory,
    i18n: I18nContext,
    service: FromDishka[CategoryItemService],
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    current_page = callback_data.page
    filters = CategoryItemFiltersSchema(count=LIST_RESOURCES_CATEGORIES_ON_PAGE, has_resource_items=True)
    category_item_entities, count = await service.get_many(filters.to_entity())
    total_category_items_pages = ceil(count / LIST_RESOURCES_CATEGORIES_ON_PAGE)

    keyboard_builder = CategoryListKeyboardBuilder(
        i18n,
        items=category_item_entities,
        current_page=current_page,
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
    ListResourcesItemCallbackFactory.filter(),
)
async def list_resource_resource_page(
    callback: CallbackQuery,
    callback_data: ListResourcesItemCallbackFactory,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.category_item_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    current_page = callback_data.page
    category_item_id = callback_data.category_item_id

    filters = ResourceItemFiltersSchema(
        count=LIST_RESOURCES_RESOURCES_ON_PAGE,
        category_item_id=category_item_id,
    )
    resource_item_entities, count = await resource_item_service.get_many(filters.to_entity())
    total_resources_pages = ceil(count / LIST_RESOURCES_RESOURCES_ON_PAGE)

    keyboard_builder = ResourceListKeyboardBuilder(
        i18n,
        items=resource_item_entities,
        current_page=current_page,
        total_pages=total_resources_pages,
        category_item_id=category_item_id,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-change-page",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ResourceItemDetailsCallbackFactory.filter(),
)
async def list_resource_resource_select(
    callback: CallbackQuery,
    callback_data: ResourceItemDetailsCallbackFactory,
    i18n: I18nContext,
    resource_item_service: FromDishka[ResourceItemService],
    category_item_service: FromDishka[CategoryItemService],
    resource_favorite_service: FromDishka[ResourceFavoriteService],
    resource_image_service: FromDishka[ResourceImageService],
    resource_rating_service: FromDishka[ResourceRatingService],
    quiz_item_service: FromDishka[QuizItemService],
    quiz_result_service: FromDishka[QuizResultService],
    user_account: UserAccountSchema,
):
    if not callback.message or not callback.data or not callback_data.resource_item_id:
        return

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)

    is_quiz_exists = await quiz_item_service.check_exists_by_resource_item_id(resource_item_id)
    quiz_result_entity = await quiz_result_service.get_one(resource_item_id)

    resource_image_filters = ResourceImageFiltersSchema(resource_item_id=resource_item_id)

    resource_image_entities, _ = await resource_image_service.get_many(resource_image_filters.to_entity())

    resource_rating = await resource_rating_service.get_one_by_user_account_id_and_resource_item_id(
        user_account_id=user_account.user_account_id,
        resource_item_id=resource_item_entity.resource_item_id,
    )
    resource_rating_number = resource_rating.rating if resource_rating else None
    quiz_result_percent = quiz_result_entity.percent if quiz_result_entity else None

    (
        resource_item_index_in_category,
        resource_item_entities_navigation_ids_tuple,
        total_resource_item_count,
    ) = await resource_item_service.get_resource_pagination(
        category_item_id=resource_item_entity.category_item_id,
        resource_item_id=resource_item_id,
    )

    category_item_entity = await category_item_service.get_one(resource_item_entity.category_item_id)
    if not category_item_entity:
        raise CategoryItemNotFoundException(resource_item_entity.category_item_id)

    match callback_data.action:
        case "select":
            ...
        case "add_favorite":
            resource_favorite_schema = BaseResourceFavoriteSchema(
                user_account_id=user_account.user_account_id,
                resource_item_id=resource_item_id,
            )
            await resource_favorite_service.create(resource_favorite_schema.to_entity())
        case "remove_favorite":
            await resource_favorite_service.delete_by_user_account_id_and_resource_item_id(
                user_account_id=user_account.user_account_id,
                resource_item_id=resource_item_id,
            )
        case "rate":
            if callback_data.rating:
                resource_item_rating = BaseResourceRatingSchema(
                    resource_rating_id=uuid4(),
                    resource_item_id=resource_item_id,
                    rating=callback_data.rating,
                    user_account_id=user_account.user_account_id,
                )
                await resource_rating_service.create(resource_item_rating.to_entity())

    is_favorite = await resource_favorite_service.check_exists_by_user_account_id_and_resource_item_id(
        user_account.user_account_id,
        resource_item_id,
    )

    keyboard_builder = ResourceItemKeyboardBuilder(
        i18n=i18n,
        item_ids=resource_item_entities_navigation_ids_tuple,
        current_item=resource_item_entity,
        total_items=total_resource_item_count,
        is_favorite=is_favorite,
        has_quiz=is_quiz_exists,
        rating=resource_rating_number,
        current_item_index=resource_item_index_in_category,
        quiz_percent=quiz_result_percent,
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
            resource_item=resource_item_entity,
            category_item=category_item_entity,
            i18n=i18n,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ResourceItemDetailsCallbackFactory.filter(F.action == "start_quiz"),
)
async def list_resource_start_quiz(
    callback: CallbackQuery,
    callback_data: ResourceItemDetailsCallbackFactory,
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

    resource_item_id = callback_data.resource_item_id

    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item_entity = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz_item_entity:
        raise QuizItemNotFoundException(resource_item_id)

    quiz_question_count = await quiz_question_service.get_count_by_quiz_item_id(quiz_item_entity.quiz_item_id)

    keyboard_builder = ResourceQuizConfirmKeyboardBuilder(i18n=i18n, current_item=resource_item_entity)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-start-quiz-question",
            question_count=quiz_question_count,
            resource_name=resource_item_entity.name,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    ResourceItemDetailsCallbackFactory.filter(F.action == "start_quiz_cnfrm"),
)
async def list_resource_start_quiz_confirm(
    callback: CallbackQuery,
    callback_data: ResourceItemDetailsCallbackFactory,
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

    quiz_item = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz_item:
        raise QuizItemNotFoundException(resource_item_id)

    quiz_question_entity = await quiz_question_service.get_one_by_question_number(
        resource_item_id=resource_item_id,
        quiz_question_number=0,
    )
    if not quiz_question_entity:
        raise QuizQuestionNotFoundException(resource_item_id)

    keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
        i18n=i18n,
        item=resource_item_entity,
        question=quiz_question_entity,
        page=1,
        question_number=0,
        quiz_item=quiz_item,
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
    callback_data: ListResourcesQuizQuestionCallbackFactory,
    i18n: I18nContext,
    quiz_result_service: FromDishka[QuizResultService],
    quiz_item_service: FromDishka[QuizItemService],
    quiz_question_service: FromDishka[QuizQuestionService],
    resource_item_service: FromDishka[ResourceItemService],
    user_account: UserAccountSchema,
    state: FSMContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    question_number = callback_data.question_number

    quiz_item_id = callback_data.quiz_item_id
    quiz_item_entity = await quiz_item_service.get_one(quiz_item_id)
    if not quiz_item_entity:
        raise QuizItemNotFoundException(quiz_item_id)

    resource_item_entity = await resource_item_service.get_one(quiz_item_entity.resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(quiz_item_entity.resource_item_id)

    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_entity.resource_item_id)
    quiz_question_entities, count = await quiz_question_service.get_many(filters.to_entity())

    if question_number + 1 < count:
        keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
            i18n=i18n,
            item=resource_item_entity,
            page=0,
            question=quiz_question_entities[question_number + 1],
            question_number=question_number,
            quiz_item=quiz_item_entity,
        )
        keyboard = keyboard_builder.build()
        image = quiz_question_entities[question_number + 1].image

        if image is None:
            await callback.message.answer(text=quiz_question_entities[question_number + 1].text, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(
                photo=image,
                text=quiz_question_entities[question_number + 1].text,
                reply_markup=keyboard,
            )
    else:
        state_data = await state.get_data()
        current_quiz_answers = state_data["current_quiz_answers"]
        quiz_answers = current_quiz_answers + [callback_data.option_number]
        right_answers = [question.right_options for question in quiz_question_entities]
        right_answers_len = len(
            [quiz_answers[i] for i in range(len(quiz_answers)) if quiz_answers[i] in right_answers[i]],
        )
        right_answer_percent = int(100 * right_answers_len / len(quiz_answers))

        existing_quiz_result = await quiz_result_service.get_one_by_user_account_id_and_resource_item_id(
            resource_item_entity.resource_item_id,
            user_account.user_account_id,
        )
        if existing_quiz_result:
            await quiz_result_service.delete_by_user_account_id_and_resource_item_id(
                resource_item_entity.resource_item_id,
                user_account.user_account_id,
            )
        quiz_result = BaseQuizResultSchema(
            quiz_result_id=uuid4(),
            quiz_item_id=quiz_item_entity.quiz_item_id,
            user_account_id=user_account.user_account_id,
            percent=right_answer_percent,
        )
        await quiz_result_service.create(quiz_result.to_entity())

        keyboard_builder = ResourceQuizFinalKeyboardBuilder(i18n=i18n, item=resource_item_entity, page=0)
        keyboard = keyboard_builder.build()
        await callback.message.answer(
            text=i18n.get("start-quiz-final", percent=right_answer_percent),
            reply_markup=keyboard,
        )
