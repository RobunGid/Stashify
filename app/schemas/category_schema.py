from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, UUID4

from utils.OptionalSchema import AllOptional

if TYPE_CHECKING:
    from schemas.resource_schema import ResourceSchemaWithoutCategory


class CategorySchemaWithoutResources(BaseModel):
    category_id: UUID4

    name: str


class CategorySchema(CategorySchemaWithoutResources):
    resources: list[ResourceSchemaWithoutCategory] = Field(default_factory=list)


class UpdateCategorySchema(CategorySchemaWithoutResources, metaclass=AllOptional):
    pass
