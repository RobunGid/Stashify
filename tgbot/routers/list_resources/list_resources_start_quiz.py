from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.list_resources.list_resources_start_quiz_confirm_keyboard import list_resources_start_quiz_confirm_keyboard
from database.operations.get_quiz import get_quiz
from keyboards.list_resources.list_resources_quiz_question_keyboard import ListResourcesQuizQuestionCallbackFactory, list_resources_quiz_question_keyboard
from database.operations.get_resource import get_resource
from .router import router
from config.bot_config import bot
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory
from i18n.translate import t

@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="start_quiz"))
async def list_resource_start_quiz(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id): return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    resource_id = callback_data.resource_id
    resource = await get_resource(resource_id=resource_id)
    
    await callback.message.answer(
        text=t("list_resources.start_quiz.question".format(question_count=len(resource.quiz.questions), resource_name=resource.name), callback.from_user.language_code), 
        reply_markup=list_resources_start_quiz_confirm_keyboard(user_lang=callback.from_user.language_code)
    )
    
@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="start_quiz_confirm"))
async def list_resource_start_quiz_confirm(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id or 
        not callback_data.rating): return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_id = state_data["resource_id"]
    quiz = await get_quiz(resource_id=resource_id)
    await state.update_data(quiz=quiz)
    await state.update_data(quiz_answers=[])
    if quiz.questions[0].image:
        await callback.message.answer_photo(
            photo=quiz.questions[0].image,
            text=quiz.questions[0].text, 
            reply_markup=list_resources_quiz_question_keyboard(question=quiz.questions[0], question_number=0)
        )
    else:
        await callback.message.answer(
            text=quiz.questions[0].text, 
            reply_markup=list_resources_quiz_question_keyboard(question=quiz.questions[0], question_number=0)
        )
        
@router.callback_query(ListResourcesQuizQuestionCallbackFactory.filter(F.action=="answer"))
async def list_resource_quiz_question_answer(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesQuizQuestionCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data): return
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    current_quiz_answers = state_data["quiz_answers"]
    question_number = callback_data.question_number
    await state.update_data(quiz_answers=current_quiz_answers+[callback_data.option_number])
    if quiz.questions[question_number+1].image:
        await callback.message.answer_photo(
            photo=quiz.questions[question_number+1].image,
            text=quiz.questions[question_number+1].text, 
            reply_markup=list_resources_quiz_question_keyboard(question=quiz.questions[question_number+1], question_number=question_number+1)
        )
    else:
        await callback.message.answer(
            text=quiz.questions[question_number+1].text, 
            reply_markup=list_resources_quiz_question_keyboard(question=quiz.questions[question_number+1], question_number=question_number+1)
        )