from dataclasses import dataclass
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackKeyboardBuilderMixin,
    BackToMenuKeyboardBuilderMixin,
    BaseBackKeyboardBuilder,
    BaseConfirmKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
)
from application.keyboards.resources import ListCategoriesItemCallbackFactory
from application.schemas.category_item_schema import CategoryItemSchema
from domain.entities.category_item import CategoryItemEntity


@dataclass
class EntryEditCategoryKeyboardBuilder(BaseManageEntryKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
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


class DeleteCategoryChooseCategoryCallbackFactory(CallbackData, prefix="delete_category_id"):  # type: ignore[call-arg]
    category_item_id: UUID


@dataclass
class DeleteCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity]):
    def _back_callback(self) -> str:
        return "manage_categories"

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="dlt_ctg",
        )

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteCategoryChooseCategoryCallbackFactory(
                category_item_id=item.category_item_id,
            ),
        }


class EditCategoryChooseCategoryCallbackFactory(CallbackData, prefix="edit_category_id"):  # type: ignore[call-arg]
    category_item_id: UUID | None


@dataclass
class ManageCategoriesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_categories"


@dataclass
class ManageCategoriesBackKeyboardBuilderMixin(BackKeyboardBuilderMixin):
    def _back_callback(self) -> str:
        return "manage_categories"


@dataclass
class EditCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    ManageCategoriesBackKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="edt_ctg",
        )

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditCategoryChooseCategoryCallbackFactory(
                category_item_id=item.category_item_id,
            ),
        }


class DeleteCategoryConfirmCallbackFactory(CallbackData, prefix="dlt_ctg_cnfrm"):  # type: ignore[call-arg]
    category_item_id: UUID


@dataclass
class DeleteCategoryConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder):
    category_item_id: UUID

    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get(
                    "manage-category-delete-confirm",
                ),
                "callback_data": DeleteCategoryConfirmCallbackFactory(category_item_id=self.category_item_id),
            },
        ]

    def _back_callback(self) -> str:
        return "manage_resources"
