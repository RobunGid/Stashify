from uuid import UUID, uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from application.exceptions.quiz_item import QuizItemNotFoundException
from application.filters.user_role_filter import UserRoleFilter
from application.filters.valid_callback_filter import ValidCallbackFilter
from application.filters_schemas.quiz_question import QuizQuestionFiltersSchema
from application.keyboards.quizes import (
    CreateQuizChooseResourceCallbackFactory,
    DeleteQuizChooseResourceCallbackFactory,
    DeleteQuizConfirmKeyboardBuilder,
    EditQuizActionCallbackFactory,
    EditQuizChooseResourceCallbackFactory,
    ManageQuizesBackKeyboardBuilder,
    QuizConfirmFinishKeyboardBuilder,
    QuizManageEntryKeyboardBuilder,
)
from application.schemas.quiz_item_schema import BaseQuizItemSchema, QuizSchema
from application.schemas.quiz_question_schema import (
    BaseQuizQuestionSchema,
    QuizQuestionSchema,
    QuizQuestionUpdateSchema,
)
from application.services.quiz_item import QuizItemService
from application.services.quiz_question import QuizQuestionService
from dishka import FromDishka
from infrastructure.models.user_account import Role
from sqlalchemy.exc import IntegrityError

from settings.aiogram import bot

router = Router()
router.callback_query.filter(ValidCallbackFilter())


