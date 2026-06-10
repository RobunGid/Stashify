from uuid import UUID

from pydantic import BaseModel, Field


class CategorySchemaWithoutResources(BaseModel):
    category_id: UUID

    name: str


class CategorySchema(CategorySchemaWithoutResources):
    resources: list[BaseResourceItemSchema] = Field(default_factory=list)


from schemas.resource_schema import BaseResourceItemSchema  # noqa
