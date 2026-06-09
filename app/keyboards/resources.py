from typing import Literal, Union

from aiogram.filters.callback_data import CallbackData

from pydantic import UUID4

from schemas.category_schema import CategorySchema
from schemas.resource_schema import ResourceSchema
from keyboards.base import BaseListKeyboardBuilder


class ListResourcesChooseResourceCallbackFactory(CallbackData, prefix="lst_rsc_rsc"):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_id: UUID4 | None
    page: int


class ListResourcesChooseCategoryCallbackFactory(
    CallbackData,
    prefix="list_resources_ctg",
):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID4 | None
    page: int


class ResourceListKeyboardBuilder(BaseListKeyboardBuilder[ResourceSchema]):
    def _back_callback(self) -> str:
        return "resources"

    def _item_button(self, item: ResourceSchema) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesChooseResourceCallbackFactory(
                action="select", resource_id=item.resource_id, page=0
            ),
        }


class CategoryListKeyboardBuilder(BaseListKeyboardBuilder[CategorySchema]):
    def _back_callback(self) -> str:
        return "menu"

    def _item_button(self, item: CategorySchema) -> dict:
        return {
            "text": item.name,
            "callback_data": ListResourcesChooseCategoryCallbackFactory(
                action="select", category_id=item.category_id, page=0
            ),
        }
