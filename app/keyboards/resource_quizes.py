from dataclasses import dataclass

from aiogram.filters.callback_data import CallbackData

from keyboards.base import BaseManageEntryKeyboardBuilder, BaseQuizFinalKeyboardBuilder
from keyboards.resources import ListResourcesChooseResourceCallbackFactory, ListResourcesItemCallbackFactory
from schemas.resource_schema import ResourceSchema


@dataclass
class ResourceQuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {"text": self.i18n.get("manage-quizes-keyboard-create"), "callback_data": "create_quiz"},
            {"text": self.i18n.get("manage-quizes-keyboard-edit"), "callback_data": "edit_quiz"},
            {"text": self.i18n.get("manage-quizes-keyboard-delete"), "callback_data": "delete_quiz"},
        ]

    def _back_callback(self) -> str:
        return "menu"


@dataclass
class ResourceQuizFinalKeyboardBuilder(BaseQuizFinalKeyboardBuilder[ResourceSchema]):
    def _build_retry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("start-quiz-retry"),
                "callback_data": ListResourcesItemCallbackFactory(
                    action="start_quiz",
                    resource_item_id=self.item.resource_item_id,
                    rating=0,
                ),
            },
        ]

    def _back_callback(self) -> CallbackData:
        return ListResourcesChooseResourceCallbackFactory(
            action="change_page",
            page=self.page,
            resource_item_id=self.item.resource_item_id,
        )
