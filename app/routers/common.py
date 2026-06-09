from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from aiogram_i18n import I18nContext

from database.managers.UserManager import UserManager
from database.models.user import Role
from keyboards.main_menu_keyboard import main_menu_keyboard
from schemas.user_schema import UserSchema

router = Router()


@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext):
    if not message.from_user or not message.from_user.id:
        return
    user_data = {
        "id": str(message.from_user.id),
        "username": str(message.from_user.username),
        "role": Role.user,
        "language": message.from_user.language_code,
    }

    user = UserSchema(**user_data)
    await UserManager.create(user)

    existing_user = await UserManager.get_one(str(message.from_user.id))
    role = existing_user.role

    reply_keyboard = main_menu_keyboard(role, message.from_user.language_code)
    await message.answer(
        i18n.get(
            "main-menu-welcome",
        ),
        reply_markup=reply_keyboard,
    )
