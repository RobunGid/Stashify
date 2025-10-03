from math import ceil

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_quizes.manage_quizes_edit_resource_list_keyboard import manage_quizes_edit_resource_list_keyboard, EditQuizChooseResourceCallbackFactory
from keyboards.manage_quizes.manage_quizes_edit_category_list_keyboard import manage_quizes_edit_category_list_keyboard, EditQuizChooseCategoryCallbackFactory
from keyboards.manage_quizes.manage_quizes_edit_keyboard import EditQuizActionCallbackFactory, manage_quizes_edit_keyboard
from config.bot_config import bot
from config.var_config import EDIT_QUIZ_RESOURCES_ON_PAGE, EDIT_QUIZ_CATEGORIES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.get_categories import get_categories
from keyboards.manage_quizes.manage_quizes_delete_question_back_keyboard import manage_quizes_delete_question_back_keyboard
from database.operations.get_quiz_questions import get_quiz_questions
from .router import router

class EditQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_id = State()
    question_number = State()

@router.callback_query(F.data=="edit_quiz", UserRoleFilter([Role.admin, Role.manager]))
async def edit_quiz_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories(has_quizes=True)
    total_pages = ceil(len(categories)/EDIT_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_quizes.edit.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_edit_category_list_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    
@router.callback_query(EditQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_quiz_category_page(callback: CallbackQuery, state: FSMContext, callback_data: EditQuizChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    state_data = await state.get_data()
    categories = state_data["categories"][(current_page-1)*EDIT_QUIZ_CATEGORIES_ON_PAGE:current_page*(EDIT_QUIZ_CATEGORIES_ON_PAGE)]
    total_pages = state_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.edit.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_edit_category_list_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(EditQuizChooseCategoryCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_quizes_category_choose(callback: CallbackQuery, callback_data: EditQuizChooseCategoryCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    category_id = callback_data.category_id
    resources = await get_resources(category_id=category_id, has_quiz=True)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources)/EDIT_QUIZ_RESOURCES_ON_PAGE)
    
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text=t("manage_quizes.edit.choose_to_change", callback.from_user.language_code),
        reply_markup=manage_quizes_edit_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=1)
    )
    
@router.callback_query(EditQuizChooseResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_quiz_page(callback: CallbackQuery, state: FSMContext, callback_data: EditQuizChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*EDIT_QUIZ_RESOURCES_ON_PAGE:current_page*(EDIT_QUIZ_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.edit.choose", callback.from_user.language_code), 
        reply_markup=manage_quizes_edit_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(EditQuizChooseResourceCallbackFactory.filter(F.action == "select"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_choose(callback: CallbackQuery, callback_data: EditQuizChooseResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    await state.update_data(resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_quizes.edit.choose_to_change", callback.from_user.language_code),
        reply_markup=manage_quizes_edit_keyboard(callback.from_user.language_code, resource_id=resource_id)
    )
    
@router.callback_query(EditQuizActionCallbackFactory.filter(F.action == "delete"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_delete_question(callback: CallbackQuery, callback_data: EditQuizChooseResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_id = state_data["resource_id"]
    quiz_questions = await get_quiz_questions(resource_id=resource_id)
    
    formatted_questions = ""
    
    for index, question in enumerate(quiz_questions):
        formatted_question = f"{index+1}. {question.text}\n"
        
        for option in question.options:
            if index in question.right_options:
                formatted_question += f"!{option}\n"
            else:
                formatted_question += f"{option}\n"
        
        formatted_questions += formatted_question + "\n"
    
    await callback.message.answer(
        text=t("manage_quizes.edit.delete_question_number", callback.from_user.language_code).format(questions=formatted_questions),
        reply_markup=manage_quizes_delete_question_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(EditQuizState.question_number)
    
@router.message(EditQuizState.question_number, F.text, UserRoleFilter([Role.admin, Role.manager]))
async def delete_question_confirm(state: FSMContext):
    state_data = await state.get_data()
    resource_id = state_data["resource_id"]