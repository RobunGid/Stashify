from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from application.containers.factories import get_container

from settings.config import Config

container = get_container()
config = container.get_sync(Config)

bot = Bot(
    config.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

storage = MemoryStorage()

dp = Dispatcher(storage=storage, echo=True)
