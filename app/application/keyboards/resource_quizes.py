from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from application.keyboards.base import (
    BaseManageEntryKeyboardBuilder,
    BaseQuizFinalKeyboardBuilder,
    BaseQuizQuestionKeyboardBuilder,
)
from application.keyboards.resources import (
    ListCategoryResourcesItemCallbackFactory,
)
from domain.entities.quiz_item import QuizItemEntity
from domain.entities.quiz_question import QuizQuestionEntity
from domain.entities.resource_item import ResourceItemEntity


class ListResourcesQuizQuestionCallbackFactory(CallbackData, prefix="lst_rsc_qstn"):  # type: ignore[call-arg]
    action: Union[Literal["answer"], None]
    option_number: int
    question_number: int
    quiz_item_id: UUID


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
class ResourceQuizFinalKeyboardBuilder(BaseQuizFinalKeyboardBuilder[ResourceItemEntity]):
    def _build_retry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("start-quiz-retry"),
                "callback_data": ListCategoryResourcesItemCallbackFactory(
                    page=0,
                    context="menu",
                    category_item_id=self.item.category_item_id,
                ).pack(),
            },
        ]

    def _back_callback(self) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            context="menu",
            category_item_id=self.item.category_item_id,
            page=0,
        ).pack()


@dataclass
class ResourceQuizQuestionKeyboardBuilder(
    BaseQuizQuestionKeyboardBuilder[ResourceItemEntity, QuizQuestionEntity, QuizItemEntity],
):
    def _build_quiz_callback(self, option_number: int, question_number: int) -> str:
        return ListResourcesQuizQuestionCallbackFactory(
            action="answer",
            option_number=option_number,
            question_number=question_number,
            quiz_item_id=self.quiz_item.quiz_item_id,
        ).pack()

    def _back_callback(self) -> str:
        return ListCategoryResourcesItemCallbackFactory(
            page=self.page,
            context="menu",
            category_item_id=self.item.category_item_id,
        ).pack()
