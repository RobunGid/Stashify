from abc import ABC
from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.keyboards.base import BackToMenuKeyboardBuilderMixin, BaseBackKeyboardBuilder, BaseKeyboardBuilder


@dataclass
class BaseMenuKeyboardBuilder(BaseKeyboardBuilder, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for row in self._base_buttons():
            builder.row(*row)

        for row in self._role_buttons():
            builder.row(*row)

        return builder.as_markup()

    def _base_buttons(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-resources"),
                    callback_data="resources",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-search-resource"),
                    callback_data="search_resource",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-favorite"),
                    callback_data="list_favorites",
                ),
            ],
        ]

    def _role_buttons(self) -> list[list[InlineKeyboardButton]]:
        return []


@dataclass
class UserMenuKeyboardBuilder(BaseMenuKeyboardBuilder):
    def _role_buttons(self) -> list[list[InlineKeyboardButton]]:
        return []


@dataclass
class AdminMenuKeyboardBuilder(BaseMenuKeyboardBuilder):
    def _role_buttons(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-resources"),
                    callback_data="manage_resources",
                ),
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-categories"),
                    callback_data="manage_categories",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-users"),
                    callback_data="manage_users",
                ),
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-quizes"),
                    callback_data="manage_quizes",
                ),
            ],
        ]


@dataclass
class ManagerMenuKeyboardBuilder(BaseMenuKeyboardBuilder):
    def _role_buttons(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-resources"),
                    callback_data="manage_resources",
                ),
                InlineKeyboardButton(
                    text=self.i18n.get("main-menu-keyboard-manage-quizes"),
                    callback_data="manage_quizes",
                ),
            ],
        ]


@dataclass
class MenuBackKeyboardBuilder(BaseBackKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
    pass
