from uuid import uuid4
from pprint import pprint

from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from database.models.user import Role
from schemas.user_schema import UserSchema
from database.operations.create_user import create_user

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    if message.from_user and message.from_user.id:
        user_data = {"id": str(uuid4()), "tg_id": str(message.from_user.id), "role": Role.user, "language": message.from_user.language_code}
        
        user = UserSchema(**user_data)
        await create_user(user)
     
    await message.answer(f"Hello, {message.from_user.username if message.from_user else 'user'}. It's my first test message")