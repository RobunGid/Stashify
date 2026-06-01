from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n.translate import t


class PaginationMixin:

    @staticmethod
    def build_page_buttons(
        builder: InlineKeyboardBuilder,
        callback_factory_fn,  
        page: int,
        total_pages: int,
        user_lang: str,
    ) -> int:
        if total_pages <= 1:
            builder.button(
                text=f"{page}/{total_pages}",
                callback_data=" ",
            )
            return 1

        is_first = page == 1
        is_last = page == total_pages

        if not is_first:
            builder.button(text=t("items.start", user_lang), callback_data=callback_factory_fn(1))
            builder.button(text=t("items.back", user_lang), callback_data=callback_factory_fn(page - 1))

        builder.button(text=f"{page}/{total_pages}", callback_data=" ")

        if not is_last:
            builder.button(text=t("items.forward", user_lang), callback_data=callback_factory_fn(page + 1))
            builder.button(text=t("items.end", user_lang), callback_data=callback_factory_fn(total_pages))

        if is_first:
            return 3   
        if is_last:
            return 3   
        return 5


class BaseListKeyboard(PaginationMixin):

    def __init__(self, user_lang: str = "en"):
        self.user_lang = user_lang
        self.builder = InlineKeyboardBuilder()

    def _back_callback(self) -> str:
        raise NotImplementedError

    def _back_label(self) -> str:
        return t("common.back", self.user_lang)

    def _add_back_button(self):
        self.builder.row(
            InlineKeyboardButton(text=self._back_label(), callback_data=self._back_callback())
        )

    def build(self) -> "InlineKeyboardMarkup":
        raise NotImplementedError


class BaseItemKeyboard(PaginationMixin):

    def __init__(self, user_lang: str = "en"):
        self.user_lang = user_lang
        self.builder = InlineKeyboardBuilder()

    def _back_callback(self) -> str:
        raise NotImplementedError

    def _back_label(self) -> str:
        return t("common.back", self.user_lang)

    def _add_back_button(self):
        self.builder.row(
            InlineKeyboardButton(text=self._back_label(), callback_data=self._back_callback())
        )

    @staticmethod
    def _resolve_item_nav(index: int, total: int):
        return index == 0, index + 1 == total

    def build(self) -> "InlineKeyboardMarkup":
        raise NotImplementedError