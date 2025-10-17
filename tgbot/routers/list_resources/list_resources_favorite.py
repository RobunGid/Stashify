from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory
from database.operations.create_favorite import create_favorite
from database.operations.remove_favorite import remove_favorite
from .router import router
from config.bot_config import bot
from database.operations.get_resource import get_resource
from database.operations.get_resource_rating import get_resource_rating
from keyboards.list_resources.list_resources_resource_item_keyboard import ListResourcesItemCallbackFactory, list_resources_resource_item_keyboard
from i18n.translate import t
from utils.format_resource_text import format_resource_text
from schemas.favorite_schema import FavoriteSchema
 
@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="add_favorite"))
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
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=True,
            rating=resource_rating.rating if resource_rating else 0
    ))

@router.callback_query(ListResourcesItemCallbackFactory.filter(F.action=="remove_favorite"))
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
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code, 
            resource=resource,
            is_favorite=False,
            rating=resource_rating.rating if resource_rating else 0
    ))