from dataclasses import dataclass

from keyboards.base import BaseManageEntryKeyboardBuilder


@dataclass
class UserManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {"text": self.i18n.get("manage-users-keyboard-edit"), "callback_data": "edit_user"},
            {"text": self.i18n.get("manage-users-keyboard-block"), "callback_data": "block_user"},
        ]

    def _back_callback(self) -> str:
        return "menu"
