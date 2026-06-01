from typing import List, Literal, Optional, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema

class ListFavoritesItemCallbackFactory(CallbackData, prefix="lst_fvrt_itm"):
    action: Union[Literal["change_page"], Literal["add_favorite"], Literal["remove_favorite"], Literal["rate"]]
    resource_id: UUID4 | None
    rating: int | None

def list_favorites_resource_item_keyboard(resources: List[ResourceSchema], resource: ResourceSchema, user_lang: str = "en", is_favorite: bool = False, rating: int = 0):
    builder = InlineKeyboardBuilder()
    resource_index = resources.index(resource)
    resource_quantity = len(resources)
    first_line_buttons_quantity = 1
    if resource_index+1 != resource_quantity and resource_index != 0:
            builder.button(text=t("items.start", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[0].id, rating=0))
            builder.button(text=t("items.back", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id, rating=0))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id, rating=0))
            builder.button(text=t("items.end", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[-1].id, rating=0))
            first_line_buttons_quantity = 5
    elif resource_index == 0 and resource_quantity != 1:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id, rating=0))
            builder.button(text=t("items.end", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[-1].id, rating=0))
            first_line_buttons_quantity = 3
    elif resource_index+1 == resource_quantity and resource_quantity != 1:
            builder.button(text=t("items.start", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[0].id, rating=0))
            builder.button(text=t("items.back", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id, rating=0))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            first_line_buttons_quantity = 3
    elif resource_index == 0 and resource_quantity == 1:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            first_line_buttons_quantity = 1
    
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="list_favorites"))
    if not is_favorite:    
        builder.button(text=t("favorite.add", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="add_favorite", resource_id=resource.id, rating=0))
    if is_favorite:
        builder.button(text=t("favorite.remove", user_lang), callback_data=ListFavoritesItemCallbackFactory(action="remove_favorite", resource_id=resource.id, rating=0))
    for i in range(1, 6):
        symbol = "⭐" if i <= rating else "☆"
        builder.button(text=symbol, callback_data=ListFavoritesItemCallbackFactory(action="rate", resource_id=resource.id, rating=i))
    builder.adjust(first_line_buttons_quantity, 2, 5)
    return builder.as_markup()

        
