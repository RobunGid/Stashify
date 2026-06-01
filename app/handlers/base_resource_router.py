from abc import ABC, abstractmethod
from math import ceil
from uuid import uuid4

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.managers import FavoriteManager, ResourceManager, ResourceRatingManager, CategoryManager
from schemas.favorite_schema import FavoriteSchema
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
from settings.config import bot
from utils.format_resource_text import format_resource_text

from constants import LIST_RESOURCES_CATEGORIES_ON_PAGE, LIST_RESOURCES_RESOURCES_ON_PAGE


class BaseResourceRouter(ABC):
    def __init__(self):
        self.router = Router()

    @abstractmethod
    def _build_resource_item_keyboard(self, resources, resource, user_lang, is_favorite, rating):
        pass

    @abstractmethod
    def _build_resource_list_keyboard(self, resources, user_lang, total_pages, page):
        pass

    @abstractmethod
    def _build_category_list_keyboard(self, categories, user_lang, total_pages, page):
        pass

    async def _delete_message(self, message: Message):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    async def _send_resource_photo(
        self,
        message: Message,
        resource,
        resources,
        user_id: str,
        user_lang: str,
    ):
        formatted_text = format_resource_text(resource)
        favorites = await FavoriteManager.get_many(user_id=user_id)
        is_favorite = any(resource.id == fav.resource_id for fav in favorites)
        resource_rating = await ResourceRatingManager.get_one(user_id=user_id, resource_id=resource.id)

        await message.answer_photo(
            photo=resource.image,
            caption=formatted_text,
            reply_markup=self._build_resource_item_keyboard(
                resources=resources,
                resource=resource,
                user_lang=user_lang,
                is_favorite=is_favorite,
                rating=resource_rating.rating if resource_rating else 0,
            ),
        )

    async def _handle_add_favorite(self, user_id: str, resource_id):
        await FavoriteManager.create(FavoriteSchema(user_id=user_id, resource_id=resource_id))

    async def _handle_remove_favorite(self, user_id: str, resource_id):
        await FavoriteManager.delete(user_id=user_id, resource_id=resource_id)

    async def _handle_rate(self, user_id: str, resource_id, rating: int):
        existing = await ResourceRatingManager.get_one(user_id=user_id, resource_id=resource_id)
        if existing:
            await ResourceRatingManager.delete(user_id=user_id, resource_id=resource_id)
        new_rating = ResourceRatingWithoutUserAndResourceSchema(
            id=uuid4(), resource_id=resource_id, rating=rating, user_id=user_id
        )
        await ResourceRatingManager.create(new_rating)


    async def _show_category_list(
        self,
        message: Message,
        state: FSMContext,
        user_id: str,
        user_lang: str,
        empty_text_key: str,
        choose_text_key: str,
        translate_fn,
    ):
        categories = await CategoryManager.get_many(
            has_resources=True, favorites_user_id=user_id, has_quizes=True
        )
        total_pages = ceil(len(categories) / LIST_RESOURCES_CATEGORIES_ON_PAGE)
        await state.update_data(total_categories_pages=total_pages, categories=categories)

        text_key = choose_text_key if total_pages != 0 else empty_text_key
        await message.answer(
            text=translate_fn(text_key, user_lang),
            reply_markup=self._build_category_list_keyboard(
                categories=categories[:LIST_RESOURCES_CATEGORIES_ON_PAGE],
                user_lang=user_lang,
                total_pages=total_pages,
                page=1,
            ),
        )

    async def _show_resource_list(
        self,
        message: Message,
        state: FSMContext,
        user_id: str,
        category_id,
        user_lang: str,
        text_key: str,
        translate_fn,
    ):
        resources = await ResourceManager.get_many(category_id=category_id, favorites_user_id=user_id)
        total_pages = ceil(len(resources) / LIST_RESOURCES_RESOURCES_ON_PAGE)
        await state.update_data(category_id=category_id, resources=resources, total_resources_pages=total_pages)

        await message.answer(
            text=translate_fn(text_key, user_lang),
            reply_markup=self._build_resource_list_keyboard(
                resources=resources,
                user_lang=user_lang,
                total_pages=total_pages,
                page=1,
            ),
        )