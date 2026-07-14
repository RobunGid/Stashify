from uuid import uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.exceptions.quiz_item import QuizItemNotFoundException
from application.exceptions.resource_item import ResourceItemNotFoundException
from application.filters.user_role_filter import UserRoleFilter
from application.filters.valid_callback_filter import ValidCallbackFilter
from application.keyboards.manage_quizes import (
    BackToManageQuizesKeyboardBuilder,
    CreateQuizChooseResourceCallbackFactory,
    DeleteQuizChooseResourceCallbackFactory,
    DeleteQuizConfirmKeyboardBuilder,
    DeleteQuizConfirmResourceCallbackFactory,
    EditQuizQuestionChooseResourceCallbackFactory,
    FinishQuizConfirmKeyboardBuilder,
    QuizManageEntryKeyboardBuilder,
)
from application.schemas.quiz_item_schema import BaseQuizItemSchema
from application.schemas.quiz_option_schema import BaseQuizOptionSchema
from application.schemas.quiz_question_schema import (
    BaseQuizQuestionSchema,
)
from application.services.quiz_item import QuizItemService
from application.services.quiz_option import QuizOptionService
from application.services.quiz_question import QuizQuestionService
from application.services.resource_item import ResourceItemService
from dishka import FromDishka
from infrastructure.models.user_account import Role

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
    quiz_question_options = question_data[1:]
    quiz_item_id = state_data["quiz_item_id"]

    quiz_question_schema = BaseQuizQuestionSchema(
        quiz_question_id=uuid4(),
        image=message.photo[0].file_id if message.photo else None,
        quiz_item_id=quiz_item_id,
        text=question_text,
    )
    question_options_schemas = [
        BaseQuizOptionSchema(
            quiz_question_id=quiz_question_schema.quiz_question_id,
            is_right=quiz_question_option.startswith("!"),
            text=quiz_question_option[1:] if quiz_question_option.startswith("!") else quiz_question_option,
        )
        for quiz_question_option in quiz_question_options
    ]

    existing_questions = state_data.get("questions", [])
    existing_question_options = state_data.get("question_options", [])
    await state.update_data(
        questions=[*existing_questions, quiz_question_schema],
        question_options=[*existing_question_options, *question_options_schemas],
    )

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
    quiz_option_service: FromDishka[QuizOptionService],
    resource_item_service: FromDishka[ResourceItemService],
    message: Message,
):
    state_data = await state.get_data()

    quiz_question_schemas = state_data["questions"]
    quiz_option_schemas = state_data["question_options"]
    quiz_item_id = state_data["quiz_item_id"]
    resource_item_id = state_data["resource_item_id"]

    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if resource_item_entity is None:
        raise ResourceItemNotFoundException(resource_item_id)

    quiz_item_schema = BaseQuizItemSchema(quiz_item_id=quiz_item_id, resource_item_id=resource_item_id)

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await quiz_item_service.create(item=quiz_item_schema.to_entity())

    for quiz_question_schema in quiz_question_schemas:
        await quiz_question_service.create(quiz_question_schema.to_entity())

    for quiz_option_schema in quiz_option_schemas:
        await quiz_option_service.create(quiz_option_schema.to_entity())

    await message.answer(
        text=i18n.get(
            "manage-quizes-create-success",
            resource_name=resource_item_entity.name,
            question_count=len(quiz_question_schemas),
        ),
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
    resource_item_service: FromDishka[ResourceItemService],
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
    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if resource_item_entity is None:
        raise ResourceItemNotFoundException(resource_item_id)

    keyboard_builder = DeleteQuizConfirmKeyboardBuilder(i18n=i18n, resource_item_id=resource_item_id)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get("manage-quizes-edit-delete-confirm", name=resource_item_entity.name),
        reply_markup=keyboard,
    )


@router.callback_query(
    DeleteQuizConfirmResourceCallbackFactory.filter(),
    UserRoleFilter([Role.admin, Role.manager]),
    ValidCallbackFilter(),
)
async def delete_quiz_confirm_callback_handler(
    callback: CallbackQuery,
    callback_data: DeleteQuizConfirmResourceCallbackFactory,
    i18n: I18nContext,
    quiz_item_service: FromDishka[QuizItemService],
    resource_item_service: FromDishka[ResourceItemService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    resource_item_entity = await resource_item_service.get_one(resource_item_id)
    if not resource_item_entity:
        raise ResourceItemNotFoundException(resource_item_id)
    quiz_item_entity = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz_item_entity:
        raise QuizItemNotFoundException(resource_item_id)

    keyboard_builder = BackToManageQuizesKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await quiz_item_service.delete_by_id(item_id=quiz_item_entity.quiz_item_id)
    await message.answer(
        text=i18n.get("manage-quizes-delete-success", resource_name=resource_item_entity.name),
        reply_markup=keyboard,
    )
