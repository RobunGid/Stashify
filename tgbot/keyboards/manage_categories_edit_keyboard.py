from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from pydantic import UUID4
from aiogram.filters.callback_data import CallbackData

from i18n.translate import t
from schemas.category_schema import CategorySchema
from config.var_config import EDIT_CATEGORIES_ON_PAGE

class CategoryIdCallbackFactory(CallbackData, prefix="edit_category_id"):
    action: str
    value: UUID4


def manage_categories_edit_keyboard(user_lang: str | None, categories: List[CategorySchema], page: int, total_pages: int):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category.name, callback_data=CategoryIdCallbackFactory(action="change", value=category.id))
        
        builder.adjust(1)
    
    if page != total_pages and page != 1:
        builder.row(
            InlineKeyboardButton(text=t("items.start", user_lang), callback_data=f"edit_category_page_1"),
            InlineKeyboardButton(text=t("items.back", user_lang), callback_data=f"edit_category_page_{page-1}"),
            InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f" "),
            InlineKeyboardButton(text=t("items.forward", user_lang), callback_data=f"edit_category_page_{page+1}"),
            InlineKeyboardButton(text=t("items.end", user_lang), callback_data=f"edit_category_page_{total_pages}")
        )
    elif page == 1 and total_pages != 1:
        builder.row(
            InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f" "),
            InlineKeyboardButton(text=t("items.forward", user_lang), callback_data=f"edit_category_page_{page+1}"),
            InlineKeyboardButton(text=t("items.end", user_lang), callback_data=f"edit_category_page_{total_pages}"),
        )
    elif page == total_pages and total_pages != 1:
        builder.row(
            InlineKeyboardButton(text=t("items.start", user_lang), callback_data=f"edit_category_page_1"),
            InlineKeyboardButton(text=t("items.back", user_lang), callback_data=f"edit_category_page_{page-1}"),
            InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f" "),
        )
    elif page == 1 and total_pages == 1:
        builder.row(
            InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f" "),
        )
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_categories"))
    return builder.as_markup()