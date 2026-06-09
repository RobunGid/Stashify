from typing import List, Literal, Union

from aiogram.filters.callback_data import CallbackData

from pydantic import UUID4

from keyboards.base import BaseListKeyboard
from schemas.category_schema import CategorySchema


class ListFavoritesChooseCategoryCallbackFactory(
    CallbackData,
    prefix="list_favorites_ctg",
):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID4 | None
    page: int


class FavoritesCategoryListKeyboard(BaseListKeyboard):
    def __init__(
        self,
        categories: List[CategorySchema],
        page: int,
        total_pages: int,
        user_lang: str = "en",
    ):
        super().__init__(user_lang)
        self.categories = categories
        self.page = page
        self.total_pages = total_pages

    def _back_callback(self) -> str:
        return "menu"

    def _page_callback(self, page: int) -> ListFavoritesChooseCategoryCallbackFactory:
        return ListFavoritesChooseCategoryCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def build(self):
        for category in self.categories:
            self.builder.button(
                text=category.name,
                callback_data=ListFavoritesChooseCategoryCallbackFactory(
                    action="select",
                    category_id=category.category_id,
                    page=0,
                ),
            )

        pagination_count = self.build_page_buttons(
            builder=self.builder,
            callback_factory_fn=self._page_callback,
            page=self.page,
            total_pages=self.total_pages,
            user_lang=self.user_lang,
        )

        self._add_back_button()
        self.builder.adjust(*([1] * len(self.categories)), pagination_count, 2)
        return self.builder.as_markup()
