from math import ceil
from uuid import UUID, uuid4

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_i18n import I18nContext
from constants import (
    CREATE_QUIZ_CATEGORIES_ON_PAGE,
    CREATE_QUIZ_RESOURCES_ON_PAGE,
    DELETE_QUIZ_CATEGORIES_ON_PAGE,
    DELETE_QUIZ_RESOURCES_ON_PAGE,
    EDIT_QUIZ_CATEGORIES_ON_PAGE,
    EDIT_QUIZ_RESOURCES_ON_PAGE,
)
from sqlalchemy.exc import IntegrityError

from database.managers import CategoryManager, QuizManager, QuizQuestionManager, ResourceManager
from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from keyboards.quizes import (
    CreateQuizCategoryListKeyboardBuilder,
    CreateQuizChooseCategoryCallbackFactory,
    CreateQuizChooseResourceCallbackFactory,
    CreateQuizResourceListKeyboardBuilder,
    DeleteQuizCategoryListKeyboardBuilder,
    DeleteQuizChooseCategoryCallbackFactory,
    DeleteQuizChooseResourceCallbackFactory,
    DeleteQuizConfirmKeyboardBuilder,
    DeleteQuizResourceListKeyboardBuilder,
    EditQuizActionCallbackFactory,
    EditQuizCategoryListKeyboardBuilder,
    EditQuizChooseCategoryCallbackFactory,
    EditQuizChooseResourceCallbackFactory,
    EditQuizResourceListKeyboardBuilder,
    ManageQuizesBackKeyboardBuilder,
    QuizConfirmFinishKeyboardBuilder,
    QuizManageEntryKeyboardBuilder,
)
from schemas.quiz_question_schema import QuizQuestionBaseSchema, QuizQuestionSchema
from schemas.quiz_schema import QuizSchema
from settings.config import bot

router = Router()


@router.callback_query(
    F.data == "manage_quizes",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def manage_quizes(callback: CallbackQuery, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    keyboard_builder = QuizManageEntryKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-text",
        ),
        reply_markup=keyboard,
    )


class CreateQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_item_id = State()
    category_id = State()
    name = State()
    description = State()
    image = State()
    tags = State()
    quiz = State()
    questions = State()


