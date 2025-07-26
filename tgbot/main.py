import asyncio

from config.bot_config import dp, bot
from routers import common
from database.orm import init_models
from database.models import user, resource, category, rating, quiz, quiz_question, quiz_result

async def main():
    dp.include_routers(common.router)
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(init_models())
    asyncio.run(main())