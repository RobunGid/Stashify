from math import ceil
from uuid import uuid4

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_categories_keyboard import manage_categories_keyboard
from config.bot_config import bot
from database.operations.create_category import create_category
from schemas.category_schema import CategorySchema
from keyboards.manage_categories_back_keyboard import manage_categories_back_keyboard
from database.operations.get_categories import get_categories
from keyboards.manage_categories_edit_keyboard import EditCategoryIdCallbackFactory, manage_categories_edit_keyboard
from keyboards.manage_categories_delete_keyboard import DeleteCategoryIdCallbackFactory, manage_categories_delete_keyboard
from config.var_config import EDIT_CATEGORIES_ON_PAGE, DELETE_CATEGORIES_ON_PAGE
from database.operations.edit_category import edit_category
from database.operations.delete_category import delete_category

router = Router()

@router.callback_query(F.data=="manage_categories", UserRoleFilter([Role.admin]))
async def manage_categories(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.text", callback.from_user.language_code), 
        reply_markup=manage_categories_keyboard(callback.from_user.language_code)
    )
    
class CreateCategoryState(StatesGroup):
    choosing_category_name = State()

@router.callback_query(F.data=="create_category", UserRoleFilter([Role.admin]))
async def create_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(
        text=t("manage_categories.create.text", callback.from_user.language_code), 
        reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(CreateCategoryState.choosing_category_name)
    
@router.message(CreateCategoryState.choosing_category_name, F.text, UserRoleFilter([Role.admin]))
async def create_category_final(message: Message):
    if not message.from_user: return
    category_data = CategorySchema(id=uuid4(), name=message.html_text)
    try:
        await create_category(category_data)
    except IntegrityError:
        await message.answer(
            text=t("manage_categories.create.fail", message.from_user.language_code).format(category_name=category_data.name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )
    else:
        await message.answer(
            text=t("manage_categories.create.success", message.from_user.language_code).format(category_name=category_data.name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )
        
class EditCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    new_category_name = State()
    category_id = State()

@router.callback_query(F.data=="edit_category", UserRoleFilter([Role.admin]))
async def edit_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages=ceil(len(categories)/EDIT_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_categories.edit.text", callback.from_user.language_code), 
        reply_markup=manage_categories_edit_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("category_id")
    
@router.callback_query(EditCategoryIdCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin]))
async def edit_category_page(callback: CallbackQuery, state: FSMContext, callback_data: EditCategoryIdCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page=callback_data.page
    
    await state.update_data(current_page=current_page)
    
    categories_data = await state.get_data()
    categories = categories_data["categories"][(current_page-1)*EDIT_CATEGORIES_ON_PAGE:current_page*(EDIT_CATEGORIES_ON_PAGE)]
    total_pages = categories_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_categories.edit.choose", callback.from_user.language_code), 
        reply_markup=manage_categories_edit_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(EditCategoryIdCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin]))
async def edit_category_choose(callback: CallbackQuery, callback_data: EditCategoryIdCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    await callback.message.answer(
        text=t("manage_categories.edit.text", callback.from_user.language_code),
        reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
    )
    
    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(EditCategoryState.new_category_name)
    
@router.message(EditCategoryState.new_category_name)
async def new_category_name_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    state_date = await state.get_data()
    new_category_name = message.html_text
    category_id = state_date["category_id"]
    try:
        await edit_category(category_id, new_category_name)
    except ValueError:
        await message.answer(
            text=t("manage_categories.edit.fail", message.from_user.language_code).format(category_name=new_category_name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )
    else:
        await message.answer(
            text=t("manage_categories.edit.success", message.from_user.language_code).format(category_name=new_category_name),
            reply_markup=manage_categories_back_keyboard(message.from_user.language_code)
        )
    await state.clear()
    
class DeleteCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    category_id = State()

@router.callback_query(F.data=="delete_category", UserRoleFilter([Role.admin]))
async def delete_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages = ceil(len(categories)/DELETE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_categories.delete.choose", callback.from_user.language_code), 
        reply_markup=manage_categories_delete_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("category_id")
    
@router.callback_query(DeleteCategoryIdCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin]))
async def delete_category_page(callback: CallbackQuery, state: FSMContext, callback_data: EditCategoryIdCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    categories_data = await state.get_data()
    categories = categories_data["categories"][(current_page-1)*DELETE_CATEGORIES_ON_PAGE:current_page*(DELETE_CATEGORIES_ON_PAGE)]
    total_pages = categories_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_categories.delete.choose", callback.from_user.language_code), 
        reply_markup=manage_categories_delete_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteCategoryIdCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin]))
async def delete_category_choose(callback: CallbackQuery, callback_data: DeleteCategoryIdCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    categories_data = await state.get_data()
    category = next((category for category in categories_data["categories"] if category.id == callback_data.category_id), None)
    try:
        if not callback_data.category_id:
            raise ValueError
        await delete_category(callback_data.category_id)
    except (IntegrityError, ValueError):
        await callback.message.answer(
            text=t("manage_categories.delete.fail", callback.from_user.language_code).format(category_name=category.name if category else "unknown"),
            reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
        )
    else:
        await callback.message.answer(
            text=t("manage_categories.delete.success", callback.from_user.language_code).format(category_name=category.name if category else "unknown"),
            reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
        )
     