from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ResourceSchemaWithoutCategory(BaseModel):
    resource_item_id: UUID

    name: str
    description: str
    links: str
    tags: str
    verified: bool = Field(default=False)

    category_id: UUID
    quiz: "QuizSchemaWithoutResource | None" = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchemaWithoutResources"
    ratings: list["ResourceRatingWithoutUserAndResourceSchema"] = Field(
        default_factory=list,
    )
    images: list["ResourceImageWithoutResourceSchema"] = Field(default_factory=list)


from schemas.category_schema import CategorySchemaWithoutResources  # noqa
from schemas.quiz_schema import QuizSchemaWithoutResource  # noqa
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema  # noqa
from schemas.resource_rating_schema import (  # noqa
    ResourceRatingWithoutUserAndResourceSchema,
)
