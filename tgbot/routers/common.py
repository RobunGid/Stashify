from uuid import uuid4
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
        user_data = {"id": uuid4(), "tg_id": message.from_user.id, "role": Role.user}
        
        user = UserSchema.model_validate(user_data)
        await create_user(user)
     
    await message.answer(f"Hello, {message.from_user.username if message.from_user else 'user'}. It's my first test message")