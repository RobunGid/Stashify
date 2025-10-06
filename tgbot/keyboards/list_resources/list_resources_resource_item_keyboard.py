from typing import List, Union, Literal

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pydantic import UUID4

from i18n.translate import t
from schemas.resource_schema import ResourceSchema
from keyboards.list_resources.list_resources_resource_list_keyboard import ListResourcesChooseResourceCallbackFactory

class ListResourcesItemCallbackFactory(CallbackData, prefix="list_resources_itm"):
    action: Literal["change_page"]
    resource_id: UUID4 | None

def list_resources_resource_item_keyboard(resources: List[ResourceSchema],  resource: ResourceSchema, user_lang: str = "en"):
    builder = InlineKeyboardBuilder()
    resource_index = resources.index(resource)
    resource_quantity = len(resources)
    
    if resource_index+1 != resource_quantity and resource_index != 0:
            builder.button(text=t("items.start", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[0].id))
            builder.button(text=t("items.back", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id))
            builder.button(text=t("items.end", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[-1].id,))
            builder.adjust(5)
    elif resource_index == 0 and resource_quantity != 1:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.button(text=t("items.forward", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index+1].id))
            builder.button(text=t("items.end", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[-1].id))
            builder.adjust(3)
    elif resource_index+1 == resource_quantity and resource_quantity != 1:
            builder.button(text=t("items.start", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[0].id))
            builder.button(text=t("items.back", user_lang), callback_data=ListResourcesItemCallbackFactory(action="change_page", resource_id=resources[resource_index-1].id))
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.adjust(3)
    elif resource_index == 0 and resource_quantity == 0:
            builder.button(text=f"{resource_index+1}/{resource_quantity}", callback_data=f" ")
            builder.adjust(1)
    builder.row(InlineKeyboardButton(text=t("common.back", user_lang), callback_data="resources"))
    return builder.as_markup()
