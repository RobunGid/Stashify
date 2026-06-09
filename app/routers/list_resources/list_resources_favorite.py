from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.managers import FavoriteManager, ResourceManager, ResourceRatingManager
from keyboards.list_resources.list_resources_resource_item_keyboard import (
    list_resources_resource_item_keyboard,
    ListResourcesItemCallbackFactory,
)
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory
from schemas.favorite_schema import FavoriteSchema
from settings.config import bot
from utils.format_resource_text import format_resource_text

from .router import router


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "add_favorite"),
)
async def list_resource_resource_add_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource = await ResourceManager.get_one(resource_id=callback_data.resource_id)
    if not resource:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    favorite = FavoriteSchema(user_id=user_id, resource_id=resource.resource_id)
    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_id=resource.resource_id,
    )
    await FavoriteManager.create(favorite)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code,
            resource=resource,
            is_favorite=True,
            rating=resource_rating.rating if resource_rating else 0,
        ),
    )


@router.callback_query(
    ListResourcesItemCallbackFactory.filter(F.action == "remove_favorite"),
)
async def list_resource_resource_remove_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ListResourcesChooseResourceCallbackFactory,
):
    if (
        not callback.from_user
        or not callback.from_user.language_code
        or not callback.message
        or not callback.data
        or not callback_data.resource_id
    ):
        return
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    resource = await ResourceManager.get_one(resource_id=callback_data.resource_id)
    if not resource:
        return
    state_data = await state.get_data()
    resources = state_data["resources"]
    formatted_text = format_resource_text(resource)
    user_id = str(callback.from_user.id)
    resource_rating = await ResourceRatingManager.get_one(
        user_id=user_id,
        resource_id=resource.resource_id,
    )

    await FavoriteManager.delete(user_id=user_id, resource_id=resource.resource_id)
    await state.update_data(resources=resources)
    await callback.message.answer_photo(
        photo=resource.image,
        caption=formatted_text,
        reply_markup=list_resources_resource_item_keyboard(
            resources=resources,
            user_lang=callback.from_user.language_code,
            resource=resource,
            is_favorite=False,
            rating=resource_rating.rating if resource_rating else 0,
        ),
    )
