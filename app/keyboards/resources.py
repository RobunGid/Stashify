from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from keyboards.base import (
    BaseItemKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
    BaseQuizConfirmKeyboardBuilder,
)
from schemas.category_schema import CategorySchema
from schemas.resource_schema import ResourceSchema


class ListResourcesChooseResourceCallbackFactory(CallbackData, prefix="lst_rsc_rsc"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


@dataclass
class ResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceSchema]):
    def _back_callback(self) -> str:
        return "resources"

    def _item_button(self, item: ResourceSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
            ),
        }

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListResourcesChooseResourceCallbackFactory(
            action="change_page",
            resource_item_id=None,
            page=page,
        )


class ListResourcesChooseCategoryCallbackFactory(
    CallbackData,
    prefix="list_resources_ctg",  # type: ignore[call-arg]
):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


@dataclass
class CategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategorySchema]):
    def _back_callback(self) -> str:
        return "menu"

    def _item_button(self, item: CategorySchema) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_id,
                page=0,
            ),
        }

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListResourcesChooseCategoryCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )


class ListResourcesItemCallbackFactory(CallbackData, prefix="lst_rsc_itm"):  # type: ignore[call-arg]
    action: Union[
        Literal["change_page"],
        Literal["add_favorite"],
        Literal["remove_favorite"],
        Literal["rate"],
        Literal["start_quiz"],
        Literal["start_quiz_cnfrm"],
    ]
    resource_item_id: UUID | None
    rating: int | None


@dataclass
class ResourceItemKeyboardBuilder(BaseItemKeyboardBuilder):
    def _get_item_id(self, item: ResourceSchema) -> UUID:
        return item.resource_item_id

    def _navigation_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="change_page",
            rating=None,
        )

    def _remove_favorite_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="remove_favorite",
            rating=None,
        )

    def _add_favorite_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="add_favorite",
            rating=None,
        )

    def _rating_callback(self, item: ResourceSchema, rating: int) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="rate",
            rating=rating,
        )

    def _quiz_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="start_quiz",
            rating=None,
        )

    def _quiz_confirm_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="start_quiz_cnfrm",
            rating=None,
        )


@dataclass
class ResourceQuizConfirmKeyboardBuilder(BaseQuizConfirmKeyboardBuilder[ResourceSchema]):
    def _navigation_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="change_page",
            rating=None,
        )

    def _quiz_confirm_callback(self, item: ResourceSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            action="start_quiz_cnfrm",
            resource_item_id=item.resource_item_id,
            rating=None,
        )


@dataclass
class ResourceManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-resources-keyboard-create"),
                "callback_data": "create_resource",
            },
            {
                "text": self.i18n.get("manage-resources-keyboard-edit"),
                "callback_data": "edit_resource",
            },
            {
                "text": self.i18n.get("manage-resources-keyboard-delete"),
                "callback_data": "delete_resource",
            },
        ]

    def _back_callback(self) -> str:
        return "menu"
