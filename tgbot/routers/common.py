from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Hello, {message.from_user.username if message.from_user else 'user'}. It's my first test message")