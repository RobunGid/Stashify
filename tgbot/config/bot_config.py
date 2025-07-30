import logging
from pathlib import Path

from dotenv import dotenv_values
from aiogram import Dispatcher
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)

env_path = Path(__file__).parent.parent / '.env'

config = dotenv_values(dotenv_path=env_path)

if config["TOKEN"] is None:
	raise ValueError("Bot token is required in /tgbot/.env")

TOKEN = config["TOKEN"]


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage, echo=True)
