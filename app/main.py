import asyncio

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from application.containers.factories import get_container
from application.middlewares.create_user import CreateUserMiddleware
from application.middlewares.delete_message import DeleteOldMessagesMiddleware
from application.routers import common, menu
from application.routers.manage_categories.router import router as manage_categories_router
from application.routers.manage_quizes.router import router as manage_quizes_router
from application.routers.manage_resources.router import router as manage_resources_router
from application.routers.manage_users import router as manage_users_router
from application.routers.resources.router import router as list_resources_router
from application.routers.search_resource.router import router as search_resource_router
from dishka.integrations.aiogram import setup_dishka

from database.init import init_models
from settings.aiogram import bot, dp


async def main():
    await init_models()
    container = get_container()

    dp.include_routers(
        common.router,
        menu.router,
        manage_resources_router,
        manage_categories_router,
        manage_quizes_router,
        list_resources_router,
        search_resource_router,
        manage_users_router,
    )

    i18n_middleware = I18nMiddleware(core=FluentRuntimeCore(path="domain/locales/{locale}"))
    create_user_middleware = CreateUserMiddleware(container)
    delete_old_messages_middleware = DeleteOldMessagesMiddleware()

    dp.message.middleware(i18n_middleware)
    dp.message.outer_middleware(create_user_middleware)
    dp.callback_query.outer_middleware(create_user_middleware)
    dp.message.middleware(delete_old_messages_middleware)
    dp.callback_query.outer_middleware(delete_old_messages_middleware)
    dp.update.middleware()
    i18n_middleware.setup(dispatcher=dp)

    setup_dishka(container, dp, auto_inject=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
