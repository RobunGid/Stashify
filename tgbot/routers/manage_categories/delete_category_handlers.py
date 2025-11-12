from math import ceil

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from config.bot_config import bot
from keyboards.manage_categories.manage_categories_back_keyboard import manage_categories_back_keyboard
from keyboards.manage_categories.manage_categories_edit_keyboard import EditCategoryIdCallbackFactory
from keyboards.manage_categories.manage_categories_delete_keyboard import DeleteCategoryIdCallbackFactory, manage_categories_delete_keyboard
from config.var_config import DELETE_CATEGORIES_ON_PAGE
from .router import router
from database.managers import CategoryManager

class DeleteCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    category_id = State()

@router.callback_query(F.data=="delete_category", UserRoleFilter([Role.admin]))
async def delete_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message:
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await CategoryManager.get_categories()
    total_pages = ceil(len(categories)/DELETE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_categories.delete.choose", callback.from_user.language_code), 
        reply_markup=manage_categories_delete_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("category_id")
    
@router.callback_query(DeleteCategoryIdCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin]))
async def delete_category_page(callback: CallbackQuery, state: FSMContext, callback_data: EditCategoryIdCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
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
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    categories_data = await state.get_data()
    category = next((category for category in categories_data["categories"] if category.id == callback_data.category_id), None)
    try:
        if not callback_data.category_id:
            raise ValueError
        await CategoryManager.delete_category(callback_data.category_id)
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
     