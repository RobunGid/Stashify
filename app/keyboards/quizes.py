from dataclasses import dataclass
from typing import Literal, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from keyboards.base import BaseManageEntryKeyboardBuilder


class EditQuizActionCallbackFactory(CallbackData, prefix="edit_quiz_actn"):  # type: ignore[call-arg]
    action: Union[Literal["edit"], Literal["delete"], Literal["add"]]
    resource_item_id: UUID | None


@dataclass
class QuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    resource_item_id: UUID

    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage_quizes_keyboard.add_question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="add",
                    resource_item_id=self.resource_item_id,
                ),
            },
            {
                "text": self.i18n.get("manage_quizes_keyboard.edit_question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="edit",
                    resource_item_id=self.resource_item_id,
                ),
            },
            {
                "text": self.i18n.get("manage_quizes_keyboard.delete_question"),
                "callback_data": EditQuizActionCallbackFactory(
                    action="delete",
                    resource_item_id=self.resource_item_id,
                ),
            },
        ]

    def _back_callback(self) -> str:
        return "menu"
