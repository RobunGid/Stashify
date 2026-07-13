from abc import ABC
from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackToMenuKeyboardBuilderMixin,
    BackToSearchResourcesKeyboardBuilderMixin,
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
        Literal["menu"],
        Literal["crt_rsc"],
        Literal["edt_rsc"],
        Literal["dlt_rsc"],
        Literal["edt_ctg"],
        Literal["dlt_ctg"],
        Literal["crt_quiz"],
        Literal["dlt_quiz"],
        Literal["crt_quiz_qstn"],
        Literal["edt_quiz_qstn"],
        Literal["dlt_quiz_qstn"],
    ]


class ListCategoryResourcesItemCallbackFactory(CallbackData, prefix="rsc_lst"):  # type: ignore[call-arg]
    category_item_id: UUID
    page: int
    context: Union[
        Literal["menu"],
        Literal["edt_rsc"],
        Literal["dlt_rsc"],
        Literal["dlt_quiz"],
        Literal["crt_quiz"],
        Literal["edt_quiz_qst"],
        Literal["crt_quiz_qst"],
        Literal["dlt_quiz_qst"],
    ]


class ListSearchResourcesItemCallbackFactory(CallbackData, prefix="rsc_lst"):  # type: ignore[call-arg]
    query: str
    page: int
    context: Union[Literal["menu"], Literal["..."]]


class ResourceItemDetailsCallbackFactory(CallbackData, prefix="rsc_itm"):  # type: ignore[call-arg]
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
        Literal["menu"],
        Literal["srch"],
    ]
    rating: int | None


@dataclass
class CategoryResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceItemEntity]):
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
class SearchResourceListKeyboardBuilder(
    BaseListKeyboardBuilder[ResourceItemEntity],
    BackToSearchResourcesKeyboardBuilderMixin,
):
    query: str

    def _item_button(self, item: ResourceItemEntity) -> dict:
        return {
            "text": item.name,
            "callback_data": ResourceItemDetailsCallbackFactory(
                resource_item_id=item.resource_item_id,
                action="select",
                context="srch",
                rating=None,
            ).pack(),
        }

    def _pagination_callback(self, page: int) -> str:
        return ListSearchResourcesItemCallbackFactory(
            page=page,
            query=self.query,
            context="menu",
        ).pack()


@dataclass
class CategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategoryItemEntity], BackToMenuKeyboardBuilderMixin):
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


@dataclass
class ResourceItemKeyboardBuilder(BaseItemKeyboardBuilder[ResourceItemEntity]):
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
            context="menu",
            page=0,
        ).pack()


@dataclass
class ResourceQuizConfirmKeyboardBuilder(BaseQuizConfirmKeyboardBuilder[ResourceItemEntity]):
    def _navigation_callback(self, item: ResourceItemEntity) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=item.category_item_id,
            page=0,
            context="menu",
        ).pack()

    def _build_confirm_buttons(
        self,
    ) -> list[dict]:
        return [
            {
                "callback_data": ResourceItemDetailsCallbackFactory(
                    action="start_quiz_cnfrm",
                    resource_item_id=self.current_item.resource_item_id,
                    rating=None,
                    context="menu",
                ),
                "text": self.i18n.get("ist-resources-start_quiz-confirm"),
            },
        ]

    def _back_callback(self) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            category_item_id=self.current_item.category_item_id,
            page=0,
            context="menu",
        ).pack()


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


class CreateResourceCallbackFactory(CallbackData, prefix="crt_rsc"):  # type: ignore[call-arg]
    category_item_id: UUID


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
class ManageResourcesBackKeyboardBuilder(BaseBackKeyboardBuilder):
    def _back_callback(self) -> str:
        return "manage_resources"


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
