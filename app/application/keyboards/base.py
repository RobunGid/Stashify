from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_i18n import I18nContext
from domain.entities.base import BaseEntity


@dataclass
class CallbackDataResolverMixin(ABC):
    @staticmethod
    def _resolve_callback_data(
        callback: str | None | CallbackData,
    ) -> str | None:
        if isinstance(callback, CallbackData):
            return callback.pack()
        return callback


@dataclass
class BackKeyboardBuilderMixin(CallbackDataResolverMixin, ABC):
    i18n: I18nContext

    def _append_back_button(self, builder: InlineKeyboardBuilder):
        builder.row(
            InlineKeyboardButton(
                text=self.i18n.get("common-back"),
                callback_data=self._resolve_callback_data(self._back_callback()),
            ),
        )

    @abstractmethod
    def _back_callback(self) -> str | None | CallbackData:
        """callback_data for 'Back' button"""


@dataclass
class BackToMenuKeyboardBuilderMixin(BackKeyboardBuilderMixin):
    def _back_callback(self) -> str:
        return "menu"


@dataclass
class BaseKeyboardBuilder(ABC):
    i18n: I18nContext

    @abstractmethod
    def build(self) -> InlineKeyboardMarkup:
        pass


@dataclass
class BaseBackKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        self._append_back_button(builder)
        return builder.as_markup()


class QuizWithOptions(Protocol):
    options: list[str]


It = TypeVar("It", bound=BaseEntity)
Qs = TypeVar("Qs", bound=QuizWithOptions)
Qz = TypeVar("Qz")


@dataclass
class BaseListKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, Generic[It]):
    items: list[It]
    current_page: int
    total_pages: int

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for item in self.items:
            builder.row(InlineKeyboardButton(**self._item_button(item)))
        nav_buttons = [InlineKeyboardButton(**btn) for btn in self._build_pagination_buttons()]
        builder.row(*nav_buttons)

        self._append_back_button(builder)
        return builder.as_markup()

    def _build_pagination_buttons(self) -> list[dict]:
        current_page, total_pages = self.current_page, self.total_pages

        if total_pages <= 1:
            return [{"text": f"{current_page + 1}/{total_pages}", "callback_data": " "}]

        buttons = []

        if current_page > 0:
            buttons += [
                {
                    "text": self.i18n.get("items-start"),
                    "callback_data": self._pagination_callback(0).pack(),
                },
                {
                    "text": self.i18n.get("items-back"),
                    "callback_data": self._pagination_callback(current_page - 1).pack(),
                },
            ]

        buttons.append({"text": f"{current_page + 1}/{total_pages}", "callback_data": " "})

        if current_page < (total_pages - 1):
            buttons += [
                {
                    "text": self.i18n.get("items-forward"),
                    "callback_data": self._pagination_callback(current_page + 1).pack(),
                },
                {
                    "text": self.i18n.get("items-end"),
                    "callback_data": self._pagination_callback(total_pages - 1).pack(),
                },
            ]

        return buttons

    @abstractmethod
    def _pagination_callback(self, page: int) -> CallbackData:
        """Return callback_data for pagination button"""

    @abstractmethod
    def _item_button(self, item: It) -> dict:
        """Convert item to kwargs for builder.button() - text and callback_data"""


@dataclass
class NavigationKeyboardBuilderMixin(ABC):
    @abstractmethod
    def _navigation_callback(self, item_id: UUID) -> CallbackData:
        """Return callback_data for pagination button"""


