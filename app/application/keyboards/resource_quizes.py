from dataclasses import dataclass
from typing import Literal, Union

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BaseManageEntryKeyboardBuilder,
    BaseQuizFinalKeyboardBuilder,
    BaseQuizQuestionKeyboardBuilder,
)
from application.keyboards.resources import (
    ListResourcesChooseResourceCallbackFactory,
    ListResourcesItemCallbackFactory,
)
from application.schemas.quiz_question_schema import BaseQuizQuestionSchema
from application.schemas.resource_schema import ResourceItemSchema


class ListResourcesQuizQuestionCallbackFactory(CallbackData, prefix="lst_rsc_qstn"):  # type: ignore[call-arg]
    action: Union[Literal["answer"], None]
    option_number: int
    question_number: int


@dataclass
class ResourceQuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-quizes-keyboard-create"),
                "callback_data": "create_quiz",
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-edit"),
                "callback_data": "edit_quiz",
            },
            {
                "text": self.i18n.get("manage-quizes-keyboard-delete"),
                "callback_data": "delete_quiz",
            },
        ]

    def _back_callback(self) -> str:
        return "menu"


@dataclass
class ResourceQuizFinalKeyboardBuilder(BaseQuizFinalKeyboardBuilder[ResourceItemSchema]):
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


@dataclass
class ResourceQuizQuestionKeyboardBuilder(
    BaseQuizQuestionKeyboardBuilder[ResourceItemSchema, BaseQuizQuestionSchema],
):
    def _build_quiz_callback(self, option_number: int, question_number: int) -> CallbackData:
        return ListResourcesQuizQuestionCallbackFactory(
            action="answer",
            option_number=option_number,
            question_number=question_number,
        )

    def _back_callback(self) -> str | CallbackData | None:
        return ListResourcesChooseResourceCallbackFactory(
            action="change_page",
            page=self.page,
            resource_item_id=self.item.resource_item_id,
        )
