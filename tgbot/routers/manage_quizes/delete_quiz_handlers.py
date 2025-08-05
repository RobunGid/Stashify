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
from keyboards.manage_quizes.manage_quizes_delete_category_list_keyboard import manage_quizes_delete_category_list_keyboard, DeleteQuizChooseCategoryCallbackFactory
from keyboards.manage_quizes.manage_quizes_delete_resource_list_keyboard import manage_quizes_delete_resource_list_keyboard, DeleteQuizChooseResourceCallbackFactory
from keyboards.manage_quizes.manage_quizes_delete_keyboard_confirm import manage_quizes_delete_keyboard_confirm
from config.bot_config import bot
from config.var_config import DELETE_QUIZ_CATEGORIES_ON_PAGE, DELETE_QUIZ_RESOURCES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.get_categories import get_categories
from keyboards.manage_quizes.manage_quizes_back_keyboard import manage_quizes_back_keyboard
from schemas.quiz_question_schema import QuizQuestionSchema
from schemas.quiz_schema import QuizSchema
from keyboards.manage_quizes.manage_quizes_add_question_keyboard import manage_quizes_add_question_keyboard
from database.operations.delete_quiz import delete_quiz
from .router import router

class DeleteQuizState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_id = State()
    category_id = State()
    confirm = State()

@router.callback_query(F.data=="delete_quiz", UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages = ceil(len(categories) / DELETE_QUIZ_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_quizes.delete.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_delete_category_list_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    
@router.callback_query(DeleteQuizChooseCategoryCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_category_page(callback: CallbackQuery, state: FSMContext, callback_data: DeleteQuizChooseCategoryCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    state_data = await state.get_data()
    categories = state_data["categories"][(current_page-1)*DELETE_QUIZ_CATEGORIES_ON_PAGE:current_page*(DELETE_QUIZ_CATEGORIES_ON_PAGE)]
    total_pages = state_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.delete.choose_category", callback.from_user.language_code), 
        reply_markup=manage_quizes_delete_category_list_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteQuizChooseCategoryCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_category_choose(callback: CallbackQuery, callback_data: DeleteQuizChooseCategoryCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    category_id = callback_data.category_id
    resources = await get_resources(category_id=category_id, has_quiz=True)
    await state.update_data(resources=resources)
    total_pages = ceil(len(resources)/DELETE_QUIZ_RESOURCES_ON_PAGE)
    
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text=t("manage_quizes.delete.choose_resource", callback.from_user.language_code),
        reply_markup=manage_quizes_delete_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=1)
    )
    
@router.callback_query(DeleteQuizChooseResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_page(callback: CallbackQuery, state: FSMContext, callback_data: DeleteQuizChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*DELETE_QUIZ_RESOURCES_ON_PAGE:current_page*(DELETE_QUIZ_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_quizes.delete.choose", callback.from_user.language_code), 
        reply_markup=manage_quizes_delete_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteQuizChooseResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_choose(callback: CallbackQuery, callback_data: DeleteQuizChooseResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    state_data = await state.get_data()
    
    quiz_resource = next((resource for resource in state_data["resources"] if resource.id == resource_id))
    quiz = QuizSchema(id=uuid4(), resource_id=resource_id, questions=[], resource=quiz_resource)
    await state.update_data(quiz=quiz, questions=[], resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_quizes.delete.choose_to_delete", callback.from_user.language_code), 
        reply_markup=manage_quizes_delete_keyboard_confirm(user_lang=callback.from_user.language_code)
    )
    
@router.callback_query(F.data=="delete_quiz_confirm", UserRoleFilter([Role.admin, Role.manager]))
async def delete_quiz_confirm(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_data = await state.get_data()
    resource = next((resource for resource in resource_data["resources"] if resource.id==resource_data["resource_id"]), {})
    try:
        await delete_quiz(resource_id=resource_data["resource_id"])
    except (IntegrityError, ValueError) as e:
        print(e)
        await callback.message.answer(
            text=t("manage_quizes.delete.fail", callback.from_user.language_code).format(resource_name=resource.name),
            reply_markup=manage_quizes_back_keyboard(callback.from_user.language_code)
        )
    else:
        await callback.message.answer(
            text=t("manage_quizes.delete.success", callback.from_user.language_code).format(resource_name=resource.name),
            reply_markup=manage_quizes_back_keyboard(callback.from_user.language_code)
        )