from functools import lru_cache

from containers.providers.common import CommonProvider
from containers.providers.repositories import RepositoriesProvider
from containers.providers.services import ServicesProvider
from dishka import AsyncContainer, make_async_container


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(CommonProvider(), RepositoriesProvider(), ServicesProvider())
