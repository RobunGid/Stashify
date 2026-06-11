import asyncio

from aiogram import Bot, Dispatcher

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from application.routers import common, manage_users, menu
from application.routers.manage_categories.router import router as manage_categories_router
from application.routers.manage_quizes.router import router as manage_quizes_router
from application.routers.manage_resources.router import router as manage_resources_router
from application.routers.resources.router import router as list_resources_router
from application.routers.search_resource.router import router as search_resource_router
from containers.factories import get_container

from database.base import init_models


async def main():
    await init_models()
    container = get_container()
    async with container() as request_container:
        dp = await request_container.get(Dispatcher)
        bot = await request_container.get(Bot)

        dp.include_routers(
            common.router,
            menu.router,
            manage_resources_router,
            manage_categories_router,
            manage_quizes_router,
            list_resources_router,
            search_resource_router,
            manage_users.router,
        )

        i18n_middleware = I18nMiddleware(core=FluentRuntimeCore(path="locales/{locale}"))

        dp.message.middleware(i18n_middleware)
        i18n_middleware.setup(dispatcher=dp)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
