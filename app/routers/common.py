from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from database.models.user import Role
from schemas.user_schema import UserSchema
from database.managers.UserManager import UserManager
from keyboards.main_menu_keyboard import main_menu_keyboard
from i18n.translate import t

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    if not message.from_user or not message.from_user.id: 
        return
    user_data = {"id": str(message.from_user.id), "username": str(message.from_user.username), "role": Role.user, "language": message.from_user.language_code}
    
    user = UserSchema(**user_data)
    await UserManager.create(user)
        
    existing_user = await UserManager.get_one(str(message.from_user.id))
    role = existing_user.role
    
    reply_keyboard = main_menu_keyboard(role, message.from_user.language_code)
    await message.answer(t("main_menu.welcome", message.from_user.language_code), reply_markup=reply_keyboard)
    
