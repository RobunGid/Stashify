from uuid import uuid4
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.list_resources.list_resources_start_quiz_confirm_keyboard import list_resources_start_quiz_confirm_keyboard
from keyboards.list_resources.list_resources_quiz_question_keyboard import ListResourcesQuizQuestionCallbackFactory, list_resources_quiz_question_keyboard
from keyboards.list_resources.list_resources_quiz_final_keyboard import list_resources_quiz_final_keyboard
from schemas.quiz_result_schema import QuizResultSchema
from .router import router
from config.bot_config import bot
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory
from i18n.translate import t
from database.managers import QuizManager
from database.managers import QuizResultManager

@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="start_quiz"))
async def list_resource_start_quiz(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id): 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    state_data = await state.get_data()
    resource = state_data["resource"]
    state_data = await state.get_data()
    page = state_data["current_page"]
    
    await callback.message.answer(
        text=t("list_resources.start_quiz.question", lang=callback.from_user.language_code).format(question_count=len(resource.quiz.questions), resource_name=resource.name), 
        reply_markup=list_resources_start_quiz_confirm_keyboard(user_lang=callback.from_user.language_code, resource_id=resource.id, page=page)
    )
    
@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="start_quiz_cnfrm"))
async def list_resource_start_quiz_confirm(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id): 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    state_data = await state.get_data()
    quiz = await QuizManager.get_one(resource_id=resource_id)
    page = state_data["current_page"]
    await state.update_data(quiz=quiz)
    await state.update_data(quiz_answers=[])
    if quiz.questions[0].image:
        await callback.message.answer_photo(
            photo=quiz.questions[0].image,
            text=quiz.questions[0].text, 
            reply_markup=list_resources_quiz_question_keyboard(
                question=quiz.questions[0], 
                question_number=0,
                page=page,
                resource_id=resource_id,
                user_lang=callback.from_user.language_code
            )
        )
    else:
        await callback.message.answer(
            text=quiz.questions[0].text, 
            reply_markup=list_resources_quiz_question_keyboard(
                question=quiz.questions[0], 
                question_number=0,
                page=page,
                resource_id=resource_id
            )
        )
        
@router.callback_query(ListResourcesQuizQuestionCallbackFactory.filter(F.action=="answer"))
async def list_resource_quiz_question_answer(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesQuizQuestionCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data): 
        return
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    current_quiz_answers = state_data["quiz_answers"]
    resource = state_data["resource"]
    question_number = callback_data.question_number
    page = state_data["current_page"]
    
    if question_number+1 < len(quiz.questions):
        await state.update_data(quiz_answers=current_quiz_answers+[callback_data.option_number])
        if quiz.questions[question_number+1].image:
            await callback.message.answer_photo(
                photo=quiz.questions[question_number+1].image,
                text=quiz.questions[question_number+1].text, 
                reply_markup=list_resources_quiz_question_keyboard(
                    question=quiz.questions[question_number+1], 
                    question_number=question_number+1,
                    page=page,
                    resource_id=resource.id,
                    user_lang=callback.from_user.language_code
                    
                    )
            )
        else:
            await callback.message.answer(
                text=quiz.questions[question_number+1].text, 
                reply_markup=list_resources_quiz_question_keyboard(
                    question=quiz.questions[question_number+1], 
                    question_number=question_number+1,
                    resource_id=resource.id,
                    page=page,
                    user_lang=callback.from_user.language_code
                    )
            )
    else:
        quiz_answers = current_quiz_answers+[callback_data.option_number]
        right_answers = [question.right_options for question in quiz.questions]
        right_answers_len = len([quiz_answers[i] for i in range(len(quiz_answers)) if quiz_answers[i] in right_answers[i]])
        right_answer_percent = int(100 * right_answers_len / len(quiz_answers))
        
        state_data = await state.get_data()
        resource = state_data["resource"]
        existing_quiz_result = QuizResultManager.get_one(resource.id)
        if existing_quiz_result:
            await QuizResultManager.delete(resource.id, str(callback.from_user.id))
        quiz_result = QuizResultSchema(id=uuid4(), quiz=quiz, quiz_id=quiz.id, user_id=str(callback.from_user.id), percent=right_answer_percent)
        await QuizResultManager.create(quiz_result)
        
        await callback.message.answer(
            text=t("start_quiz.final", lang=callback.from_user.language_code).format(percent=right_answer_percent),
            reply_markup=list_resources_quiz_final_keyboard(user_lang=callback.from_user.language_code, resource_id=resource.id, page=page)
        )