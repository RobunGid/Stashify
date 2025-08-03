from math import ceil
from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery, Message, PhotoSize
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from database.models.user import Role
from filters.user_role_filter import UserRoleFilter
from i18n.translate import t
from keyboards.manage_resources.manage_resources_edit_resource_list_keyboard import manage_resources_edit_resource_list_keyboard, EditResourceCallbackFactory
from keyboards.manage_resources.manage_resources_edit_keyboard import manage_resources_edit_keyboard
from keyboards.manage_resources.manage_resources_back_keyboard import manage_resources_back_keyboard
from config.bot_config import bot
from config.var_config import EDIT_RESOURCE_RESOURCES_ON_PAGE
from database.operations.get_resources import get_resources
from database.operations.edit_resource import edit_resource
from .router import router

class EditResourceState(StatesGroup):
    total_pages = State()
    resources = State()
    resource_id = State()
    name = State()
    description = State()
    image = State()
    tags = State()

@router.callback_query(F.data=="edit_resource", UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    resources = await get_resources()
    total_pages = ceil(len(resources)/EDIT_RESOURCE_RESOURCES_ON_PAGE)
    await state.update_data(total_pages=total_pages, resources=resources)
    
    await callback.message.answer(
        text=t("manage_resources.edit.choose_resource", callback.from_user.language_code), 
        reply_markup=manage_resources_edit_resource_list_keyboard(resources=resources[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("resource_id")
    
@router.callback_query(EditResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_page(callback: CallbackQuery, state: FSMContext, callback_data: EditResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*EDIT_RESOURCE_RESOURCES_ON_PAGE:current_page*(EDIT_RESOURCE_RESOURCES_ON_PAGE)]
    total_pages = resources_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_resources.edit.choose", callback.from_user.language_code), 
        reply_markup=manage_resources_edit_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(EditResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_choose(callback: CallbackQuery, callback_data: EditResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    await state.update_data(resource_id=resource_id)
    await callback.message.answer(
        text=t("manage_resources.edit.choose_to_change", callback.from_user.language_code),
        reply_markup=manage_resources_edit_keyboard(callback.from_user.language_code)
    )
    
@router.callback_query(F.data=="edit_resource_name", UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_name(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_name = next((resource.name for resource in state_data["resources"] if resource.id == state_data["resource_id"]), "Unknown")
    
    await callback.message.answer(
        text=t("manage_resources.edit.name.text", callback.from_user.language_code).format(name=resource_name),
        reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(EditResourceState.name)
    
@router.message(EditResourceState.name, UserRoleFilter([Role.admin, Role.manager]), F.text)
async def edit_resource_name_success(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    resource_data = await state.get_data()
    try:
        await edit_resource(id=resource_data["resource_id"], new_name=message.html_text)
    except (IntegrityError, ValueError):
        await message.answer(
            text=t("manage_resources.edit.name.fail", message.from_user.language_code).format(name=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        await state.set_state(EditResourceState.name)
    else:
        await message.answer(
            text=t("manage_resources.edit.name.success", message.from_user.language_code).format(name=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        
@router.callback_query(F.data=="edit_resource_description", UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_description(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_description = next((resource.description for resource in state_data["resources"] if resource.id == state_data["resource_id"]), "Unknown")
    
    await callback.message.answer(
        text=t("manage_resources.edit.description.text", callback.from_user.language_code).format(description=resource_description),
        reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(EditResourceState.description)
    
@router.message(EditResourceState.description, UserRoleFilter([Role.admin, Role.manager]), F.text)
async def edit_resource_description_success(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    resource_data = await state.get_data()
    try:
        await edit_resource(id=resource_data["resource_id"], new_description=message.html_text)
    except (IntegrityError, ValueError):
        await message.answer(
            text=t("manage_resources.edit.description.fail", message.from_user.language_code).format(description=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        await state.set_state(EditResourceState.description)
    else:
        await message.answer(
            text=t("manage_resources.edit.description.success", message.from_user.language_code).format(description=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        
@router.callback_query(F.data=="edit_resource_tags", UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_tags(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_tags = next((resource.tags for resource in state_data["resources"] if resource.id == state_data["resource_id"]), "Unknown")
    
    await callback.message.answer(
        text=t("manage_resources.edit.tags.text", callback.from_user.language_code).format(tags=resource_tags),
        reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(EditResourceState.tags)
    
@router.message(EditResourceState.tags, UserRoleFilter([Role.admin, Role.manager]), F.text)
async def edit_resource_tags_success(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    resource_data = await state.get_data()
    try:
        await edit_resource(id=resource_data["resource_id"], new_tags=message.html_text)
    except (IntegrityError, ValueError):
        await message.answer(
            text=t("manage_resources.edit.tags.fail", message.from_user.language_code).format(tags=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        await state.set_state(EditResourceState.tags)
    else:
        await message.answer(
            text=t("manage_resources.edit.tags.success", message.from_user.language_code).format(tags=message.html_text),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        
@router.callback_query(F.data=="edit_resource_image", UserRoleFilter([Role.admin, Role.manager]))
async def edit_resource_image(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    state_data = await state.get_data()
    resource_image = next((resource.image for resource in state_data["resources"] if resource.id == state_data["resource_id"]), "Unknown")
    
    await callback.message.answer_photo(
        photo=resource_image,
        caption=t("manage_resources.edit.image.text", callback.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
    )
    await state.set_state(EditResourceState.image)
    
@router.message(EditResourceState.image, UserRoleFilter([Role.admin, Role.manager]), F.photo[-1].as_("resource_image"))
async def edit_resource_image_success(message: Message, state: FSMContext, resource_image: PhotoSize):
    if not message.from_user or not message.from_user.language_code: return
    resource_data = await state.get_data()
    try:
        await edit_resource(id=resource_data["resource_id"], new_image=resource_image.file_id)
    except (IntegrityError, ValueError):
        await message.answer_photo(
            photo=resource_image.file_id,
            caption=t("manage_resources.edit.image.fail", message.from_user.language_code),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
        await state.set_state(EditResourceState.image)
    else:
        await message.answer_photo(
            photo=resource_image.file_id,
            caption=t("manage_resources.edit.image.success", message.from_user.language_code),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )