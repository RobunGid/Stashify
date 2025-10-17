from uuid import uuid4

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.operations.get_user_favorites import get_user_favorites
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from .router import router
from config.bot_config import bot
from database.operations.get_resource import get_resource
from database.operations.get_resource_rating import get_resource_rating
from database.operations.create_resource_rating import create_resource_rating
from database.operations.delete_resource_rating import delete_resource_rating
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory, list_resources_resource_item_keyboard
from i18n.translate import t
from utils.format_resource_text import format_resource_text

@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="rate"))
async def list_resource_resource_rate(callback: CallbackQuery, state: FSMContext, callback_data: ListResourcesItemCallbackFactory):
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
    if existing_resource_rating:
        await delete_resource_rating(user_id=user_id, resource_id=resource.id)
    resource_rating = ResourceRatingWithoutUserAndResourceSchema(id=uuid4(), resource_id=resource_id, rating=rating, user_id=user_id)
    await create_resource_rating(resource_rating)
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