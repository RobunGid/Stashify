from uuid import uuid4
from pprint import pprint

from aiogram import Router
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message

from database.models.user import Role
from schemas.user_schema import UserSchema
from database.operations.create_user import create_user
from database.operations.get_user_role import get_user_role
from keyboards.main_menu_keyboard import main_menu_keyboard
from i18n.translate import t

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    if not message.from_user or not message.from_user.id: return
    user_data = {"id": str(uuid4()), "tg_id": str(message.from_user.id), "role": Role.user, "language": message.from_user.language_code}
    
    user = UserSchema(**user_data)
    await create_user(user)
        
    user_role = await get_user_role(str(message.from_user.id))
    
    reply_keyboard = main_menu_keyboard(user_role, message.from_user.language_code)
    await message.answer(t("main_menu.welcome", message.from_user.language_code), reply_markup=reply_keyboard)
    
@router.message(Command("menu"))
async def main_menu_command(message: Message):
    if not message.from_user or not message.from_user.id: return

    user_role = await get_user_role(str(message.from_user.id))
    
    reply_keyboard = main_menu_keyboard(user_role, message.from_user.language_code)
    await message.answer(t("main_menu.text", message.from_user.language_code), reply_markup=reply_keyboard)