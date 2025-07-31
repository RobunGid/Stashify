from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from i18n.translate import t

def manage_resources_edit_keyboard(user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("manage_resources.edit.name.choose", user_lang), callback_data="edit_resource_name"))
    builder.row(InlineKeyboardButton(text=t("manage_resources.edit.description.choose", user_lang), callback_data="edit_resource_description"))
    builder.row(InlineKeyboardButton(text=t("manage_resources.edit.image.choose", user_lang), callback_data="edit_resource_image"))
    builder.row(InlineKeyboardButton(text=t("manage_resources.edit.tags.choose", user_lang), callback_data="edit_resource_tags"))

    return builder.as_markup()