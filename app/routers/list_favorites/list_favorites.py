from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants import (
    LIST_RESOURCES_CATEGORIES_ON_PAGE,
    LIST_RESOURCES_RESOURCES_ON_PAGE,
)

from database.managers import ResourceManager
from handlers.base_resource_router import BaseResourceRouter
from i18n.translate import t
from keyboards.list_favorites.category_list_keyboard import (
    FavoritesCategoryListKeyboard,
    ListFavoritesChooseCategoryCallbackFactory,
)
from keyboards.list_favorites.resource_item_keyboard import (
    FavoritesResourceItemKeyboard,
    ListFavoritesItemCallbackFactory,
)
from keyboards.list_favorites.resource_list_keyboard import (
    FavoritesResourceListKeyboard,
    ListFavoritesChooseResourceCallbackFactory,
)
from routers.list_favorites.router import router


class ListFavoritesRouter(BaseResourceRouter):
    def __init__(self):
        super().__init__()
        self.router = router
        self._register_handlers()

    def _build_category_list_keyboard(self, categories, user_lang, total_pages, page):
        return FavoritesCategoryListKeyboard(
            categories=categories,
            page=page,
            total_pages=total_pages,
            user_lang=user_lang,
        ).build()

    def _build_resource_list_keyboard(self, resources, user_lang, total_pages, page):
        return FavoritesResourceListKeyboard(
            resources=resources,
            page=page,
            total_pages=total_pages,
            user_lang=user_lang,
        ).build()

    def _build_resource_item_keyboard(
        self,
        resources,
        resource,
        user_lang,
        is_favorite,
        rating,
    ):
        return FavoritesResourceItemKeyboard(
            resources=resources,
            resource=resource,
            user_lang=user_lang,
            is_favorite=is_favorite,
            rating=rating,
        ).build()

    def _register_handlers(self):
        self.router.callback_query(F.data == "list_favorites")(self.on_list_favorites)
        self.router.callback_query(
            ListFavoritesChooseCategoryCallbackFactory.filter(
                F.action == "change_page",
            ),
        )(self.on_category_page)
        self.router.callback_query(
            ListFavoritesChooseCategoryCallbackFactory.filter(F.action == "select"),
        )(self.on_category_select)
        self.router.callback_query(
            ListFavoritesChooseResourceCallbackFactory.filter(
                F.action == "change_page",
            ),
        )(self.on_resource_page)
        self.router.callback_query(
            ListFavoritesChooseResourceCallbackFactory.filter(F.action == "select"),
        )(self.on_resource_select)
        self.router.callback_query(
            ListFavoritesItemCallbackFactory.filter(F.action == "change_page"),
        )(self.on_resource_item_page)
        self.router.callback_query(
            ListFavoritesItemCallbackFactory.filter(F.action == "add_favorite"),
        )(self.on_add_favorite)
        self.router.callback_query(
            ListFavoritesItemCallbackFactory.filter(F.action == "remove_favorite"),
        )(self.on_remove_favorite)
        self.router.callback_query(
            ListFavoritesItemCallbackFactory.filter(F.action == "rate"),
        )(self.on_rate)

    async def on_list_favorites(self, callback: CallbackQuery, state: FSMContext):
        if not callback.from_user or not callback.from_user.language_code or not callback.message:
            return
        await self._delete_message(callback.message)
        await self._show_category_list(
            message=callback.message,
            state=state,
            user_id=str(callback.from_user.id),
            user_lang=callback.from_user.language_code,
            empty_text_key="list_favorites.no_results",
            choose_text_key="list_favorites.choose_category",
            translate_fn=t,
        )

    async def on_category_page(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesChooseCategoryCallbackFactory,
    ):
        if not callback.from_user or not callback.from_user.language_code or not callback.message:
            return
        await self._delete_message(callback.message)
        page = callback_data.page
        data = await state.get_data()
        categories = data["categories"][
            (page - 1) * LIST_RESOURCES_CATEGORIES_ON_PAGE : page * LIST_RESOURCES_CATEGORIES_ON_PAGE
        ]
        await callback.message.answer(
            text=t("list_favorites.choose_category", callback.from_user.language_code),
            reply_markup=self._build_category_list_keyboard(
                categories=categories,
                user_lang=callback.from_user.language_code,
                total_pages=data["total_categories_pages"],
                page=page,
            ),
        )

    async def on_category_select(
        self,
        callback: CallbackQuery,
        callback_data: ListFavoritesChooseCategoryCallbackFactory,
        state: FSMContext,
    ):
        if not callback.from_user or not callback.from_user.language_code or not callback.message:
            return
        await self._delete_message(callback.message)
        await self._show_resource_list(
            message=callback.message,
            state=state,
            user_id=str(callback.from_user.id),
            category_id=callback_data.category_id,
            user_lang=callback.from_user.language_code,
            text_key="list_favorites.choose_resource",
            translate_fn=t,
        )

    async def on_resource_page(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesChooseResourceCallbackFactory,
    ):
        if not callback.from_user or not callback.from_user.language_code or not callback.message:
            return
        await self._delete_message(callback.message)
        page = callback_data.page
        data = await state.get_data()
        resources = data["resources"][
            (page - 1) * LIST_RESOURCES_RESOURCES_ON_PAGE : page * LIST_RESOURCES_RESOURCES_ON_PAGE
        ]
        await callback.message.answer(
            text=t("list_favorites.choose_resource", callback.from_user.language_code),
            reply_markup=self._build_resource_list_keyboard(
                resources=resources,
                user_lang=callback.from_user.language_code,
                total_pages=data["total_resources_pages"],
                page=page,
            ),
        )

    async def _get_resource_and_state(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        resource_id,
    ):
        resource = await ResourceManager.get_one(resource_id=resource_id)
        if not resource:
            return None, None
        state_data = await state.get_data()
        return resource, state_data

    async def on_resource_select(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesChooseResourceCallbackFactory,
    ):
        if (
            not callback.from_user
            or not callback.from_user.language_code
            or not callback.message
            or not callback_data.resource_id
        ):
            return
        resource, state_data = await self._get_resource_and_state(
            callback,
            state,
            callback_data.resource_id,
        )
        if not resource:
            return
        user_id = str(callback.from_user.id)
        resources = await ResourceManager.get_many(
            category_id=state_data["category_id"],
            favorites_user_id=user_id,
        )
        await state.update_data(resources=resources)
        await self._send_resource_photo(
            message=callback.message,
            resource=resource,
            resources=resources,
            user_id=user_id,
            user_lang=callback.from_user.language_code,
        )

    async def on_resource_item_page(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesItemCallbackFactory,
    ):
        if (
            not callback.from_user
            or not callback.from_user.language_code
            or not callback.message
            or not callback_data.resource_id
        ):
            return
        await self._delete_message(callback.message)
        resource, state_data = await self._get_resource_and_state(
            callback,
            state,
            callback_data.resource_id,
        )
        if not resource:
            return
        await self._send_resource_photo(
            message=callback.message,
            resource=resource,
            resources=state_data["resources"],
            user_id=str(callback.from_user.id),
            user_lang=callback.from_user.language_code,
        )

    async def on_add_favorite(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesItemCallbackFactory,
    ):
        if (
            not callback.from_user
            or not callback.from_user.language_code
            or not callback.message
            or not callback_data.resource_id
        ):
            return
        await self._delete_message(callback.message)
        resource, state_data = await self._get_resource_and_state(
            callback,
            state,
            callback_data.resource_id,
        )
        if not resource:
            return
        user_id = str(callback.from_user.id)
        await self._handle_add_favorite(user_id=user_id, resource_id=resource.resource_item_id)
        await self._send_resource_photo(
            message=callback.message,
            resource=resource,
            resources=state_data["resources"],
            user_id=user_id,
            user_lang=callback.from_user.language_code,
        )

    async def on_remove_favorite(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesItemCallbackFactory,
    ):
        if (
            not callback.from_user
            or not callback.from_user.language_code
            or not callback.message
            or not callback_data.resource_id
        ):
            return
        await self._delete_message(callback.message)
        resource, state_data = await self._get_resource_and_state(
            callback,
            state,
            callback_data.resource_id,
        )
        if not resource:
            return
        user_id = str(callback.from_user.id)
        await self._handle_remove_favorite(user_id=user_id, resource_id=resource.resource_item_id)
        await self._send_resource_photo(
            message=callback.message,
            resource=resource,
            resources=state_data["resources"],
            user_id=user_id,
            user_lang=callback.from_user.language_code,
        )

    async def on_rate(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: ListFavoritesItemCallbackFactory,
    ):
        if (
            not callback.from_user
            or not callback.from_user.language_code
            or not callback.message
            or not callback_data.resource_id
            or not callback_data.rating
        ):
            return
        await self._delete_message(callback.message)
        resource, state_data = await self._get_resource_and_state(
            callback,
            state,
            callback_data.resource_id,
        )
        if not resource:
            return
        user_id = str(callback.from_user.id)
        await self._handle_rate(
            user_id=user_id,
            resource_id=resource.resource_item_id,
            rating=callback_data.rating,
        )
        await self._send_resource_photo(
            message=callback.message,
            resource=resource,
            resources=state_data["resources"],
            user_id=user_id,
            user_lang=callback.from_user.language_code,
        )


list_favorites_router = ListFavoritesRouter()
