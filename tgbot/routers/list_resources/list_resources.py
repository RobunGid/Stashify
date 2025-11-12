from math import ceil

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory, list_resources_resource_list_keyboard
from .router import router
from config.bot_config import bot
from config.var_config import LIST_RESOURCES_RESOURCES_ON_PAGE, LIST_RESOURCES_CATEGORIES_ON_PAGE
from keyboards.list_resources.list_resources_category_list_keyboard import ListResourcesChooseCategoryCallbackFactory, list_resources_category_list_keyboard
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory, list_resources_resource_item_keyboard
from i18n.translate import t
from utils.format_resource_text import format_resource_text
from database.managers import CategoryManager
from database.managers import ResourceManager
from database.managers import ResourceRatingManager
from database.managers import FavoriteManager

@router.callback_query(F.data=="resources")
async def list_resources_callback_handler(callback: CallbackQuery, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    categories = await CategoryManager.get_many(has_resources=True)
    total_categories_pages = ceil(len(categories) / LIST_RESOURCES_CATEGORIES_ON_PAGE)
    await state.update_data(total_categories_pages=total_categories_pages, categories=categories, current_page=1)
    
    await callback.message.answer(
        text=t("list_resources.choose_category", callback.from_user.language_code), 
        reply_markup=list_resources_category_list_keyboard(categories=categories[0:5], user_lang=callback.from_user.language_code, total_pages=total_categories_pages, page=1)
    )
    
@router.callback_query(ListResourcesChooseCategoryCallbackFactory.filter(F.action == "change_page"))
async def list_resources_category_page(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseCategoryCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    
    await state.update_data(current_page=current_page)
    
    categories_data = await state.get_data()
    categories = categories_data["categories"][(current_page-1)*LIST_RESOURCES_CATEGORIES_ON_PAGE:current_page*(LIST_RESOURCES_CATEGORIES_ON_PAGE)]
    total_categories_pages = categories_data["total_categories_pages"]
    
    await callback.message.answer(
        text=t("list_resources.choose_category", callback.from_user.language_code), 
        reply_markup=list_resources_category_list_keyboard(
            categories=categories, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_categories_pages, 
            page=int(current_page))
    )
    
@router.callback_query(ListResourcesChooseCategoryCallbackFactory.filter(F.action=="select"))
async def list_resources_category_select(callback: CallbackQuery, callback_data: ListResourcesChooseCategoryCallbackFactory, state: FSMContext):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    category_id = callback_data.category_id
    await state.update_data(category_id=category_id)
    resources = await ResourceManager.get_many(category_id=category_id)
    total_resources_pages = ceil(len(resources) / LIST_RESOURCES_RESOURCES_ON_PAGE)
    await state.update_data(category_id=category_id, resources=resources, total_resources_pages=total_resources_pages)
    await callback.message.answer(
        text=t("list_resources.choose_resource", callback.from_user.language_code),
        reply_markup=list_resources_resource_list_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            total_pages=total_resources_pages, 
            page=1)
        )
    
@router.callback_query(ListResourcesChooseResourceCallbackFactory.filter(F.action=="change_page"))
async def list_resource_resource_page(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    current_page = callback_data.page
    await state.update_data(current_page=current_page)
    
    resources_data = await state.get_data()
    resources = resources_data["resources"][(current_page-1)*LIST_RESOURCES_RESOURCES_ON_PAGE:current_page*(LIST_RESOURCES_RESOURCES_ON_PAGE)]
    total_resources_pages = resources_data["total_resources_pages"]
    
    await callback.message.answer(
        text=t("list_resources.change_page", callback.from_user.language_code), 
        reply_markup=list_resources_resource_list_keyboard(
            resources=resources, 
            user_lang=callback.from_user.language_code, 
            total_pages=total_resources_pages, 
            page=int(current_page))
    )
    
@router.callback_query(ListResourcesChooseResourceCallbackFactory.filter(F.action=="select"))
async def list_resource_resource_select(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data or not callback_data.resource_id: 
        return
    resource = await ResourceManager.get_one(resource_id=callback_data.resource_id)
    if not resource:
        return
    state_data = await state.get_data()
    category_id = state_data["category_id"]
    resources = await ResourceManager.get_many(category_id=category_id)
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_many(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    resource_rating = await ResourceRatingManager.get_one(user_id=user_id, resource_id=resource.id)
    await state.update_data(resources=resources, resource=resource)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=resource_rating.rating if resource_rating else 0,
            has_quiz=bool(resource.quiz),
            quiz_percent=0
    ))
    
@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="change_page"))
async def list_resource_resource_change_page(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesChooseResourceCallbackFactory):
    if not callback.from_user or not callback.from_user.language_code or not callback.message or not callback.data or not callback_data.resource_id: 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource = await ResourceManager.get_one(resource_id=callback_data.resource_id)
    if not resource:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_many(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    resource_rating = await ResourceRatingManager.get_one(user_id=user_id, resource_id=resource.id)
    await state.update_data(resources=resources, resource=resource)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=resource_rating.rating if resource_rating else 0,
			has_quiz=bool(resource.quiz),
            quiz_percent=0
    ))
    
