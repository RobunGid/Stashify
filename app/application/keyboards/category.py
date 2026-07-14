from dataclasses import dataclass
from uuid import UUID

from application.keyboards.base import BackToMenuKeyboardBuilderMixin, BaseListKeyboardBuilder
from application.keyboards.resources import (
    ListCategoriesItemCallbackFactory,
    ListCategoryResourcesItemCallbackFactory,
    ResourceItemDetailsCallbackFactory,
)
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


@dataclass
class ListResourcesCategoryResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return ListCategoriesItemCallbackFactory(action="change_page", context="menu", page=0).pack()

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=item.resource_item_id,
                action="select",
                context="menu",
                rating=None,
            ).pack(),
        }

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            page=page,
            category_item_id=self.category_item_id,
            context="menu",
        ).pack()


@dataclass
class FavoriteCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], BackToMenuKeyboardBuilderMixin):
    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="favorites",
            ).pack(),
        }

    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="favorites",
        ).pack()


@dataclass
class ListResourcesCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    BackToMenuKeyboardBuilderMixin,
):
    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="menu",
            ).pack(),
        }

    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="menu",
        ).pack()
