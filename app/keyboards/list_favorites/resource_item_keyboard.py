from typing import List, Literal, Union

from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema
from keyboards.base import BaseItemKeyboard


class ListFavoritesItemCallbackFactory(CallbackData, prefix="lst_fvrt_itm"):
    action: Union[Literal["change_page"], Literal["add_favorite"], Literal["remove_favorite"], Literal["rate"]]
    resource_id: UUID4 | None
    rating: int | None


class FavoritesResourceItemKeyboard(BaseItemKeyboard):
    def __init__(
        self,
        resources: List[ResourceSchema],
        resource: ResourceSchema,
        user_lang: str = "en",
        is_favorite: bool = False,
        rating: int = 0,
    ):
        super().__init__(user_lang)
        self.resources = resources
        self.resource = resource
        self.is_favorite = is_favorite
        self.rating = rating

    def _back_callback(self) -> str:
        return "list_favorites"

    def _nav_callback(self, resource_id) -> ListFavoritesItemCallbackFactory:
        return ListFavoritesItemCallbackFactory(action="change_page", resource_id=resource_id, rating=0)

    def build(self):
        resources = self.resources
        index = resources.index(self.resource)
        total = len(resources)
        is_first, is_last = self._resolve_item_nav(index, total)

        if not is_first:
            self.builder.button(text=t("items.start", self.user_lang), callback_data=self._nav_callback(resources[0].id))
            self.builder.button(text=t("items.back", self.user_lang), callback_data=self._nav_callback(resources[index - 1].id))

        self.builder.button(text=f"{index + 1}/{total}", callback_data=" ")

        if not is_last:
            self.builder.button(text=t("items.forward", self.user_lang), callback_data=self._nav_callback(resources[index + 1].id))
            self.builder.button(text=t("items.end", self.user_lang), callback_data=self._nav_callback(resources[-1].id))

        if is_first and is_last:
            pagination_count = 1
        elif is_first or is_last:
            pagination_count = 3
        else:
            pagination_count = 5

        self._add_back_button()

        if self.is_favorite:
            self.builder.button(
                text=t("favorite.remove", self.user_lang),
                callback_data=ListFavoritesItemCallbackFactory(action="remove_favorite", resource_id=self.resource.id, rating=0),
            )
        else:
            self.builder.button(
                text=t("favorite.add", self.user_lang),
                callback_data=ListFavoritesItemCallbackFactory(action="add_favorite", resource_id=self.resource.id, rating=0),
            )

        for i in range(1, 6):
            symbol = "⭐" if i <= self.rating else "☆"
            self.builder.button(
                text=symbol,
                callback_data=ListFavoritesItemCallbackFactory(action="rate", resource_id=self.resource.id, rating=i),
            )

        self.builder.adjust(pagination_count, 2, 5)
        return self.builder.as_markup()