@router.callback_query(
    F.data == "create_quiz",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many()
    total_pages = ceil(len(categories) / CREATE_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = CreateQuizCategoryListKeyboardBuilder(
        current_page=1,
        items=categories,
        i18n=i18n,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes.create.choose_category",
            callback.from_user.language_code,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CreateQuizChooseCategoryCallbackFactory,
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
        (current_page - 1) * CREATE_QUIZ_CATEGORIES_ON_PAGE : current_page * (CREATE_QUIZ_CATEGORIES_ON_PAGE)
    ]
    total_pages = state_data["total_pages"]

    keyboard_builder = CreateQuizCategoryListKeyboardBuilder(
        i18n=i18n,
        total_pages=total_pages,
        current_page=current_page,
        items=categories,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-create-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateQuizChooseCategoryCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_category_choose(
    callback: CallbackQuery,
    callback_data: CreateQuizChooseCategoryCallbackFactory,
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
    resources = await ResourceManager.get_many(category_id=category_id, has_quiz=False)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources) / CREATE_QUIZ_RESOURCES_ON_PAGE)

    await state.update_data(category_id=category_id)

    keyboard_builder = CreateQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage_quizes-create-choose",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateQuizChooseResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CreateQuizChooseResourceCallbackFactory,
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
        (current_page - 1) * CREATE_QUIZ_RESOURCES_ON_PAGE : current_page * (CREATE_QUIZ_RESOURCES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    keyboard_builder = CreateQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        total_pages=total_pages,
        current_page=current_page,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-create-choose",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    CreateQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def create_quiz_choose(
    callback: CallbackQuery,
    callback_data: CreateQuizChooseResourceCallbackFactory,
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
    state_data = await state.get_data()
    if not resource_item_id:
        return

    quiz_resource = next(
        resource for resource in state_data["resources"] if resource.resource_item_id == resource_item_id
    )
    quiz = QuizSchema(
        quiz_id=uuid4(),
        resource_item_id=resource_item_id,
        questions=[],
        resource=quiz_resource,
    )
    await state.update_data(quiz=quiz, questions=[], resource_item_id=resource_item_id)

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-create-send-question",
        ),
        reply_markup=keyboard,
    )
    await state.set_state(CreateQuizState.questions)


@router.message(CreateQuizState.questions, UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_add_question(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code:
        return

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
        quiz_id=state_data["quiz"].id,
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
async def create_quiz_finish(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return

    state_data = await state.get_data()
    quiz = state_data["quiz"]
    quiz_questions = state_data["questions"]
    quiz.questions = quiz_questions

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await QuizManager.create(quiz)
    except IntegrityError:
        await callback.message.answer(
            text=i18n.get(
                "manage-quizes-create-fail",
                resource_name=quiz.resource.name,
                question_count=len(quiz_questions),
            ),
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(
            text=i18n.get(
                "manage-quizes-create-success",
                resource_name=quiz.resource.name,
                question_count=len(quiz_questions),
            ),
            reply_markup=keyboard,
        )


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
        quiz_id=uuid4(),
        resource_item_id=resource_item_id,
        questions=[],
        resource=quiz_resource,
    )
    await state.update_data(quiz=quiz, questions=[], resource_item_id=resource_item_id)

    keyboard_builder = DeleteQuizConfirmKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-delete-choose-to-delete",
        ),
        reply_markup=keyboard,
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


class EditQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_item_id = State()
    delete_question_number = State()
    edit_question_number = State()
    new_question_text = State()
    edit_question_text = State()


@router.callback_query(
    F.data == "edit_quiz",
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_quiz_callback_handler(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )

    categories = await CategoryManager.get_many(has_quizes=True)
    total_pages = ceil(len(categories) / EDIT_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)

    keyboard_builder = EditQuizCategoryListKeyboardBuilder(
        i18n=i18n,
        total_pages=total_pages,
        current_page=1,
        items=categories,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-edit-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_quiz_category_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: EditQuizChooseResourceCallbackFactory,
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
        (current_page - 1) * EDIT_QUIZ_CATEGORIES_ON_PAGE : current_page * (EDIT_QUIZ_CATEGORIES_ON_PAGE)
    ]
    total_pages = state_data["total_pages"]

    keyboard_builder = EditQuizCategoryListKeyboardBuilder(
        i18n=i18n,
        items=categories,
        total_pages=total_pages,
        current_page=current_page,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage-quizes-edit-choose-category",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditQuizChooseCategoryCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_quizes_category_choose(
    callback: CallbackQuery,
    callback_data: EditQuizChooseCategoryCallbackFactory,
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
    total_pages = ceil(len(resources) / EDIT_QUIZ_RESOURCES_ON_PAGE)

    await state.update_data(category_id=category_id)

    keyboard_builder = EditQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=1,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get("manage_quizes.edit.choose_to_change", callback.from_user.language_code),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditQuizChooseResourceCallbackFactory.filter(F.action == "change_page"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_quiz_page(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: EditQuizChooseResourceCallbackFactory,
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
        (current_page - 1) * EDIT_QUIZ_RESOURCES_ON_PAGE : current_page * (EDIT_QUIZ_RESOURCES_ON_PAGE)
    ]
    total_pages = resources_data["total_pages"]

    keyboard_builder = EditQuizResourceListKeyboardBuilder(
        i18n=i18n,
        items=resources,
        current_page=current_page,
        total_pages=total_pages,
    )
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage_quizes.edit.choose",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditQuizChooseResourceCallbackFactory.filter(F.action == "select"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_choose(
    callback: CallbackQuery,
    callback_data: EditQuizChooseResourceCallbackFactory,
    state: FSMContext,
    i18n: I18nContext,
):
    if (
        not callback_data.resource_item_id
        or not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource_item_id = callback_data.resource_item_id
    await state.update_data(resource_item_id=resource_item_id)

    keyboard_builder = QuizManageEntryKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "manage_quizes.edit.choose_to_change",
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    EditQuizActionCallbackFactory.filter(F.action == "delete"),
    UserRoleFilter([Role.admin, Role.manager]),
)
async def edit_resource_delete_question(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    quiz_questions = await QuizQuestionManager.get_many(resource_item_id=resource_item_id)

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

    await callback.message.answer(
        text=i18n.get("manage-quizes-edit-delete-question-number", questions=formatted_questions),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.delete_question_number)


@router.message(
    EditQuizState.delete_question_number,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def delete_question_confirm(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code or not message or not message.text:
        return
    state_data = await state.get_data()
    resource_item_id = str(state_data["resource_item_id"])
    quiz_question_number = int(message.text) - 1

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await QuizQuestionManager.delete(
            resource_item_id=resource_item_id,
            quiz_question_number=quiz_question_number,
            quiz_question_id=None,
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
async def edit_resource_add_question(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    quiz_questions = await QuizQuestionManager.get_many(resource_item_id=resource_item_id)

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

    await callback.message.answer(
        text=i18n.get("manage-quizes-edit-add-question-text", questions=formatted_questions),
        reply_markup=keyboard,
    )
    await state.set_state(EditQuizState.new_question_text)


@router.message(
    EditQuizState.new_question_text,
    F.text,
    UserRoleFilter([Role.admin, Role.manager]),
)
async def add_question_confirm(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code or not message or not message.text:
        return
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    quiz = await QuizManager.get_one(resource_item_id=resource_item_id)
    quiz_id = UUID(str(quiz.quiz_id))
    question_data = message.html_text.split("\n")
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith("!")]

    question = QuizQuestionBaseSchema(
        quiz_question_id=uuid4(),
        quiz_id=quiz_id,
        image=message.photo[0].file_id if message.photo else None,
        options=question_options,
        right_options=right_options,
        text=question_text,
    )

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    try:
        await QuizQuestionManager.create(quiz_question_data=question)
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
async def edit_resource_edit_question(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    state_data = await state.get_data()
    resource_item_id = state_data["resource_item_id"]
    quiz_questions = await QuizQuestionManager.get_many(resource_item_id=resource_item_id)

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

    await callback.message.answer(
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
    if not message.from_user or not message.from_user.language_code or not message or not message.text:
        return
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
async def edit_question_text(message: Message, state: FSMContext, i18n: I18nContext):
    if not message.from_user or not message.from_user.language_code or not message or not message.text:
        return
    state_data = await state.get_data()
    question_number = int(state_data["edit_question_number"])
    resource_item_id = state_data["resource_item_id"]
    questions = await QuizQuestionManager.get_many(resource_item_id)
    question_id = questions[question_number].quiz_question_id
    quiz = await QuizManager.get_one(resource_item_id=resource_item_id)
    quiz_id = UUID(str(quiz.quiz_id))
    question_data = message.html_text.split("\n")
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith("!")]

    question = QuizQuestionBaseSchema(
        quiz_question_id=question_id,
        quiz_id=quiz_id,
        image=message.photo[0].file_id if message.photo else None,
        options=question_options,
        right_options=right_options,
        text=question_text,
    )

    keyboard_builder = ManageQuizesBackKeyboardBuilder(i18n=i18n)
    keyboard = keyboard_builder.build()

    await QuizQuestionManager.update(quiz_question_data=question)
    await message.answer(
        text=i18n.get(
            "manage_quizes.edit.edit_question.fail",
        ),
        reply_markup=keyboard,
    )
