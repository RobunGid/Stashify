from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database.models.user import Role
from i18n.translate import t

def main_menu_keyboard(user_role: Role, user_lang: str | None):
    user_lang = user_lang or "en"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("main_menu_keyboard.resources", user_lang), callback_data="resources"))
    builder.row(InlineKeyboardButton(text=t("main_menu_keyboard.search_resource", user_lang), callback_data="search_resource"))
    builder.row(InlineKeyboardButton(text=t("main_menu_keyboard.favorite", user_lang), callback_data="favorite"))
    builder.row(InlineKeyboardButton(text=t("main_menu_keyboard.quizes", user_lang), callback_data="quizes"))

    if user_role == Role.admin:
        builder.row(
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_resources", user_lang), callback_data="manage_resources"),
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_categories", user_lang), callback_data="manage_categories"),
        )
        builder.row(
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_users", user_lang), callback_data="manage_users"),
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_quizes", user_lang), callback_data="manage_quizes"),
        )

    if user_role == Role.manager:
        builder.row(
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_resources", user_lang), callback_data="manage_resources"),
            InlineKeyboardButton(text=t("main_menu_keyboard.manage_quizes", user_lang), callback_data="manage_quizes"),
        )

    return builder.as_markup()