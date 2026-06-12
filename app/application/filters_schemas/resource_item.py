from uuid import UUID

from application.filters_schemas.base import BaseFiltersSchema
from domain.filters.resource_item import ResourceItemFilters


class ResourceItemFiltersSchema(BaseFiltersSchema):
    entity_cls: type[ResourceItemFilters] = ResourceItemFilters
