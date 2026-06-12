from uuid import UUID

from application.schemas.base_schema import BaseSchema
from pydantic import ConfigDict, Field


class BaseResourceItemSchema(BaseSchema):
    resource_item_id: UUID

    name: str
    description: str
    links: str
    tags: str
    verified: bool

    category_id: UUID
    quiz: "BaseQuizItemSchema | None" = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class ResourceItemSchema(BaseResourceItemSchema):
    category: "BaseCategoryItemSchema"
    ratings: list["ResourceRatingWithoutUserAndResourceSchema"] = Field(
        default_factory=list,
    )
    images: list["ResourceImageWithoutResourceSchema"] = Field(default_factory=list)


from application.schemas.category_item_schema import BaseCategoryItemSchema  # noqa
from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
from application.schemas.resource_image_schema import ResourceImageWithoutResourceSchema  # noqa
from application.schemas.resource_rating_schema import (  # noqa
    ResourceRatingWithoutUserAndResourceSchema,
)
