from math import ceil
from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_resources.manage_resources_back_keyboard import manage_resources_back_keyboard
from keyboards.manage_resources.manage_resources_delete_resource_list_keyboard import DeleteResourceCallbackFactory, manage_resources_delete_resource_list_keyboard
from keyboards.manage_resources.manage_resources_delete_keyboard_confirm import manage_resources_delete_keyboard_confirm
from config.bot_config import bot
from config.var_config import EDIT_RESOURCE_RESOURCES_ON_PAGE, DELETE_RESOURCE_RESOURCES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.delete_resource import delete_resource
from .router import router
        
class DeleteResourceState(StatesGroup):
    total_pages = State()
    resources = State()
    resource_id = State()
    confirm = State()

@router.callback_query(F.data=="delete_resource", UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    resources = await get_resources()
    total_pages = ceil(len(resources)/DELETE_RESOURCE_RESOURCES_ON_PAGE)
    await state.update_data(total_pages=total_pages, resources=resources)
    
    await callback.message.answer(
        text=t("manage_resources.delete.choose_resource", callback.from_user.language_code), 
        reply_markup=manage_resources_delete_resource_list_keyboard(resources=resources[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("resource_id")
    
@router.callback_query(DeleteResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_page(callback: CallbackQuery, state: FSMContext, callback_data: DeleteResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*EDIT_RESOURCE_RESOURCES_ON_PAGE:current_page*(EDIT_RESOURCE_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_resources.delete.choose_to_delete", callback.from_user.language_code), 
        reply_markup=manage_resources_delete_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(DeleteResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_select(callback: CallbackQuery, callback_data: DeleteResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    await state.update_data(resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_resources.delete.choose_to_delete", callback.from_user.language_code),
        reply_markup=manage_resources_delete_keyboard_confirm(callback.from_user.language_code)
    )
    
@router.callback_query(F.data=="delete_resource_choose", UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_choose(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_name = next((resource.name for resource in state_data["resources"] if resource.id == state_data["resource_id"]), "Unknown")
    
    await callback.message.answer(
        text=t("manage_resources.delete.name.text", callback.from_user.language_code).format(name=resource_name),
        reply_markup=manage_resources_delete_keyboard_confirm(callback.from_user.language_code)
    )
    
@router.callback_query(F.data=="delete_resource_confirm", UserRoleFilter([Role.admin, Role.manager]))
async def delete_resource_name_confirm(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_data = await state.get_data()
    resource = next((resource for resource in resource_data["resources"] if resource.id==resource_data["resource_id"]), {})
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