@router.callback_query(
    F.data == "manage_quizes",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def manage_quizes(callback: CallbackQuery, i18n: I18nContext, message: Message):
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
    resource_item_id = State()
    name = State()
    description = State()
    image = State()
    tags = State()
    quiz = State()
    questions = State()


@router.callback_query(
    CreateQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_choose(
    callback: CallbackQuery,
    callback_data: CreateQuizChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    state_data = await state.get_data()
    if not resource_item_id:
        return

    quiz_resource = next(
        resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id
    )
    quiz = QuizSchema(
        quiz_item_id=uuid4(),
        resource_item_id=resource_item_id,
        questions=[],
        resource=quiz_resource,
    )
    await state.update_data(quiz=quiz, questions=[], resource_item_id=resource_item_id)

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
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

    question = QuizQuestionSchema(
        quiz_question_id=uuid4(),
        image=message.photo[0].file_id if message.photo else None,
        quiz=state_data["quiz"],
        options=question_options,
        quiz_item_id=state_data["quiz"].id,
        right_options=right_options,
        text=question_text,
    )

    await state.update_data(questions=[*state_data["questions"], question])
    await state.set_state(CreateQuizState.questions)

    keyboard_builder = QuizConfirmFinishKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-create-add-question",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == "manage_quizes.stop",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_finish(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizItemService],
    message: Message,
):
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    quiz_questions = state_data["questions"]
    quiz.questions = quiz_questions

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await service.create(item=quiz)
    except IntegrityError:
        await message.answer(
            text=i18n.get(
                "manage-quizes-create-fail",
                resource_name=quiz.resource.name,
                question_count=len(quiz_questions),
            ),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get(
                "manage-quizes-create-success",
                resource_name=quiz.resource.name,
                question_count=len(quiz_questions),
            ),
            reply_markup=keyboard,
        )


class DeleteQuizState(StatesGroup):
    resource_item_id = State()
    category_item_id = State()
    confirm = State()


@router.callback_query(
    DeleteQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_quiz_choose(
    callback: CallbackQuery,
    callback_data: DeleteQuizChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    if not resource_item_id:
        return

    quiz = BaseQuizItemSchema(
        quiz_item_id=uuid4(),
        resource_item_id=resource_item_id,
    )
    await state.update_data(quiz=quiz, questions=[], resource_item_id=resource_item_id)

    keyboard_builder = DeleteQuizConfirmKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-delete-choose-to-delete",
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

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
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


class EditQuizState(StatesGroup):
    resource_item_id = State()
    delete_question_number = State()
    edit_question_number = State()
    new_question_text = State()
    edit_question_text = State()


@router.callback_query(
    EditQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_choose(
    callback: CallbackQuery,
    callback_data: EditQuizChooseResourceCallbackFactory,
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
    EditQuizActionCallbackFactory.filter(F.action == "delete"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_delete_question(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_id)
    quiz_questions, _ = await service.get_many(filters.to_entity())

    formatted_questions = ""

    for index, question in enumerate(quiz_questions):
        formatted_question = f"{index + 1}. {question.text}\n"

        for option in question.options:
            if index in question.right_options:
                formatted_question += f"!{option}\n"
            else:
                formatted_question += f"{option}\n"

        formatted_questions += formatted_question + "\n"

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get("manage-quizes-edit-delete-question-number", questions=formatted_questions),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.delete_question_number)


@router.message(
    EditQuizState.delete_question_number,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_question_confirm(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
):
    state_data = await state.get_data()
    resource_item_id = UUID(state_data["resource_item_id"])
    quiz_question_number = int(message.text or "1") - 1

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await service.delete_by_question_number(
            resource_item_id=resource_item_id,
            quiz_question_number=quiz_question_number,
        )
    except IntegrityError:
        await message.answer(
            text=i18n.get(
                "manage-quizes-edit-delete-question-fail",
            ),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get(
                "manage-quizes-edit-delete-question-success",
            ),
            reply_markup=keyboard,
        )
    finally:
        await state.clear()


@router.callback_query(
    EditQuizActionCallbackFactory.filter(F.action == "add"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_add_question(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
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

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get("manage-quizes-edit-add-question-text", questions=formatted_questions),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.new_question_text)


@router.message(
    EditQuizState.new_question_text,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def add_question_confirm(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    quiz_item_service: FromDishka[QuizItemService],
    quiz_question_service: FromDishka[QuizQuestionService],
):
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    quiz_item_entity = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz_item_entity:
        raise QuizItemNotFoundException(resource_item_id)

    quiz_item_id = UUID(str(quiz_item_entity.quiz_item_id))
    question_data = message.html_text.split("\n")
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith("!")]

    question = BaseQuizQuestionSchema(
        quiz_question_id=uuid4(),
        quiz_item_id=quiz_item_id,
        image=message.photo[0].file_id if message.photo else None,
        options=question_options,
        right_options=right_options,
        text=question_text,
    )

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await quiz_question_service.create(question.to_entity())
    except IntegrityError:
        await message.answer(
            text=i18n.get(
                "manage-quizes-edit-add-question-fail",
            ),
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=i18n.get(
                "manage-quizes-edit-add-question-success",
            ),
            reply_markup=keyboard,
        )
    finally:
        await state.clear()


@router.callback_query(
    EditQuizActionCallbackFactory.filter(F.action == "edit"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_edit_question(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    service: FromDishka[QuizQuestionService],
    message: Message,
):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_id)
    quiz_questions, _ = await service.get_many(filters.to_entity())

    formatted_questions = ""

    for index, question in enumerate(quiz_questions):
        formatted_question = f"{index + 1}. {question.text}\n"

        for option in question.options:
            if index in question.right_options:
                formatted_question += f"!{option}\n"
            else:
                formatted_question += f"{option}\n"

        formatted_questions += formatted_question + "\n"

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage-quizes-edit-edit-question-number",
            callback.from_user.language_code,
            questions=formatted_questions,
        ),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.edit_question_number)


@router.message(
    EditQuizState.edit_question_number,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_question_number(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(edit_question_number=message.text)

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await message.answer(
        text=i18n.get(
            "manage_quizes.edit.edit_question.text",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.edit_question_text)


@router.message(
    EditQuizState.edit_question_text,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_question_text(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    quiz_question_service: FromDishka[QuizQuestionService],
    quiz_item_service: FromDishka[QuizItemService],
):
    state_data = await state.get_data()
    question_number = int(state_data["edit_question_number"])
    resource_item_id = state_data["resource_item_id"]
    filters = QuizQuestionFiltersSchema(resource_item_id=resource_item_id)
    questions, _ = await quiz_question_service.get_many(filters.to_entity())
    question_id = questions[question_number].quiz_question_id
    quiz = await quiz_item_service.get_one_by_resource_item_id(resource_item_id)
    if not quiz:
        raise QuizItemNotFoundException(resource_item_id)
    question_data = message.html_text.split("\n")
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith("!")]

    question = QuizQuestionUpdateSchema(
        image=message.photo[0].file_id if message.photo else None,
        options=question_options,
        right_options=right_options,
        text=question_text,
    )

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await quiz_question_service.update(question_id, question.to_entity())
    await message.answer(
        text=i18n.get(
            "manage_quizes.edit.edit_question.fail",
        ),
        reply_markup=keyboard,
    )
