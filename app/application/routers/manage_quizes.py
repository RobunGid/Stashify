from uuid import uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.exceptions.resource_item import ResourceItemNotFoundException
from application.filters.user_role_filter import UserRoleFilter
from application.filters.valid_callback_filter import ValidCallbackFilter
from application.filters_schemas.quiz_question import QuizQuestionFiltersSchema
from application.keyboards.manage_quizes import (
    BackToManageQuizesKeyboardBuilder,
    CreateQuizChooseResourceCallbackFactory,
    DeleteQuizChooseResourceCallbackFactory,
    EditQuizQuestionChooseResourceCallbackFactory,
    FinishQuizConfirmKeyboardBuilder,
    QuizManageEntryKeyboardBuilder,
)
from application.schemas.quiz_item_schema import BaseQuizItemSchema
from application.schemas.quiz_question_schema import (
    BaseQuizQuestionSchema,
)
from application.services.quiz_item import QuizItemService
from application.services.quiz_question import QuizQuestionService
from application.services.resource_item import ResourceItemService
from dishka import FromDishka
from infrastructure.models.user_account import Role
from sqlalchemy.exc import IntegrityError

from settings.aiogram import bot

router = Router()


@router.callback_query(F.data == "manage_quizes", UserRoleFilter([Role.admin, Role.manager]), ValidCallbackFilter())
async def manage_quizes_entry_callback_handler(callback: CallbackQuery, i18n: I18nContext, message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )

    keyboard_builder = QuizManageEntryKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-text",
        ),
        reply_markup=keyboard,
    )


class CreateQuizState(StatesGroup):
    name = State()
    description = State()
    image = State()
    tags = State()
    quiz = State()
    questions = State()


@router.callback_query(
    CreateQuizChooseResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
    ValidCallbackFilter(),
)
async def create_quiz_callback_handler(
    callback: CallbackQuery,
    callback_data: CreateQuizChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
    message: Message,
    service: FromDishka[ResourceItemService],
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    if not resource_item_id:
        return

    resource_item_id = callback_data.resource_item_id
    if not resource_item_id:
        return
    resource_item_entity = await service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)
    await state.update_data(resource_item_id=resource_item_id, quiz_item_id=uuid4())

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-create-send-question",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateQuizState.questions)


@router.message(CreateQuizState.questions, UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_add_question(message: Message, state: FSMContext, i18n: I18nContext):
    state_data = await state.get_data()

    question_data = message.html_text.split("\n")
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith("!")]
    quiz_item_id = state_data["quiz_item_id"]

    question = BaseQuizQuestionSchema(
        quiz_question_id=uuid4(),
        image=message.photo[0].file_id if message.photo else None,
        options=question_options,
        quiz_item_id=quiz_item_id,
        right_options=right_options,
        text=question_text,
    )

    existing_questions = state_data.get("questions", [])
    await state.update_data(questions=[*existing_questions, question])

    keyboard_builder = FinishQuizConfirmKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-create-add-question",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateQuizState.questions)


@router.callback_query(
    F.data == "finish_quiz_confirm",
    UserRoleFilter([Role.admin, Role.manager]),
    ValidCallbackFilter(),
)
async def create_quiz_finish_callback_handler(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    quiz_item_service: FromDishka[QuizItemService],
    quiz_question_service: FromDishka[QuizQuestionService],
    resource_item_service: FromDishka[ResourceItemService],
    message: Message,
):
    state_data = await state.get_data()

    quiz_questions = state_data["questions"]
    quiz_item_id = state_data["quiz_item_id"]
    resource_item_id = state_data["resource_item_id"]

    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if resource_item_entity is None:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item_schema = BaseQuizItemSchema(quiz_item_id=quiz_item_id, resource_item_id=resource_item_id)
    quiz_questions_schemas = [
        BaseQuizQuestionSchema(
            quiz_question_id=uuid4(),
            text=quiz_question.text,
            quiz_item_id=quiz_item_id,
            options=quiz_question.options,
            right_options=quiz_question.right_options,
            image=quiz_question.image,
        )
        for quiz_question in quiz_questions
    ]

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await quiz_item_service.create(item=quiz_item_schema.to_entity())

    for quiz_question_schema in quiz_questions_schemas:
        await quiz_question_service.create(quiz_question_schema.to_entity())

    await message.answer(
        text=i18n.get(
            "manage-quizes-create-success",
            resource_name=resource_item_entity.name,
            question_count=len(quiz_questions),
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == "delete_quiz_confirm",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizItemService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    resource = next(resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id)

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await service.delete_by_id(item_id=state_data["resource_item_id"])
    except IntegrityError, ValueError:
        await message.answer(
            text=i18n.get("manage-quizes-delete-fail", resource_name=resource.name),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get("manage-quizes-delete-success", resource_name=resource.name),
            reply_markup=keyboard,
        )


@router.callback_query(
    EditQuizQuestionChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_choose(
    callback: CallbackQuery,
    callback_data: EditQuizQuestionChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    await state.update_data(resource_item_id=resource_item_id)

    keyboard_builder = QuizManageEntryKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage_quizes.edit.choose_to_change",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteQuizChooseResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
    ValidCallbackFilter(),
)
async def delete_quiz_callback_handler(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
    message: Message,
    callback_data: DeleteQuizChooseResourceCallbackFactory,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    if resource_item_id is None:
        return
    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_id)
    quiz_questions, _ = await service.get_many(filters.to_entity())

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get("manage-quizes-edit-delete-confirm"),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateQuizChooseResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
    ValidCallbackFilter(),
)
async def edit_resource_add_question(
    callback: CallbackQuery,
    callback_data: CreateQuizChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await state.get_data()
    resource_item_id = callback_data.resource_item_id
    if not resource_item_id:
        return
    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_id)
    quiz_question_enttiies, _ = await service.get_many(filters.to_entity())

    formatted_questions = ""

    for index, question in enumerate(quiz_question_enttiies):
        formatted_question = f"{index + 1}. {question.text}\n"

        for option in question.options:
            if index in question.right_options:
                formatted_question += f"!{option}\n"
            else:
                formatted_question += f"{option}\n"

        formatted_questions += formatted_question + "\n"

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get("manage-quizes-edit-add-question-text", questions=formatted_questions),
        reply_markup=keyboard,
    )
