from uuid import UUID, uuid4

from application.schemas.base_schema import BaseSchema
from domain.entities.category_item import CategoryItemEntity
from pydantic import Field


class BaseCategoryItemSchema(BaseSchema[CategoryItemEntity]):
    category_item_id: UUID = Field(default_factory=uuid4)

    name: str

    def to_entity(self) -> CategoryItemEntity:
        return CategoryItemEntity(category_item_id=self.category_item_id, name=self.name)


class CategoryItemSchema(BaseCategoryItemSchema):
    resources: list[BaseResourceItemSchema] = Field(default_factory=list)


from application.schemas.resource_schema import BaseResourceItemSchema  # noqa
