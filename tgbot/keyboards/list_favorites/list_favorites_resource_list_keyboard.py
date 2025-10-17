from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema

class ListFavoritesChooseResourceCallbackFactory(CallbackData, prefix="list_favorites_rsc"):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_id: UUID4 | None
    page: int

def list_favorites_resource_list_keyboard(resources: List[ResourceSchema], page: int, total_pages: int, user_lang: str = "en", ):
    builder = InlineKeyboardBuilder()
    first_line_buttons_quantity = 1
    
    for resource in resources:
        builder.button(text=resource.name, callback_data=ListFavoritesChooseResourceCallbackFactory(action="select", resource_id=resource.id, page=0))
    if page != total_pages and page != 1:
            builder.button(text=t("items.start", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=total_pages))
            first_line_buttons_quantity = 5
    elif page == 1 and total_pages != 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=total_pages))
            first_line_buttons_quantity = 3
    elif page == total_pages and total_pages != 1:
            builder.button(text=t("items.start", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=ListFavoritesChooseResourceCallbackFactory(action="change_page", resource_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            first_line_buttons_quantity = 3
    elif page == 1 and total_pages == 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            first_line_buttons_quantity = 1
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="list_favorites"))
    builder.adjust(len(resources), first_line_buttons_quantity, 2, 5)
    return builder.as_markup()
