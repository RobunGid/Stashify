from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from pydantic import UUID4
from aiogram.filters.callback_data import CallbackData

from i18n.translate import t
from schemas.category_schema import CategorySchema

class CreateResourceCallbackFactory(CallbackData, prefix="create_resource"):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID4 | None
    page: int


def manage_resources_create_keyboard(user_lang: str | None, categories: List[CategorySchema], page: int, total_pages: int):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    
    for category in categories:
        builder.button(text=category.name, callback_data=CreateResourceCallbackFactory(action="select", category_id=category.id, page=0))
    if page != total_pages and page != 1:
            builder.button(text=t("items.start", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=total_pages))
            builder.adjust(*[*([1]*len(categories)), 5, 1])
    elif page == 1 and total_pages != 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=total_pages))
            builder.adjust(*[*([1]*len(categories)), 3, 1])
    elif page == total_pages and total_pages != 1:
            builder.button(text=t("items.start", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=CreateResourceCallbackFactory(action="change_page", category_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.adjust(*[*([1]*len(categories)), 3, 1])
    elif page == 1 and total_pages == 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.adjust(*[*([1]*len(categories)), 1, 1])
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_resources"))
    return builder.as_markup()