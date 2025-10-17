from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.category_schema import CategorySchema

class ListResourcesChooseCategoryCallbackFactory(CallbackData, prefix="list_resources_ctg"):
    action: Union[Literal["select"], Literal["change_page"]]
    category_id: UUID4 | None
    page: int

def list_resources_category_list_keyboard(categories: List[CategorySchema], page: int, total_pages: int, user_lang: str = "en"):
    builder = InlineKeyboardBuilder()
    first_line_buttons_quantity = 1
    
    for category in categories:
        builder.button(text=category.name, callback_data=ListResourcesChooseCategoryCallbackFactory(action="select", category_id=category.id, page=0))
    if page != total_pages and page != 1:
        builder.button(text=t("items.start", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=1))
        builder.button(text=t("items.back", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page-1))
        builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
        builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page+1))
        builder.button(text=t("items.end", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=total_pages))
        first_line_buttons_quantity = 5
    elif page == 1 and total_pages != 1:
        builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
        builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page+1))
        builder.button(text=t("items.end", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=total_pages))
        first_line_buttons_quantity = 3
    elif page == total_pages and total_pages != 1:
        builder.button(text=t("items.start", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=1))
        builder.button(text=t("items.back", user_lang), callback_data=ListResourcesChooseCategoryCallbackFactory(action="change_page", category_id=None, page=page-1))
        builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
        first_line_buttons_quantity = 3
    elif page == 1 and total_pages == 1:
        builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
        first_line_buttons_quantity = 1
    elif page == 1 and total_pages == 0:
        builder.button(text=t("list_favorites.no_results", lang=user_lang), callback_data=f" ")
        first_line_buttons_quantity = 1
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))
    
    builder.adjust(*([1]*len(categories)), first_line_buttons_quantity, 2)
    return builder.as_markup()
