from abc import ABC
from dataclasses import dataclass
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackToMenuKeyboardBuilderMixin,
    BaseBackKeyboardBuilder,
    BaseConfirmKeyboardBuilder,
    BaseEditKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
)
from application.keyboards.resources import ListCategoriesItemCallbackFactory, ListCategoryResourcesItemCallbackFactory
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


class CreateResourceCallbackFactory(CallbackData, prefix="crt_rsc"):  # type: ignore[call-arg]
    category_item_id: UUID


@dataclass
class ManageResourcesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str:
        return "manage_resources"


@dataclass
class CreateResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], ABC):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="crt_rsc",
        ).pack()

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": CreateResourceCallbackFactory(category_item_id=item.category_item_id).pack(),
        }


@dataclass
class DeleteResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], ABC):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="dlt_rsc",
        ).pack()

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                page=0,
                context="dlt_rsc",
                category_item_id=item.category_item_id,
            ).pack(),
        }


class DeleteResourceChooseResourceCallbackFactory(CallbackData, prefix="dlt_rsc"):  # type: ignore[call-arg]
    resource_item_id: UUID


class EditResourceChooseResourceCallbackFactory(CallbackData, prefix="edt_rsc"):  # type: ignore[call-arg]
    resource_item_id: UUID


@dataclass
class DeleteResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity], ABC):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.category_item_id,
            page=page,
            context="dlt_rsc",
        ).pack()

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteResourceChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ).pack(),
        }


class DeleteResourceConfirmCallbackFactory(CallbackData, prefix="dlt_rsc_cnfrm"):  # type: ignore[call-arg]
    resource_item_id: UUID


@dataclass
class DeleteResourceConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder):
    resource_item_id: UUID

    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get(
                    "manage-resources-delete-confirm",
                ),
                "callback_data": DeleteResourceConfirmCallbackFactory(resource_item_id=self.resource_item_id),
            },
        ]

    def _back_callback(self) -> str:
        return "manage_resources"


@dataclass
class EditResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity]):
    def _pagination_callback(self, page: int) -> str:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="edt_rsc",
        ).pack()

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": f"{item.name} ({item.resource_item_count})",
            "callback_data": ListCategoryResourcesItemCallbackFactory(
                page=0,
                context="edt_rsc",
                category_item_id=item.category_item_id,
            ).pack(),
        }


@dataclass
class EditResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            page=page,
            context="edt_rsc",
            category_item_id=self.category_item_id,
        ).pack()

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": EditResourceChooseResourceCallbackFactory(
                resource_item_id=item.resource_item_id,
            ).pack(),
        }


@dataclass
class EditResourceChooseFieldKeyboardBuilder(BaseEditKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
    def _build_edit_buttons(self) -> list[dict]:
        return [
            {"text": self.i18n.get("manage-resources-edit-name-choose"), "callback_data": "edit_resource_name"},
            {
                "text": self.i18n.get("manage-resources-edit-description-choose"),
                "callback_data": "edit_resource_description",
            },
            {"text": self.i18n.get("manage-resources-edit-image-choose"), "callback_data": "edit_resource_image"},
            {"text": self.i18n.get("manage-resources-edit-tags-choose"), "callback_data": "edit_resource_tags"},
        ]


@dataclass
class ResourceManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-resources-keyboard-create"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="crt_rsc",
                    page=0,
                ).pack(),
            },
            {
                "text": self.i18n.get("manage-resources-keyboard-edit"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="edt_rsc",
                    page=0,
                ).pack(),
            },
            {
                "text": self.i18n.get("manage-resources-keyboard-delete"),
                "callback_data": ListCategoriesItemCallbackFactory(
                    action="change_page",
                    context="dlt_rsc",
                    page=0,
                ).pack(),
            },
        ]


@dataclass
class ResourceManageBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_resources"
