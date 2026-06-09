from pydantic import BaseModel, Field, UUID4


class CategorySchemaWithoutResources(BaseModel):
    category_id: UUID4

    name: str


class CategorySchema(CategorySchemaWithoutResources):
    resources: list[ResourceSchemaWithoutCategory] = Field(default_factory=list)


from schemas.resource_schema import ResourceSchemaWithoutCategory  # noqa
