from math import ceil
from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_quizes.manage_quizes_create_resource_list_keyboard import manage_quizes_create_resource_list_keyboard, CreateQuizChooseResourceCallbackFactory
from keyboards.manage_quizes.manage_quizes_create_category_list_keyboard import manage_quizes_create_category_list_keyboard, CreateQuizChooseCategoryCallbackFactory
from config.bot_config import bot
from config.var_config import CREATE_QUIZ_RESOURCES_ON_PAGE, CREATE_QUIZ_CATEGORIES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.get_categories import get_categories
from keyboards.manage_quizes.manage_quizes_back_keyboard import manage_quizes_back_keyboard
from schemas.quiz_question_schema import QuizQuestionSchema
from schemas.quiz_schema import QuizSchema
from keyboards.manage_quizes.manage_quizes_add_question_keyboard import manage_quizes_add_question_keyboard
from database.operations.create_quiz import create_quiz
from .router import router

class CreateQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_id = State()
    category_id = State()
    name = State()
    description = State()
    image = State()
    tags = State()
    quiz = State()
    questions = State()

@router.callback_query(F.data=="create_quiz", UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages = ceil(len(categories) / CREATE_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_quizes.create.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_create_category_list_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    
@router.callback_query(CreateQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_category_page(callback: CallbackQuery, state: FSMContext, callback_data: CreateQuizChooseCategoryCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    state_data = await state.get_data()
    categories = state_data["categories"][(current_page-1)*CREATE_QUIZ_CATEGORIES_ON_PAGE:current_page*(CREATE_QUIZ_CATEGORIES_ON_PAGE)]
    total_pages = state_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.create.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_create_category_list_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(CreateQuizChooseCategoryCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_category_choose(callback: CallbackQuery, callback_data: CreateQuizChooseCategoryCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    category_id = callback_data.category_id
    resources = await get_resources(category_id=category_id, has_quiz=False)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources)/CREATE_QUIZ_RESOURCES_ON_PAGE)
    
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text=t("manage_quizes.create.choose", callback.from_user.language_code),
        reply_markup=manage_quizes_create_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=1)
    )
    
@router.callback_query(CreateQuizChooseResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_page(callback: CallbackQuery, state: FSMContext, callback_data: CreateQuizChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*CREATE_QUIZ_RESOURCES_ON_PAGE:current_page*(CREATE_QUIZ_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.create.choose", callback.from_user.language_code), 
        reply_markup=manage_quizes_create_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(CreateQuizChooseResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_choose(callback: CallbackQuery, callback_data: CreateQuizChooseResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    state_data = await state.get_data()
    
    quiz_resource = next((resource for resource in state_data["resources"] if resource.id == resource_id))
    quiz = QuizSchema(id=uuid4(), resource_id=resource_id, questions=[], resource=quiz_resource)
    await state.update_data(quiz=quiz, questions=[], resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_quizes.create.send_question", callback.from_user.language_code), 
        reply_markup=manage_quizes_back_keyboard(user_lang=callback.from_user.language_code)
    )
    await state.set_state(CreateQuizState.questions)
    
@router.message(CreateQuizState.questions, UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_add_question(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    
    state_data = await state.get_data()
    
    question_data = message.html_text.split('\n')
    question_text = question_data[0]
    question_options = question_data[1:]
    right_options = [index for index, option in enumerate(question_options) if option.startswith('!')]
    
    question = QuizQuestionSchema(
        id=uuid4(), 
        image=message.photo[0].file_id if message.photo else None, 
        quiz=state_data["quiz"], 
        options=question_options,
        quiz_id=state_data["quiz"].id,
        right_options=right_options,
        text=question_text)
    
    await state.update_data(questions=[*state_data["questions"], question])
    await state.set_state(CreateQuizState.questions)
    
    await message.answer(
        text=t("manage_quizes.create.add_question", message.from_user.language_code), 
        reply_markup=manage_quizes_add_question_keyboard(user_lang=message.from_user.language_code)
    )
    
@router.callback_query(F.data=="manage_quizes.stop", UserRoleFilter([Role.admin, Role.manager]))
async def create_quiz_finish(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    
    state_data = await state.get_data()
    quiz = state_data["quiz"]
    quiz_questions = state_data["questions"]
    quiz.questions = quiz_questions
    
    try:
        await create_quiz(quiz)
    except IntegrityError as e:
        await callback.message.answer(
            text=t(
                "manage_quizes.create.fail", callback.from_user.language_code)
                            .format(
                                resource_name=quiz.resource.name,
                                question_count=len(quiz_questions)
                                ),
            reply_markup=manage_quizes_back_keyboard(callback.from_user.language_code)
        )
    else:
        await callback.message.answer(
            text=t("manage_quizes.create.success", callback.from_user.language_code)
                            .format(
                                resource_name=quiz.resource.name,
                                question_count=len(quiz_questions)
                    ),
            reply_markup=manage_quizes_back_keyboard(callback.from_user.language_code)
        )