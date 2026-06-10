from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_i18n import I18nContext


@dataclass
class BackKeyboardBuilderMixin:
    i18n: I18nContext

    def _append_back_button(self, builder: InlineKeyboardBuilder):
        builder.button(
            text=self.i18n.get("common-back"),
            callback_data=self._back_callback(),
        )

    @abstractmethod
    def _back_callback(self) -> str | CallbackData | None:
        """callback_data for 'Back' button"""


@dataclass
class BaseKeyboardBuilder(ABC):
    i18n: I18nContext

    @abstractmethod
    def build(self) -> InlineKeyboardMarkup:
        pass


@dataclass
class BaseManageBackKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        self._append_back_button(builder)
        return builder.as_markup()


class QuizWithOptions(Protocol):
    options: list[str]


It = TypeVar("It")
Qs = TypeVar("Qs", bound=QuizWithOptions)


@dataclass
class BaseListKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, Generic[It]):
    items: list[It]
    current_page: int
    total_pages: int

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
                {
                    "text": self.i18n.get("items.start"),
                    "callback_data": self._pagination_callback(1),
                },
                {
                    "text": self.i18n.get("items.back"),
                    "callback_data": self._pagination_callback(pages - 1),
                },
            ]

        buttons.append({"text": f"{pages}/{total_pages}", "callback_data": " "})

        if pages < total_pages:
            buttons += [
                {
                    "text": self.i18n.get("items.forward"),
                    "callback_data": self._pagination_callback(pages + 1),
                },
                {
                    "text": self.i18n.get("items.end"),
                    "callback_data": self._pagination_callback(total_pages),
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
class NavigationKeyboardBuilderMixin(ABC, Generic[It]):
    @abstractmethod
    def _navigation_callback(self, item: It) -> CallbackData:
        """Return callback_data for pagination button"""


@dataclass
class BaseItemKeyboardBuilder(NavigationKeyboardBuilderMixin, BaseKeyboardBuilder, Generic[It]):
    items: list[It]
    current_item: It

    is_favorite: bool
    rating: int | None
    has_quiz: bool
    quiz_percent: int

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        nav_buttons = self._build_navigation_buttons()
        for btns in nav_buttons:
            builder.button(**btns)

        return builder.as_markup()

    def _build_navigation_buttons(self) -> list[dict]:
        item_ids = [self._get_item_id(item) for item in self.items]
        current_item_id = self._get_item_id(self.current_item)
        current_item_id_index = item_ids.index(current_item_id)
        total_items = len(self.items)

        is_at_start = current_item_id_index == 0
        is_at_end = current_item_id_index == total_items - 1

        buttons: list[dict] = []

        if not is_at_start:
            buttons += [
                {
                    "text": self.i18n.get("items-start"),
                    "callback_data": self._navigation_callback(self.items[0]),
                },
                {
                    "text": self.i18n.get("items-back"),
                    "callback_data": self._navigation_callback(
                        self.items[current_item_id_index - 1],
                    ),
                },
            ]
        buttons.append({"text": f"{current_item_id_index + 1}/{total_items}", "callback_data": " "})
        if not is_at_end:
            buttons += [
                {
                    "text": self.i18n.get("items-forward"),
                    "callback_data": self._navigation_callback(
                        self.items[current_item_id_index + 1],
                    ),
                },
                {
                    "text": self.i18n.get("items-end"),
                    "callback_data": self._navigation_callback(self.items[-1]),
                },
            ]
        return buttons

    def _build_favorite_buttons(self) -> list[dict]:
        if self.is_favorite:
            return [
                {
                    "text": self.i18n.get("favorite-remove"),
                    "callback_data": self._remove_favorite_callback(self.current_item),
                },
            ]
        return [
            {
                "text": self.i18n.get("favorite-add"),
                "callback_data": self._add_favorite_callback(self.current_item),
            },
        ]

    def _build_rating_buttons(self) -> list[dict]:
        return [
            {
                "text": "⭐" if self.rating and i <= self.rating else "☆",
                "callback_data": self._rating_callback(self.current_item, i),
            }
            for i in range(1, 6)
        ]

    def _build_quiz_buttons(self) -> list[dict]:
        if not self.has_quiz:
            return []
        if self.quiz_percent:
            text = self.i18n.get("start-quiz-completed").format(percent=self.quiz_percent)
        else:
            text = self.i18n.get("start-quiz-firstly")
        return [
            {
                "text": text,
                "callback_data": self._quiz_callback(self.current_item),
            },
        ]

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

    @abstractmethod
    def _quiz_callback(self, item: It) -> CallbackData:
        """Return callback_data for start quiz"""


@dataclass
class BaseQuizConfirmKeyboardBuilder(
    NavigationKeyboardBuilderMixin,
    BaseKeyboardBuilder,
    ABC,
    Generic[It],
):
    current_item: It

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_quiz_confirm_buttons()
        for btn in btns:
            builder.button(**btn)
        return builder.as_markup()

    def _build_quiz_confirm_buttons(self) -> list[dict]:
        return [
            {
                "text": self.i18n.get("ist-resources-start_quiz-confirm"),
                "callback_data": self._quiz_confirm_callback(self.current_item),
            },
            {
                "text": self.i18n.get("common-back"),
                "callback_data": self._navigation_callback(self.current_item),
            },
        ]

    @abstractmethod
    def _quiz_confirm_callback(self, item: It) -> CallbackData:
        """Return callback_data for confirm starting quiz"""


@dataclass
class BaseManageEntryKeyboardBuilder(BaseKeyboardBuilder, BackKeyboardBuilderMixin, ABC):
    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        btns = self._build_entry_buttons()
        for btn in btns:
            builder.row(**btn)

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
            builder.row(**btn)

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
    Generic[It, Qs],
):
    item: It
    question: Qs
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
