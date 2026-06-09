from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_i18n import I18nContext
from aiogram.filters.callback_data import CallbackData


@dataclass
class BackKeyboardBuilderMixin:
    i18n: I18nContext

    def _append_back_button(self, builder: InlineKeyboardBuilder):
        builder.row(
            InlineKeyboardButton(
                text=self.i18n.get("common-back"),
                callback_data=self._back_callback(),
            )
        )

    @abstractmethod
    def _back_callback(self) -> str:
        """callback_data for 'Back' button"""
        pass


@dataclass
class BaseKeyboardBuilder(ABC):
    i18n: I18nContext


It = TypeVar("It")


@dataclass
class BaseListKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, Generic[It]):
    items: list[It]
    current_page: int
    total_pages: int

    callback_factory: CallbackData

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for item in self.items:
            builder.button(**self._item_button(item))

        nav_buttons = self._build_pagination_buttons()
        for btn in nav_buttons:
            builder.button(**btn)

        nav_count = len(nav_buttons)
        builder.adjust(*([1] * len(self.items)), nav_count)

        self._append_back_button(builder)
        return builder.as_markup()

    def _build_pagination_buttons(self) -> list[dict]:
        pages, total_pages = self.current_page, self.total_pages

        if total_pages <= 1:
            return [{"text": f"{pages}/{total_pages}", "callback_data": " "}]

        buttons = []

        if pages > 1:
            buttons += [
                {"text": self.i18n.get("items.start"), "callback_data": self._pagination_callback(1)},
                {"text": self.i18n.get("items.back"), "callback_data": self._pagination_callback(pages - 1)},
            ]

        buttons.append({"text": f"{pages}/{total_pages}", "callback_data": " "})

        if pages < total_pages:
            buttons += [
                {"text": self.i18n.get("items.forward"), "callback_data": self._pagination_callback(pages + 1)},
                {"text": self.i18n.get("items.end"), "callback_data": self._pagination_callback(total_pages)},
            ]

        return buttons

    @abstractmethod
    def _pagination_callback(self, page: int) -> CallbackData:
        """Return callback_data for pagination button"""
        pass

    @abstractmethod
    def _item_button(self, item: It) -> dict:
        """Convert item to kwargs for builder.button() - text and callback_data"""
        pass
