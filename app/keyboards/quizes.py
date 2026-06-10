from dataclasses import dataclass

from keyboards.base import BaseManageEntryKeyboardBuilder


@dataclass
class QuizManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {"text": self.i18n.get("manage-quizes-keyboard-create"), "callback_data": "create_quiz"},
            {"text": self.i18n.get("manage-quizes-keyboard-edit"), "callback_data": "edit_quiz"},
            {"text": self.i18n.get("manage-quizes-keyboard-delete"), "callback_data": "delete_quiz"},
        ]

    def _back_callback(self) -> str:
        return "menu"
