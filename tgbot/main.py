import asyncio

from config.bot_config import dp, bot
from routers import common
from database.orm import init_models
from database.models import *

async def main():
    await init_models()
    dp.include_routers(common.router)
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())