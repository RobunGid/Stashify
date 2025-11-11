from math import ceil
from uuid import uuid4

from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .router import router
from database.models.user import Role
from config.var_config import FIND_RESOURCE_RESOURCES_ON_PAGE
from config.bot_config import bot
from keyboards.search_resource.search_resource_back_keyboard import search_resource_back_keyboard
from keyboards.search_resource.search_resource_resource_list_keyboard import search_resource_resource_list_keyboard, SearchResourceResourceListCallbackFactory
from keyboards.search_resource.search_resource_resource_item_keyboard import SearchResourceItemCallbackFactory, search_resource_resource_item_keyboard
from i18n.translate import t
from aiogram.types import Message
from database.operations.get_resources import get_resources
from database.operations.get_resource import get_resource
from database.operations.get_resource_rating import get_resource_rating
from utils.format_resource_text import format_resource_text
from database.operations.get_user_favorites import get_user_favorites
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory
from database.operations.get_user_favorites import get_user_favorites
from database.operations.create_favorite import create_favorite
from database.operations.remove_favorite import remove_favorite
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from .router import router
from config.bot_config import bot
from database.operations.get_resources import get_resources
from database.operations.get_resource import get_resource
from database.operations.get_resource_rating import get_resource_rating
from database.operations.create_resource_rating import create_resource_rating
from database.operations.delete_resource_rating import delete_resource_rating
from i18n.translate import t
from utils.format_resource_text import format_resource_text
from schemas.favorite_schema import FavoriteSchema

class SearchResourceState(StatesGroup):
    text = State() 
    total_pages = State()
    resources = State()
    
@router.callback_query(F.data=="search_resource")
async def search_resource_start(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    await callback.message.answer(
        text=t("search_resource.enter_text", callback.from_user.language_code), 
        reply_markup=search_resource_back_keyboard(user_lang=callback.from_user.language_code)
    )
    await state.set_state(SearchResourceState.text)
    
@router.message(SearchResourceState.text)
async def search_resource_search(message: Message, state: FSMContext):
    if not message.from_user or not message.from_user.language_code or not message: return
    
    resources = await get_resources(text=message.text)
    total_pages = ceil(len(resources)/FIND_RESOURCE_RESOURCES_ON_PAGE)
    await state.update_data(total_pages=total_pages, resources=resources)
    
    await message.answer(
        text=t("search_resource.select", message.from_user.language_code),
        reply_markup=search_resource_resource_list_keyboard(user_lang=message.from_user.language_code, resources=resources, page=1, total_pages=total_pages)
    )
    
@router.callback_query(SearchResourceResourceListCallbackFactory.filter(F.action == "change_page"))
async def search_resource_change_page(callback: CallbackQuery, state: FSMContext, callback_data: SearchResourceResourceListCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    state_data = await state.get_data()
    resources = state_data["resources"][(current_page-1)*FIND_RESOURCE_RESOURCES_ON_PAGE:current_page*(FIND_RESOURCE_RESOURCES_ON_PAGE)]
    total_pages = state_data["total_pages"]
    
    await callback.message.answer(
        text=t("search_resource.select", callback.from_user.language_code), 
        reply_markup=search_resource_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_pages, 
            page=int(current_page))
    )
    
@router.callback_query(SearchResourceResourceListCallbackFactory.filter(F.action == "select"))
async def search_resource_select(callback: CallbackQuery, state: FSMContext, callback_data: SearchResourceResourceListCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback_data.resource_id: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    state_data = await state.get_data()
    resources = state_data["resources"]
    
    resource_id = callback_data.resource_id
    resource = await get_resource(resource_id=resource_id)
    user_id = str(callback.from_user.id)
    favorites = await get_user_favorites(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    formatted_text = format_resource_text(resource)
    resource_rating = await get_resource_rating(user_id=user_id, resource_id=resource.id)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=search_resource_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=resource_rating.rating if resource_rating else 0
    ))
    
@router.callback_query(SearchResourceItemCallbackFactory.filter(F.action == "change_page"))
async def search_resource_resource_change_page(callback: CallbackQuery, state: FSMContext, callback_data: SearchResourceItemCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data or not callback_data.resource_id: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource = await get_resource(resource_id=callback_data.resource_id)
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorites = await get_user_favorites(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    resource_rating = await get_resource_rating(user_id=user_id, resource_id=resource.id)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=search_resource_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=resource_rating.rating if resource_rating else 0
    ))
    

@router.callback_query(SearchResourceItemCallbackFactory.filter(F.action=="add_favorite"))
async def list_resource_resource_add_favorite(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data or not callback_data.resource_id: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource = await get_resource(resource_id=callback_data.resource_id)
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorite = FavoriteSchema(user_id=user_id, resource_id=resource.id)
    resource_rating = await get_resource_rating(user_id=user_id, resource_id=resource.id)
    await create_favorite(favorite)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=search_resource_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=True,
            rating=resource_rating.rating if resource_rating else 0
    ))

@router.callback_query(SearchResourceItemCallbackFactory.filter(F.action=="remove_favorite"))
async def list_resource_resource_remove_favorite(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data or not callback_data.resource_id: return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource = await get_resource(resource_id=callback_data.resource_id)
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    resource_rating = await get_resource_rating(user_id=user_id, resource_id=resource.id)
    
    await remove_favorite(user_id=user_id, resource_id=resource.id)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=search_resource_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=False,
            rating=resource_rating.rating if resource_rating else 0
    ))
    
@router.callback_query(SearchResourceItemCallbackFactory.filter(F.action=="rate"))
async def list_resource_resource_rate(callback: CallbackQuery, state: FSMContext, callback_data: SearchResourceItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id or 
        not callback_data.rating): return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    resource = await get_resource(resource_id=resource_id)
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorites = await get_user_favorites(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    rating = callback_data.rating
    existing_resource_rating = await get_resource_rating(user_id=user_id, resource_id=resource.id)
    print(999991, existing_resource_rating)
    if existing_resource_rating:
        await delete_resource_rating(user_id=user_id, resource_id=resource.id)
    resource_rating = ResourceRatingWithoutUserAndResourceSchema(id=uuid4(), resource_id=resource_id, rating=rating, user_id=user_id)
    await create_resource_rating(resource_rating)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=search_resource_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=rating
    ))
