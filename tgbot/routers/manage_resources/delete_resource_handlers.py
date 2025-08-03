from math import ceil

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_resources.manage_resources_back_keyboard import manage_resources_back_keyboard
from keyboards.manage_resources.manage_resources_delete_resource_list_keyboard import DeleteResourceChooseResourceCallbackFactory, manage_resources_delete_resource_list_keyboard
from keyboards.manage_resources.manage_resources_delete_category_list_keyboard import DeleteResourceChooseCategoryCallbackFactory, manage_resources_delete_category_list_keyboard
from keyboards.manage_resources.manage_resources_delete_keyboard_confirm import manage_resources_delete_keyboard_confirm
from config.bot_config import bot
from config.var_config import DELETE_RESOURCE_RESOURCES_ON_PAGE, DELETE_RESOURCE_CATEGORIES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.delete_resource import delete_resource
from database.operations.get_categories import get_categories
from .router import router
        
class DeleteResourceState(StatesGroup):
    total_pages = State()
    resources = State()
    categories = State()
    resource_id = State()
    confirm = State()

@router.callback_query(F.data=="delete_resource", UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages = ceil(len(categories)/DELETE_RESOURCE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_resources.delete.choose_category", callback.from_user.language_code), 
        reply_markup=manage_resources_delete_category_list_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    
@router.callback_query(DeleteResourceChooseCategoryCallbackFactory.filter(F.action=="change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_categories_page(callback: CallbackQuery, state: FSMContext, callback_data: DeleteResourceChooseCategoryCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    resources_data = await state.get_data()
    categories = resources_data["categories"][(current_page-1)*DELETE_RESOURCE_CATEGORIES_ON_PAGE:current_page*(DELETE_RESOURCE_CATEGORIES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_resources.delete.choose_category", callback.from_user.language_code), 
        reply_markup=manage_resources_delete_category_list_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteResourceChooseCategoryCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_category_select(callback: CallbackQuery, callback_data: DeleteResourceChooseCategoryCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    current_page = callback_data.page
    resources_data = await state.get_data()
    category_id = callback_data.category_id
    resources = await get_resources(category_id=category_id)
    total_pages = resources_data["total_pages"]
    await state.update_data(category_id=category_id, resources=resources)
    await callback.message.answer(
        text=t("manage_resources.delete.choose_resource", callback.from_user.language_code),
        reply_markup=manage_resources_delete_resource_list_keyboard(
            resources=resources,
			user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
		)
    
@router.callback_query(DeleteResourceChooseResourceCallbackFactory.filter(F.action=="change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_page(callback: CallbackQuery, state: FSMContext, callback_data: DeleteResourceChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*DELETE_RESOURCE_RESOURCES_ON_PAGE:current_page*(DELETE_RESOURCE_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_resources.delete.choose_resource", callback.from_user.language_code), 
        reply_markup=manage_resources_delete_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteResourceChooseResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_select(callback: CallbackQuery, callback_data: DeleteResourceChooseResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    state_data = await state.get_data()
    resource = next((resource for resource in state_data["resources"] if resource.id==resource_id), {"name": "Unknown"})
    await state.update_data(resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_resources.delete.choose_to_delete", callback.from_user.language_code).format(name=resource.name),
        reply_markup=manage_resources_delete_keyboard_confirm(callback.from_user.language_code)
    )
    
@router.callback_query(F.data=="delete_resource_confirm", UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_name_confirm(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_data = await state.get_data()
    resource = next((resource for resource in resource_data["resources"] if resource.id==resource_data["resource_id"]), {})
    print(23498234982)
    try:
        await delete_resource(id=resource_data["resource_id"])
    except (IntegrityError, ValueError):
        await callback.message.answer(
            text=t("manage_resources.delete.fail", callback.from_user.language_code).format(name=resource.name),
            reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
        )
    else:
        await callback.message.answer(
            text=t("manage_resources.delete.success", callback.from_user.language_code).format(name=resource.name),
            reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
        )