import asyncio

from database.orm import init_models
from routers import common, manage_users, menu
from routers.list_favorites.router import router as list_favorites_router
from routers.list_resources.router import router as list_resources_router
from routers.manage_categories.router import router as manage_categories_router
from routers.manage_quizes.router import router as manage_quizes_router
from routers.manage_resources.router import router as manage_resources_router
from routers.search_resource.router import router as search_resource_router
from settings.config import bot, dp


async def main():
    await init_models()
    dp.include_routers(
        common.router,
        menu.router,
        manage_resources_router,
        manage_categories_router,
        manage_quizes_router,
        list_resources_router,
        search_resource_router,
        list_favorites_router,
        manage_users.router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
