from dataclasses import dataclass
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackToMenuKeyboardBuilderMixin,
    BaseBackKeyboardBuilder,
    BaseBackKeyboardBuilderMixin,
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
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="edt_ctg",
                    page=0,
                ).pack(),
            },
            {
                "text": self.i18n.get("manage-categories-keyboard-delete"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="dlt_ctg",
                    page=0,
                ).pack(),
            },
        ]


class DeleteCategoryChooseCategoryCallbackFactory(CallbackData, prefix="delete_category_id"):  # type: ignore[call-arg]
    category_item_id: UUID


@dataclass
class DeleteCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity]):
    def _back_callback(self) -> str:
        return "manage_categories"

    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="dlt_ctg",
        ).pack()

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": DeleteCategoryChooseCategoryCallbackFactory(
                category_item_id=item.category_item_id,
            ).pack(),
        }


class EditCategoryChooseCategoryCallbackFactory(CallbackData, prefix="edit_category_id"):  # type: ignore[call-arg]
    category_item_id: UUID


@dataclass
class ManageCategoriesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str:
        return "manage_categories"


@dataclass
class ManageCategoriesBackKeyboardBuilderMixin(BaseBackKeyboardBuilderMixin):
    def _back_callback(self) -> str:
        return "manage_categories"


@dataclass
class EditCategoryListKeyboardBuilder(
    BaseListKeyboardBuilder[CategoryItemEntity],
    ManageCategoriesBackKeyboardBuilderMixin,
):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="edt_ctg",
        ).pack()

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": EditCategoryChooseCategoryCallbackFactory(
                category_item_id=item.category_item_id,
            ).pack(),
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
                    "manage-categories-delete-confirm",
                ),
                "callback_data": DeleteCategoryConfirmCallbackFactory(category_item_id=self.category_item_id).pack(),
            },
        ]

    def _back_callback(self) -> str:
        return "manage_resources"
