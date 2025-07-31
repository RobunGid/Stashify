import asyncio

from config.bot_config import dp, bot
from routers import common, menu, manage_categories, manage_quizes, manage_users
from routers.manage_resources.router import router as manage_resources_router
from database.orm import init_models
from database.models import *

async def main():
    await init_models()
    dp.include_routers(
        common.router, 
        menu.router,
        manage_resources_router,
        manage_categories.router,
        manage_quizes.router,
        manage_users.router,
    )
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())