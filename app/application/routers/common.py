from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from aiogram_i18n import I18nContext
from application.routers.constants import ROLE_MENU_KEYBOARD_BUILDER_MAP
from application.schemas.user_schema import UserSchema
from infrastructure.models.user import Role

from database.managers.UserManager import UserManager

router = Router()


@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext):
    if not message.from_user or not message.from_user.id:
        return
    user = UserSchema(
        user_id=str(message.from_user.id),
        username=message.from_user.username,
        role=Role.user,
        language=message.from_user.language_code or "en",
    )
    await UserManager.create(user)

    existing_user = await UserManager.get_one(str(message.from_user.id))
    existing_user_role = existing_user.role

    RoleBuilder = ROLE_MENU_KEYBOARD_BUILDER_MAP[existing_user_role]
    builder = RoleBuilder(i18n=i18n)
    keyboard = builder.build()

    await message.answer(
        i18n.get(
            "main-menu-welcome",
        ),
        reply_markup=keyboard,
    )
