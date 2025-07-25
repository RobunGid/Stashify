import asyncio

from config.bot_config import dp, bot
from routers import common

async def main():
    dp.include_routers(common.router)
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())