from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseResourceItemSchema(BaseModel):
    resource_item_id: UUID

    name: str
    description: str
    links: str
    tags: str
    verified: bool

    category_id: UUID
    quiz: "QuizSchemaWithoutResource | None" = Field(default=None)

    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResourceItemSchema(BaseResourceItemSchema):
    category: "CategoryItemSchemaWithoutResources"
    ratings: list["ResourceRatingWithoutUserAndResourceSchema"] = Field(
        default_factory=list,
    )
    images: list["ResourceImageWithoutResourceSchema"] = Field(default_factory=list)


from schemas.category_item_schema import CategoryItemSchemaWithoutResources  # noqa
from schemas.quiz_schema import QuizSchemaWithoutResource  # noqa
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema  # noqa
from schemas.resource_rating_schema import (  # noqa
    ResourceRatingWithoutUserAndResourceSchema,
)
