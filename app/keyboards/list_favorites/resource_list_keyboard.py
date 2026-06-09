from typing import List, Literal, Union

from aiogram.filters.callback_data import CallbackData

from pydantic import UUID4

from keyboards.base import BaseListKeyboard
from schemas.resource_schema import ResourceSchema


class ListFavoritesChooseResourceCallbackFactory(
    CallbackData,
    prefix="list_favorites_rsc",
):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_id: UUID4 | None
    page: int


class FavoritesResourceListKeyboard(BaseListKeyboard):
    def __init__(
        self,
        resources: List[ResourceSchema],
        page: int,
        total_pages: int,
        user_lang: str = "en",
    ):
        super().__init__(user_lang)
        self.resources = resources
        self.page = page
        self.total_pages = total_pages

    def _back_callback(self) -> str:
        return "list_favorites"

    def _page_callback(self, page: int) -> ListFavoritesChooseResourceCallbackFactory:
        return ListFavoritesChooseResourceCallbackFactory(
            action="change_page",
            resource_id=None,
            page=page,
        )

    def build(self):
        for resource in self.resources:
            self.builder.button(
                text=resource.name,
                callback_data=ListFavoritesChooseResourceCallbackFactory(
                    action="select",
                    resource_id=resource.resource_id,
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
        self.builder.adjust(len(self.resources), pagination_count, 2, 5)
        return self.builder.as_markup()
