from abc import ABC
from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackToMenuKeyboardBuilderMixin,
    BaseBackKeyboardBuilder,
    BaseConfirmKeyboardBuilder,
    BaseEditKeyboardBuilder,
    BaseItemKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseManageEntryKeyboardBuilder,
    BaseQuizConfirmKeyboardBuilder,
)
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


class ListCategoriesItemCallbackFactory(CallbackData, prefix="ctg_lst"):  # type: ignore[call-arg]
    action: Literal["change_page"]
    page: int
    context: Union[
        Literal["view"],
        Literal["crt_rsc"],
        Literal["edt_rsc"],
        Literal["dlt_rsc"],
        Literal["edt_ctg"],
        Literal["dlt_ctg"],
    ]


class ListResourcesItemCallbackFactory(CallbackData, prefix="rsc_lst"):  # type: ignore[call-arg]
    category_item_id: UUID | None
    page: int
    context: Union[
        Literal["view"],
        Literal["edit"],
        Literal["delete"],
    ]


class ResourceItemDetailsCallbackFactory(CallbackData, prefix="rsc_itm"):
    resource_item_id: UUID | None
    action: Union[
        Literal["select"],
        Literal["add_favorite"],
        Literal["remove_favorite"],
        Literal["rate"],
        Literal["start_quiz"],
        Literal["start_quiz_cnfrm"],
    ]
    context: Union[
        Literal["view"],
        Literal["edit"],
        Literal["delete"],
    ]
    rating: int | None


@dataclass
class ResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _back_callback(self) -> str:
        return "resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=item.resource_item_id,
                action="select",
                context="view",
                rating=None,
            ),
        }

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            page=page,
            category_item_id=self.category_item_id,
            context="view",
        )


@dataclass
class CategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity]):
    def _back_callback(self) -> str:
        return "menu"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="view",
            ),
        }

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="view",
        )


@dataclass
class ResourceItemKeyboardBuilder(BaseItemKeyboardBuilder[ResourceItemEntity]):
    def _get_item_id(self, item: ResourceItemEntity) -> UUID:
        return item.resource_item_id

    def _navigation_callback(self, item_id: UUID) -> CallbackData:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item_id,
            action="select",
            context="view",
            rating=None,
        )

    def _remove_favorite_callback(self, item: ResourceItemEntity) -> CallbackData:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="remove_favorite",
            context="view",
            rating=None,
        )

    def _add_favorite_callback(self, item: ResourceItemEntity) -> CallbackData:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="add_favorite",
            context="view",
            rating=None,
        )

    def _rating_callback(self, item: ResourceItemEntity, rating: int) -> CallbackData:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="rate",
            context="view",
            rating=rating,
        )

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
                    context="view",
                ),
            },
        ]

    def _build_quiz_confirm_buttons(self) -> dict:
        return {
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=self.current_item.resource_item_id,
                action="start_quiz_cnfrm",
                rating=None,
                context="view",
            ),
            "text": self.i18n.get("list-resources-start-quiz-confirm"),
        }

    def _back_callback(self) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            context="view",
            page=0,
        )


@dataclass
class ResourceQuizConfirmKeyboardBuilder(BaseQuizConfirmKeyboardBuilder[ResourceItemEntity]):
    def _navigation_callback(self, item: ResourceItemEntity) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            category_item_id=item.category_item_id,
            page=0,
            context="view",
        )

    def _build_confirm_buttons(
        self,
    ) -> list[dict]:
        return [
            {
                "callback_data": ResourceItemDetailsCallbackFactory(
                    action="start_quiz_cnfrm",
                    resource_item_id=self.current_item.resource_item_id,
                    rating=None,
                    context="view",
                ),
                "text": self.i18n.get("ist-resources-start_quiz-confirm"),
            },
        ]

    def _back_callback(self) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            category_item_id=self.current_item.category_item_id,
            page=0,
            context="view",
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


@dataclass
class ResourceManageBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_resources"


@dataclass
class CreateResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], ABC):
    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="crt_rsc",
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": "create_resource",
        }


@dataclass
class ManageResourcesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_resources"


@dataclass
class DeleteResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], ABC):
    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="dlt_rsc",
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ListCategoriesItemCallbackFactory(
                action="change_page",
                page=0,
                context="dlt_rsc",
            ),
        }


@dataclass
class DeleteResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity], ABC):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            category_item_id=None,
            page=page,
            context="delete",
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesItemCallbackFactory(
                category_item_id=item.category_item_id,
                page=0,
                context="delete",
            ),
        }


@dataclass
class DeleteResourceConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder):
    def _build_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n(
                    "manage-resources-delete-confirm",
                ),
                "callback_data": "delete_resource_confirm",
            },
        ]

    def _back_callback(self) -> str:
        return "manage_resources"


@dataclass
class EditResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity]):
    def _pagination_callback(self, page: int) -> CallbackData:
        return ListCategoriesItemCallbackFactory(
            action="change_page",
            page=page,
            context="edt_rsc",
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ListCategoriesItemCallbackFactory(
                action="change_page",
                page=0,
                context="edt_rsc",
            ),
        }


@dataclass
class EditResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
    category_item_id: UUID

    def _pagination_callback(self, page: int) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            page=page,
            context="edit",
            category_item_id=self.category_item_id,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesItemCallbackFactory(
                category_item_id=self.category_item_id,
                page=0,
                context="edit",
            ),
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
