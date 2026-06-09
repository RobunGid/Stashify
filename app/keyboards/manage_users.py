from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.base import BackKeyboardBuilderMixin, BaseKeyboardBuilder


@dataclass
class ManageUsersKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.row(
            InlineKeyboardButton(
                text=self.i18n.get("manage-users-keyboard-edit"),
                callback_data="edit_user",
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=self.i18n.get("manage-users-keyboard-block"),
                callback_data="block_user",
            ),
        )
        self._append_back_button(builder)

        return builder.as_markup()

    def _back_callback(self) -> str:
        return "menu"
