from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from pydantic import UUID4
from aiogram.filters.callback_data import CallbackData

from i18n.translate import t
from schemas.resource_schema import ResourceSchema

class DeleteResourceCallbackFactory(CallbackData, prefix="delete_resource"):
    action: Union[Literal["select"], Literal["change_page"]]
    resource_id: UUID4 | None
    page: int


def manage_resources_delete_keyboard(user_lang: str | None, resources: List[ResourceSchema], page: int, total_pages: int):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    
    for resource in resources:
        builder.button(text=resource.name, callback_data=DeleteResourceCallbackFactory(action="select", resource_id=resource.id, page=0))
    if page != total_pages and page != 1:
            builder.button(text=t("items.start", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=total_pages))
            builder.adjust(*[*([1]*len(resources)), 5, 1])
    elif page == 1 and total_pages != 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=page+1))
            builder.button(text=t("items.end", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=total_pages))
            builder.adjust(*[*([1]*len(resources)), 3, 1])
    elif page == total_pages and total_pages != 1:
            builder.button(text=t("items.start", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=1))
            builder.button(text=t("items.back", user_lang), callback_data=DeleteResourceCallbackFactory(action="change_page", resource_id=None, page=page-1))
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.adjust(*[*([1]*len(resources)), 3, 1])
    elif page == 1 and total_pages == 1:
            builder.button(text=f"{page}/{total_pages}", callback_data=f" ")
            builder.adjust(*[*([1]*len(resources)), 1, 1])
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="manage_resources"))
    return builder.as_markup()