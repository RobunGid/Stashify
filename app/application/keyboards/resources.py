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
from application.schemas.category_item_schema import CategoryItemSchema
from application.schemas.resource_schema import ResourceItemSchema


class ListResourcesChooseResourceCallbackFactory(CallbackData, prefix="lst_rsc_rsc"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


@dataclass
class ResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema]):
    def _back_callback(self) -> str:
        return "resources"

    def _item_button(self, item: ResourceItemSchema) -> dict:
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
class CategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _back_callback(self) -> str:
        return "menu"

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_item - id,
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
class ResourceItemKeyboardBuilder(BaseItemKeyboardBuilder[ResourceItemSchema]):
    def _get_item_id(self, item: ResourceItemSchema) -> UUID:
        return item.resource_item_id

    def _navigation_callback(self, item: ResourceItemSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="change_page",
            rating=None,
        )

    def _remove_favorite_callback(self, item: ResourceItemSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="remove_favorite",
            rating=None,
        )

    def _add_favorite_callback(self, item: ResourceItemSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="add_favorite",
            rating=None,
        )

    def _rating_callback(self, item: ResourceItemSchema, rating: int) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="rate",
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
                "callback_data": ListResourcesItemCallbackFactory(
                    action="start_quiz",
                    rating=None,
                    resource_item_id=self.current_item.resource_item_id,
                ),
            },
        ]

    def _build_quiz_confirm_buttons(self) -> dict:
        return {
            "callback_data": ListResourcesItemCallbackFactory(
                resource_item_id=self.current_item.resource_item_id,
                action="start_quiz_cnfrm",
                rating=None,
            ),
            "text": self.i18n.get("list-resources-start-quiz-confirm"),
        }

    def _back_callback(self) -> CallbackData:
        return ListResourcesChooseCategoryCallbackFactory(
            action="select",
            category_id=self.current_item.category_id,
            page=0,
        )


@dataclass
class ResourceQuizConfirmKeyboardBuilder(BaseQuizConfirmKeyboardBuilder[ResourceItemSchema]):
    def _navigation_callback(self, item: ResourceItemSchema) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            resource_item_id=item.resource_item_id,
            action="change_page",
            rating=None,
        )

    def _build_confirm_buttons(
        self,
    ) -> list[dict]:
        return [
            {
                "callback_data": ListResourcesItemCallbackFactory(
                    action="start_quiz_cnfrm",
                    resource_item_id=self.current_item.resource_item_id,
                    rating=None,
                ),
                "text": self.i18n.get("ist-resources-start_quiz-confirm"),
            },
        ]

    def _back_callback(self) -> CallbackData:
        return ListResourcesItemCallbackFactory(
            action="change_page",
            resource_item_id=self.current_item.resource_item_id,
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


@dataclass
class ResourceManageBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_resources"


class CreateResourceCallbackFactory(CallbackData, prefix="create_resource"):  # type: ignore[call-arg]
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


@dataclass
class CreateResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema], ABC):
    def _pagination_callback(self, page: int) -> CallbackData:
        return CreateResourceCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": CreateResourceCallbackFactory(
                action="select",
                category_id=item.category_item - id,
                page=0,
            ),
        }


@dataclass
class ManageResourcesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str | CallbackData | None:
        return "manage_resources"


class DeleteResourceChooseCategoryCallbackFactory(
    CallbackData,
    prefix="delete_resource_ctg",  # type: ignore[call-arg]
):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


@dataclass
class DeleteResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema], ABC):
    def _pagination_callback(self, page: int) -> CallbackData:
        return DeleteResourceChooseCategoryCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: CategoryItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteResourceChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_item - id,
                page=0,
            ),
        }


class DeleteResourceChooseResourceCallbackFactory(
    CallbackData,
    prefix="delete_resource_rsc",  # type: ignore[call-arg]
):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


@dataclass
class DeleteResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema], ABC):
    def _pagination_callback(self, page: int) -> CallbackData:
        return DeleteResourceChooseResourceCallbackFactory(
            action="change_page",
            resource_item_id=None,
            page=page,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": DeleteResourceChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
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


class EditResourceChooseCategoryCallbackFactory(
    CallbackData,
    prefix="edit_resource_ctg",  # type: ignore[call-arg]
):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID | None
    page: int


@dataclass
class EditResourceCategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemSchema]):
    def _pagination_callback(self, page: int) -> CallbackData:
        return EditResourceChooseCategoryCallbackFactory(
            action="change_page",
            category_id=None,
            page=page,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditResourceChooseCategoryCallbackFactory(
                action="select",
                category_id=item.category_id,
                page=0,
            ),
        }


class EditResourceChooseResourceCallbackFactory(
    CallbackData,
    prefix="edit_resource_rsc",  # type: ignore[call-arg]
):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_item_id: UUID | None
    page: int


@dataclass
class EditResourceResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemSchema]):
    def _pagination_callback(self, page: int) -> CallbackData:
        return EditResourceChooseResourceCallbackFactory(
            action="change_page",
            resource_item_id=None,
            page=page,
        )

    def _back_callback(self) -> str:
        return "manage_resources"

    def _item_button(self, item: ResourceItemSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": EditResourceChooseResourceCallbackFactory(
                action="select",
                resource_item_id=item.resource_item_id,
                page=0,
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
