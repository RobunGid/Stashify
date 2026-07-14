from dataclasses import dataclass
from uuid import UUID

from application.keyboards.base import BaseItemKeyboardBuilder, BaseListKeyboardBuilder
from application.keyboards.resources import (
    ListCategoriesItemCallbackFactory,
    ListCategoryResourcesItemCallbackFactory,
    ResourceItemDetailsCallbackFactory,
)
from domain.entities.resource_item import ResourceItemEntity


@dataclass
class FavoriteCategoryResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return ListCategoriesItemCallbackFactory(action="change_page", context="favorites", page=0).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=item.resource_item_id,
                action="select",
                context="favorites",
                rating=None,
            ).pack(),
        }

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            page=page,
            category_item_id=self.category_item_id,
            context="favorites",
        ).pack()


@dataclass
class FavoriteResourceItemKeyboardBuilder(BaseItemKeyboardBuilder[ResourceItemEntity]):
    query: str

    def _get_item_id(self, item: ResourceItemEntity) -> UUID:
        return item.resource_item_id

    def _navigation_callback(self, item_id: UUID) -> str:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item_id,
            action="select",
            context="menu",
            rating=None,
        ).pack()

    def _remove_favorite_callback(self, item: ResourceItemEntity) -> str:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="remove_favorite",
            context="menu",
            rating=None,
        ).pack()

    def _add_favorite_callback(self, item: ResourceItemEntity) -> str:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="add_favorite",
            context="menu",
            rating=None,
        ).pack()

    def _rating_callback(self, item: ResourceItemEntity, rating: int) -> str:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="rate",
            context="menu",
            rating=rating,
        ).pack()

    def _build_quiz_buttons(self) -> list[dict]:
        if not self.has_quiz:
            return []
        if self.quiz_percent:
            text = self.i18n.get("start-quiz-completed", percent=self.quiz_percent)
        else:
            text = self.i18n.get("start-quiz-firstly")
        return [
            {
                "text": text,
                "callback_data": ResourceItemDetailsCallbackFactory(
                    action="start_quiz",
                    rating=None,
                    resource_item_id=self.current_item.resource_item_id,
                    context="menu",
                ).pack(),
            },
        ]

    def _build_quiz_confirm_buttons(self) -> dict:
        return {
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=self.current_item.resource_item_id,
                action="start_quiz_cnfrm",
                rating=None,
                context="menu",
            ),
            "text": self.i18n.get("list-resources-start-quiz-confirm"),
        }

    def _back_callback(self) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.current_item.category_item_id,
            context="favorites",
            page=0,
        ).pack()
