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
from keyboards.manage_resources.manage_resources_create_keyboard import manage_resources_create_keyboard, CreateResourceCallbackFactory
from keyboards.manage_resources.manage_resources_back_keyboard import manage_resources_back_keyboard
from config.bot_config import bot
from config.var_config import CREATE_RESOURCE_CATEGORIES_ON_PAGE
from database.operations.get_categories import get_categories
from database.operations.create_resource import create_resource
from schemas.resource_schema import ResourceSchema
from .router import router

class CreateResourceState(StatesGroup):
    total_pages = State()
    categories = State()
    category_id = State()
    name = State()
    description = State()
    links = State()
    image = State()
    tags = State()

@router.callback_query(F.data=="create_resource", UserRoleFilter([Role.admin, Role.manager]))
async def create_resource_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await get_categories()
    total_pages=ceil(len(categories)/CREATE_RESOURCE_CATEGORIES_ON_PAGE)
    await state.update_data(total_pages=total_pages, categories=categories)
    
    await callback.message.answer(
        text=t("manage_resources.create.choose_category", callback.from_user.language_code), 
        reply_markup=manage_resources_create_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_pages, page=1)
    )
    await state.set_state("resource_id")
    
@router.callback_query(CreateResourceCallbackFactory.filter(F.action == "change_page"), UserRoleFilter([Role.admin, Role.manager]))
async def create_resource_page(callback: CallbackQuery, state: FSMContext, callback_data: CreateResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    categories_data = await state.get_data()
    categories = categories_data["categories"][(current_page-1)*CREATE_RESOURCE_CATEGORIES_ON_PAGE:current_page*(CREATE_RESOURCE_CATEGORIES_ON_PAGE)]
    total_pages = categories_data["total_pages"]
    
    await callback.message.answer(
        text=t("manage_resources.create.choose_category", callback.from_user.language_code), 
        reply_markup=manage_resources_create_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(CreateResourceCallbackFactory.filter(F.action=="select"), UserRoleFilter([Role.admin, Role.manager]))
async def create_resource_choose(callback: CallbackQuery, callback_data: CreateResourceCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    await callback.message.answer(
        text=t("manage_resources.create.wait_name", callback.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(callback.from_user.language_code)
    )
    
    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(CreateResourceState.name)
    
@router.message(CreateResourceState.name, F.text, UserRoleFilter([Role.admin, Role.manager]))
async def new_resource_name_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    await state.update_data(name=message.html_text)
    await message.answer(
        text=t("manage_resources.create.wait_description", message.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
    )
    await state.set_state(CreateResourceState.description)
    
@router.message(CreateResourceState.description, F.text, UserRoleFilter([Role.admin, Role.manager]))
async def new_resource_description_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    await state.update_data(description=message.html_text)
    await message.answer(
        text=t("manage_resources.create.wait_image", message.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
    )
    await state.set_state(CreateResourceState.links)
    
@router.message(CreateResourceState.links, F.text, UserRoleFilter([Role.admin, Role.manager]))
async def new_resource_links_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    await state.update_data(description=message.html_text)
    await message.answer(
        text=t("manage_resources.create.wait_links", message.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
    )
    await state.set_state(CreateResourceState.image)
    
@router.message(CreateResourceState.image, F.photo[-1].as_("resource_image"))
async def new_resource_image_choose(message: Message, state: FSMContext, resource_image: PhotoSize):
    if not message.from_user or not message.from_user.language_code: return
    await state.update_data(image=resource_image.file_id)
    await message.answer(
        text=t("manage_resources.create.wait_tags", message.from_user.language_code),
        reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
    )
    await state.set_state(CreateResourceState.tags)
    
@router.message(CreateResourceState.tags, F.text)
async def new_resource_tags_choose(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code: return
    state_data = await state.get_data()
    resource_data = ResourceSchema(
        category_id=state_data["category_id"],
        id=uuid4(), 
        name=state_data["name"], 
        description=state_data["description"], 
        links=state_data["links"], 
        image=state_data["image"],
        tags=message.html_text, 
    )
    category_name = next((category.name for category in state_data["categories"]), "Unknown")
    try:
        await create_resource(resource_data)
    except IntegrityError as e:
        await message.answer(
            text=t(
                "manage_resources.create.fail", message.from_user.language_code)
                            .format(
                                resource_name=resource_data.name,
                                resource_description=resource_data.description,
                                resource_tags=resource_data.tags,
                                category_name=category_name,
                                ),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )
    else:
        await message.answer_photo(
            photo=resource_data.image,
            caption=t("manage_resources.create.success", message.from_user.language_code)
                            .format(
                                resource_name=resource_data.name,
                                resource_description=resource_data.description,
                                resource_tags=resource_data.tags,
                                category_name=category_name,
                                ),
            reply_markup=manage_resources_back_keyboard(message.from_user.language_code)
        )