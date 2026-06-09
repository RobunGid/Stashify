from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, UUID4

from utils.OptionalSchema import AllOptional


def default_category():
    return CategorySchemaWithoutResources(id=uuid4(), name="")


class ResourceSchemaWithoutCategory(BaseModel):
    id: UUID4

    name: str
    description: str
    links: str
    tags: str
    verified: bool = Field(default_factory=lambda: False)

    category_id: UUID4
    quiz: Optional["QuizSchemaWithoutResource"] = Field(default_factory=lambda: None)

    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchemaWithoutResources" = Field(default_factory=default_category)
    ratings: List["ResourceRatingWithoutUserAndResourceSchema"] = Field(
        default_factory=list,
    )
    images: List["ResourceImageWithoutResourceSchema"] = Field(default_factory=list)


class UpdateResourceSchemaWithoutCategory(
    ResourceSchemaWithoutCategory,
    metaclass=AllOptional,
): ...


from schemas.category_schema import CategorySchemaWithoutResources
from schemas.quiz_schema import QuizSchemaWithoutResource
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
