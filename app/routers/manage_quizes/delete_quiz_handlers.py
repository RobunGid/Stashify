from math import ceil
from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext
from constants import DELETE_QUIZ_CATEGORIES_ON_PAGE, DELETE_QUIZ_RESOURCES_ON_PAGE
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager, QuizManager, ResourceManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.manage_quizes.manage_quizes_delete_keyboard_confirm import (
    manage_quizes_delete_keyboard_confirm,
)
from keyboards.quizes import (
    DeleteQuizCategoryListKeyboardBuilder,
    DeleteQuizChooseCategoryCallbackFactory,
    DeleteQuizChooseResourceCallbackFactory,
    DeleteQuizResourceListKeyboardBuilder,
    ManageQuizesBackKeyboardBuilder,
)
from schemas.quiz_schema import QuizSchema
from settings.config import bot

from .router import router


class DeleteQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_item_id = State()
    category_id = State()
    confirm = State()


@router.callback_query(
    F.data == "delete_quiz",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many(has_resources=True, has_quizes=True)
    total_pages = ceil(len(categories) / DELETE_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = DeleteQuizCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(text=i18n.get("manage-quizes-delete-choose-category"), reply_markup=keyboard)


@router.callback_query(
    DeleteQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: DeleteQuizChooseCategoryCallbackFactory,
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
        (current_page - 1) * DELETE_QUIZ_CATEGORIES_ON_PAGE : current_page * (DELETE_QUIZ_CATEGORIES_ON_PAGE)
    ]
    total_pages = state_data["total_pages"]

    keyboard_builder = DeleteQuizCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        current_page=current_page,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-delete-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteQuizChooseCategoryCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_category_choose(
    callback: CallbackQuery,
    callback_data: DeleteQuizChooseCategoryCallbackFactory,
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
    resources = await ResourceManager.get_many(category_id=category_id, has_quiz=True)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources) / DELETE_QUIZ_RESOURCES_ON_PAGE)

    keyboard_builder = DeleteQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-delete-choose-resource",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteQuizChooseResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: DeleteQuizChooseResourceCallbackFactory,
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
        (current_page - 1) * DELETE_QUIZ_RESOURCES_ON_PAGE : current_page * (DELETE_QUIZ_RESOURCES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    keyboard_builder = DeleteQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(text=i18n.get("manage-quizes-delete-choose"), reply_markup=keyboard)


@router.callback_query(
    DeleteQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_choose(
    callback: CallbackQuery,
    callback_data: DeleteQuizChooseResourceCallbackFactory,
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
    if not resource_item_id:
        return
    state_data = await state.get_data()

    quiz_resource = next(
        resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id
    )
    quiz = QuizSchema(
        quiz_id=UUID(),
        resource_item_id=resource_item_id,
        questions=[],
        resource=quiz_resource,
    )
    await state.update_data(quiz=quiz, questions=[], resource_item_id=resource_item_id)
    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-delete-choose-to-delete",
            callback.from_user.language_code,
        ),
        reply_markup=manage_quizes_delete_keyboard_confirm(
            user_lang=callback.from_user.language_code,
        ),
    )


@router.callback_query(
    F.data == "delete_quiz_confirm",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_confirm(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    resource = next(resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id)

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await QuizManager.delete(resource_item_id=state_data["resource_item_id"])
    except IntegrityError, ValueError:
        await callback.message.answer(
            text=i18n.get("manage-quizes-delete-fail", resource_name=resource.name),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=i18n.get("manage-quizes-delete-success", resource_name=resource.name),
            reply_markup=keyboard,
        )
