from uuid import UUID

from pydantic import BaseModel, Field


class CategoryItemSchemaWithoutResources(BaseModel):
    category_id: UUID

    name: str


class CategoryItemSchema(CategoryItemSchemaWithoutResources):
    resources: list[BaseResourceItemSchema] = Field(default_factory=list)


from schemas.resource_schema import BaseResourceItemSchema  # noqa
