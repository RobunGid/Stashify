from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BackToSearchResourcesKeyboardBuilderMixin,
    BaseItemKeyboardBuilder,
    BaseListKeyboardBuilder,
    BaseQuizConfirmKeyboardBuilder,
)
from domain.entities.resource_item import ResourceItemEntity


class ListCategoriesItemCallbackFactory(CallbackData, prefix="ctg_lst"):  # type: ignore[call-arg]
    action: Literal["change_page"]
    page: int
    context: Union[
        Literal["menu"],
        Literal["favorites"],
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


class ListCategoryResourcesItemCallbackFactory(CallbackData, prefix="rsc_lst_ctg"):  # type: ignore[call-arg]
    category_item_id: UUID
    page: int
    context: Union[
        Literal["menu"],
        Literal["favorites"],
        Literal["edt_rsc"],
        Literal["dlt_rsc"],
        Literal["dlt_quiz"],
        Literal["crt_quiz"],
        Literal["edt_quiz_qst"],
        Literal["crt_quiz_qst"],
        Literal["dlt_quiz_qst"],
    ]


class ListSearchResourcesItemCallbackFactory(CallbackData, prefix="rsc_lst_srch"):  # type: ignore[call-arg]
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
    context: Union[Literal["menu"], Literal["srch"], Literal["favorites"]]
    rating: int | None


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
