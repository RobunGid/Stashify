from dataclasses import dataclass

from keyboards.base import BaseManageEntryKeyboardBuilder


@dataclass
class CategoryManageEntryKeyboardBuilder(BaseManageEntryKeyboardBuilder):
    def _build_entry_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("manage-categories-keyboard-create"),
                "callback_data": "create_category",
            },
            {
                "text": self.i18n.get("manage-categories-keyboard-edit"),
                "callback_data": "edit_category",
            },
            {
                "text": self.i18n.get("manage-categories-keyboard-delete"),
                "callback_data": "delete_category",
            },
        ]

    def _back_callback(self) -> str:
        return "menu"
