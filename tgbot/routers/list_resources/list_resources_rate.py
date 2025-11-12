from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from .router import router
from config.bot_config import bot
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory, list_resources_resource_item_keyboard
from utils.format_resource_text import format_resource_text
from database.managers import ResourceRatingManager
from database.managers import ResourceManager
from database.managers import FavoriteManager

@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="rate"))
async def list_resource_resource_rate(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
    if (not callback.from_user or 
        not callback.from_user.language_code or 
        not callback.message or 
        not callback.data or 
        not callback_data.resource_id or 
        not callback_data.rating): 
        return
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    resource_id = callback_data.resource_id
    resource = await ResourceManager.get_resource(resource_id=resource_id)
    if not resource:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorites = await FavoriteManager.get_user_favorites(user_id=user_id)
    is_favorite = any(resource.id == favorite.resource_id for favorite in favorites)
    rating = callback_data.rating
    existing_resource_rating = await ResourceRatingManager.get_resource_rating(user_id=user_id, resource_id=resource.id)
    if existing_resource_rating:
        await ResourceRatingManager.delete_resource_rating(user_id=user_id, resource_id=resource.id)
    resource_rating = ResourceRatingWithoutUserAndResourceSchema(id=uuid4(), resource_id=resource_id, rating=rating, user_id=user_id)
    await ResourceRatingManager.create_resource_rating(resource_rating)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=is_favorite,
            rating=rating
    ))