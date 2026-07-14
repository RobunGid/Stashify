from functools import lru_cache

from application.containers.providers.common import CommonProvider
from application.containers.providers.formatters import FormattersProvider
from application.containers.providers.repositories import RepositoriesProvider
from application.containers.providers.services import ServicesProvider
from dishka import AsyncContainer, make_async_container


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(CommonProvider(), RepositoriesProvider(), ServicesProvider(), FormattersProvider())
