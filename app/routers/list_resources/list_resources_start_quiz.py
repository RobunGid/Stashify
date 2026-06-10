from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram_i18n import I18nContext

from database.managers import QuizManager, QuizResultManager
from keyboards.resource_quizes import (
    ListResourcesQuizQuestionCallbackFactory,
    ResourceQuizFinalKeyboardBuilder,
    ResourceQuizQuestionKeyboardBuilder,
)
from keyboards.resources import (
    ListResourcesItemCallbackFactory,
    ResourceQuizConfirmKeyboardBuilder,
)
from schemas.quiz_result_schema import QuizResultWithoutUserAndQuizSchema
from settings.config import bot

from .router import router


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
    resource = state_data["resource"]
    state_data = await state.get_data()

    keyboard_builder = ResourceQuizConfirmKeyboardBuilder(i18n=i18n, current_item=resource)
    keyboard = keyboard_builder.build()

    await callback.message.answer(
        text=i18n.get(
            "list-resources-start-quiz-question",
        ).format(
            question_count=len(resource.quiz.questions),
            resource_name=resource.name,
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
    state_data = await state.get_data()
    quiz = await QuizManager.get_one(resource_item_id=resource_item_id)
    page = state_data["current_page"]
    await state.update_data(quiz=quiz)
    await state.update_data(quiz_answers=[])
    keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
        i18n=i18n,
        item=quiz.resource,
        question=quiz.questions[0],
        page=page,
        question_number=0,
    )
    keyboard = keyboard_builder.build()

    if quiz.questions[0].image:
        await callback.message.answer_photo(
            photo=quiz.questions[0].image,
            text=quiz.questions[0].text,
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer(text=quiz.questions[0].text, reply_markup=keyboard)


@router.callback_query(
    ListResourcesQuizQuestionCallbackFactory.filter(F.action == "answer"),
)
async def list_resource_quiz_question_answer(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesQuizQuestionCallbackFactory,
    i18n: I18nContext,
):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data:
        return
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    current_quiz_answers = state_data["quiz_answers"]
    resource = state_data["resource"]
    question_number = callback_data.question_number
    page = state_data["current_page"]

    if question_number + 1 < len(quiz.questions):
        keyboard_builder = ResourceQuizQuestionKeyboardBuilder(
            i18n=i18n,
            item=resource,
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
        resource = state_data["resource"]
        existing_quiz_result = await QuizResultManager.get_one(
            resource.resource_item_id,
            str(callback.from_user.id),
        )
        if existing_quiz_result:
            await QuizResultManager.delete(resource.resource_item_id, str(callback.from_user.id))
        quiz_result = QuizResultWithoutUserAndQuizSchema(
            quiz_result_id=UUID(),
            quiz_id=quiz.quiz_id,
            user_id=str(callback.from_user.id),
            percent=right_answer_percent,
        )
        await QuizResultManager.create(quiz_result)

        keyboard_builder = ResourceQuizFinalKeyboardBuilder(i18n=i18n, item=resource, page=page)
        keyboard = keyboard_builder.build()
        await callback.message.answer(
            text=i18n.get("start-quiz-final", percent=right_answer_percent),
            reply_markup=keyboard,
        )
