from dotenv import dotenv_values
from pathlib import Path

from aiogram import Dispatcher
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage

env_path = Path(__file__).parent.parent / '.env'

config = dotenv_values(dotenv_path=env_path)

if config["TOKEN"] is None:
	raise ValueError("Bot token is required in /tgbot/.env")

TOKEN = config["TOKEN"]

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
