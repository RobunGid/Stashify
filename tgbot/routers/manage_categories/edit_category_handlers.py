from math import ceil

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from config.bot_config import bot
from keyboards.manage_categories.manage_categories_back_keyboard import manage_categories_back_keyboard
from keyboards.manage_categories.manage_categories_edit_keyboard import EditCategoryIdCallbackFactory, manage_categories_edit_keyboard
from config.var_config import EDIT_CATEGORIES_ON_PAGE
from schemas.category_schema import UpdateCategorySchema
from .router import router
from database.managers import CategoryManager

class EditCategoryState(StatesGroup):
    total_pages = State()
    categories = State()
    new_category_name = State()
    category_id = State()

@router.callback_query(F.data=="edit_category", UserRoleFilter([Role.admin]))
async def edit_category_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await CategoryManager.get_many()
    total_pages=ceil(len(categories)/EDIT_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_categories.edit.text", callback.from_user.language_code), 
        reply_markup=manage_categories_edit_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("category_id")
    
@router.callback_query(EditCategoryIdCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin]))
async def edit_category_page(callback: CallbackQuery, state: FSMContext, callback_data: EditCategoryIdCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
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
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    await callback.message.answer(
        text=t("manage_categories.edit.text", callback.from_user.language_code),
        reply_markup=manage_categories_back_keyboard(callback.from_user.language_code)
    )
    
    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(EditCategoryState.new_category_name)
    
@router.message(EditCategoryState.new_category_name)
async def new_category_name_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: 
        return
    state_data = await state.get_data()
    category_id = state_data["category_id"]
    new_category_name = message.html_text
    new_category = UpdateCategorySchema(id=category_id, name=new_category_name)
    try:
        await CategoryManager.update(category_id, new_category)
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