@dataclass
class BaseItemKeyboardBuilder(
    NavigationKeyboardBuilderMixin,
    BaseKeyboardBuilder,
    BackKeyboardBuilderMixin,
    Generic[It],
):
    item_ids: tuple[UUID | None, UUID | None, UUID | None, UUID | None]
    current_item: It
    current_item_index: int
    total_items: int

    is_favorite: bool
    rating: int | None
    has_quiz: bool
    quiz_percent: int | None

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        nav_buttons = self._build_navigation_buttons()
        builder.row(*[InlineKeyboardButton(**btn) for btn in nav_buttons])
        self._append_back_button(builder)
        builder.adjust(len(nav_buttons), 1)
        return builder.as_markup()

    def _build_navigation_buttons(self) -> list[dict]:
        buttons: list[dict] = []
        if self.item_ids[0] is not None:
            buttons += [
                {
                    "text": self.i18n.get("items-start"),
                    "callback_data": self._navigation_callback(self.item_ids[0]).pack(),
                },
            ]
        if self.item_ids[1] is not None:
            buttons += [
                {
                    "text": self.i18n.get("items-back"),
                    "callback_data": self._navigation_callback(
                        self.item_ids[1],
                    ).pack(),
                },
            ]
        buttons.append({"text": f"{self.current_item_index + 1}/{self.total_items}", "callback_data": " "})
        if self.item_ids[2] is not None:
            buttons += [
                {
                    "text": self.i18n.get("items-forward"),
                    "callback_data": self._navigation_callback(
                        self.item_ids[2],
                    ).pack(),
                },
            ]
        if self.item_ids[3] is not None:
            buttons += [
                {
                    "text": self.i18n.get("items-end"),
                    "callback_data": self._navigation_callback(self.item_ids[3]).pack(),
                },
            ]
        return buttons

    def _build_favorite_buttons(self) -> list[dict]:
        if self.is_favorite:
            return [
                {
                    "text": self.i18n.get("favorite-remove"),
                    "callback_data": self._remove_favorite_callback(self.current_item).pack(),
                },
            ]
        return [
            {
                "text": self.i18n.get("favorite-add"),
                "callback_data": self._add_favorite_callback(self.current_item).pack(),
            },
        ]

    def _build_rating_buttons(self) -> list[dict]:
        return [
            {
                "text": "⭐" if self.rating and i <= self.rating else "☆",
                "callback_data": self._rating_callback(self.current_item, i).pack(),
            }
            for i in range(1, 6)
        ]

    @abstractmethod
    def _build_quiz_buttons(self) -> list[dict]:
        """Return buttons for start quiz"""

    @abstractmethod
    def _get_item_id(self, item: It) -> str | UUID | int:
        """Get item id callback"""

    @abstractmethod
    def _remove_favorite_callback(self, item: It) -> CallbackData:
        """Return callback_data for removing item from favorites"""

    @abstractmethod
    def _add_favorite_callback(self, item: It) -> CallbackData:
        """Return callback_data for adding item in favorites"""

    @abstractmethod
    def _rating_callback(self, item: It, rating: int) -> CallbackData:
        """Return callback_data for rate item"""


@dataclass
class BaseConfirmKeyboardBuilder(
    BackKeyboardBuilderMixin,
    BaseKeyboardBuilder,
    ABC,
):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_confirm_buttons()
        for btn in btns:
            builder.button(**btn)
        self._append_back_button(builder)
        return builder.as_markup()

    @abstractmethod
    def _build_confirm_buttons(self) -> list[dict]:
        """Return data for confirm buttons"""


@dataclass
class BaseQuizConfirmKeyboardBuilder(BaseConfirmKeyboardBuilder, ABC, Generic[It]):
    current_item: It


@dataclass
class BaseManageEntryKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_entry_buttons()
        for btn in btns:
            builder.button(**btn)
        builder.adjust(1)

        self._append_back_button(builder)

        return builder.as_markup()

    @abstractmethod
    def _build_entry_buttons(self) -> list[dict]:
        pass


@dataclass
class BaseQuizFinalKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC, Generic[It]):
    item: It
    page: int

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_retry_buttons()
        for btn in btns:
            builder.button(**btn)

        self._append_back_button(builder)
        builder.adjust(1, 1)
        return builder.as_markup()

    @abstractmethod
    def _build_retry_buttons(self) -> list[dict]:
        pass


@dataclass
class BaseQuizQuestionKeyboardBuilder(
    BaseKeyboardBuilder,
    BackKeyboardBuilderMixin,
    ABC,
    Generic[It, Qs, Qz],
):
    item: It
    question: Qs
    quiz_item: Qz
    page: int
    question_number: int

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for index, option in enumerate(self.question.options):
            if option.startswith("!"):
                option = option[1:]
            builder.button(
                text=option,
                callback_data=self._build_quiz_callback(
                    option_number=index,
                    question_number=self.question_number,
                ),
            )
            builder.adjust(1)
            self._append_back_button(builder)

        return builder.as_markup()

    @abstractmethod
    def _build_quiz_callback(self, option_number: int, question_number: int) -> str | CallbackData:
        pass


@dataclass
class BaseEditKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_edit_buttons()
        for btn in btns:
            builder.button(**btn)
        builder.adjust(1)
        self._append_back_button(builder)
        return builder.as_markup()

    @abstractmethod
    def _build_edit_buttons(self) -> list[dict]:
        pass
