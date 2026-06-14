from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.resource_favorite import ResourceFavoriteFilters


class ResourceFavoriteFiltersSchema(BaseFiltersSchema[ResourceFavoriteFilters]):
    user_account_id: UUID | None = None
    count: int | None = None

    entity_cls: type[ResourceFavoriteFilters] = ResourceFavoriteFilters

    def to_entity(self) -> ResourceFavoriteFilters:
        return ResourceFavoriteFilters(count=self.count, offset=self.offset, user_account_id=self.user_account_id)
