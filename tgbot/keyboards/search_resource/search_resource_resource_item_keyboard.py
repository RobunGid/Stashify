from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema

class SearchResourceItemCallbackFactory(CallbackData, prefix="search_resource_itm"):
    action: Union[Literal["change_page"], Literal["add_favorite"], Literal["remove_favorite"]]
    resource_id: UUID4 | None

def search_resource_resource_item_keyboard(resources: List[ResourceSchema],  resource: ResourceSchema, user_lang: str = "en", is_favorite: bool = False):
    builder = InlineKeyboardBuilder()
    resource_index = resources.index(resource)
    resource_quantity = len(resources)
    
    if resource_index+1 != resource_quantity and resource_index != 0:
            builder.button(text=t("items.start", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[0].id))
            builder.button(text=t("items.back", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id))
            builder.button(text=t("items.end", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[-1].id,))
            builder.adjust(5)
    elif resource_index == 0 and resource_quantity != 1:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id))
            builder.button(text=t("items.end", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[-1].id))
            builder.adjust(3)
    elif resource_index+1 == resource_quantity and resource_quantity != 1:
            builder.button(text=t("items.start", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[0].id))
            builder.button(text=t("items.back", user_lang), callback_data=SearchResourceItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.adjust(3)
    elif resource_index == 0 and resource_quantity == 0:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.adjust(1)
    if not is_favorite:    
        builder.button(text=t("favorite.add", user_lang), callback_data=SearchResourceItemCallbackFactory(action="add_favorite", resource_id=resource.id))
    if is_favorite:
        builder.button(text=t("favorite.remove", user_lang), callback_data=SearchResourceItemCallbackFactory(action="remove_favorite", resource_id=resource.id))
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="menu"))
    return builder.as_markup()
