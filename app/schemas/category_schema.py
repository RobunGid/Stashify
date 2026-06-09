from typing import List

from pydantic import BaseModel, Field, UUID4

from schemas.resource_schema import ResourceSchemaWithoutCategory
from utils.OptionalSchema import AllOptional


class CategorySchemaWithoutResources(BaseModel):
    category_id: UUID4

    name: str


class CategorySchema(CategorySchemaWithoutResources):
    resources: List[ResourceSchemaWithoutCategory] = Field(default_factory=list)


class UpdateCategorySchema(CategorySchemaWithoutResources, metaclass=AllOptional):
    pass
