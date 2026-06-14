from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from aiogram_i18n import I18nContext
from application.routers.constants import ROLE_MENU_KEYBOARD_BUILDER_MAP
from application.schemas.user_account_schema import UserAccountSchema

router = Router()


@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext, user_account: UserAccountSchema):
    if not message.from_user or not message.from_user.id:
        return

    RoleBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[user_account.role]
    builder = RoleBuilder(i18n=i18n)
    keyboard = builder.build()

    await message.answer(
        i18n.get(
            "main-menu-welcome",
        ),
        reply_markup=keyboard,
    )
