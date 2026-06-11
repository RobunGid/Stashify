from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from keyboards.base import (
    BaseBackKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
)
from schemas.category_item_schema import CategoryItemSchema


@dataclass
class EntryEditCategoryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-categories-keyboard-create"),
                "callback_data": "create_category",
            },
            {
                "text": self.i18n.get("manage-categories-keyboard-edit"),
                "callback_data": "edit_category",
            },
            {
                "text": self.i18n.get("manage-categories-keyboard-delete"),
                "callback_data": "delete_category",
            },
        ]

    def _back_callback(self) -> str:
        return "menu"


class DeleteCategoryIdCallbackFactory(CallbackData, prefix="delete_category_id"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


class DeleteCategoryKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str | CallbackData | None:
        return DeleteCategoryIdCallbackFactory(
            action="change_page",
            category_id=None,
            page=self.current_page - 1,
        )

    def _pagination_callback(self, page: int) -> CallbackData:
        return DeleteCategoryIdCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteCategoryIdCallbackFactory(
                action="select",
                category_id=item.category_id,
                page=0,
            ),
        }


class EditCategoryIdCallbackFactory(CallbackData, prefix="edit_category_id"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


@dataclass
class EditCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str | CallbackData | None:
        return EditCategoryIdCallbackFactory(
            action="change_page",
            category_id=None,
            page=self.current_page - 1,
        )

    def _pagination_callback(self, page: int) -> CallbackData:
        return EditCategoryIdCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditCategoryIdCallbackFactory(
                action="select",
                category_id=item.category_id,
                page=0,
            ),
        }


@dataclass
class ManageCategoriesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_categories"
