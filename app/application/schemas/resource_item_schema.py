from uuid import UUID

from application.schemas.base_schema import BaseSchema, BaseUpdateSchema
from domain.entities.resource_item import ResourceItemEntity, ResourceItemUpdateEntity
from pydantic import ConfigDict, Field


class BaseResourceItemSchema(BaseSchema[ResourceItemEntity]):
    resource_item_id: UUID

    name: str
    description: str
    links: str
    tags: str
    verified: bool

    category_item_id: UUID

    model_config = ConfigDict(from_attributes=True)

    def to_entity(self) -> ResourceItemEntity:
        return ResourceItemEntity(
            category_item_id=self.category_item_id,
            name=self.name,
            description=self.description,
            resource_item_id=self.resource_item_id,
            links=self.links,
            tags=self.tags,
            verified=self.verified,
        )


class ResourceItemSchema(BaseResourceItemSchema):
    category: "BaseCategoryItemSchema"
    ratings: list["BaseResourceRatingSchema"] = Field(
        default_factory=list,
    )
    images: list["BaseResourceImageSchema"] = Field(default_factory=list)
    quiz: "BaseQuizItemSchema | None" = Field(default=None)


class ResourceItemUpdateSchema(BaseUpdateSchema[ResourceItemUpdateEntity]):
    name: str | None = None
    description: str | None = None
    links: str | None = None
    tags: str | None = None
    verified: bool | None = None

    category_item_id: UUID | None = None

    def to_entity(self) -> ResourceItemUpdateEntity:
        return ResourceItemUpdateEntity(
            name=self.name,
            description=self.description,
            links=self.links,
            tags=self.tags,
            verified=self.verified,
            category_item_id=self.category_item_id,
        )


from application.schemas.category_item_schema import BaseCategoryItemSchema  # noqa
from application.schemas.quiz_item_schema import BaseQuizItemSchema  # noqa
from application.schemas.resource_image_schema import BaseResourceImageSchema  # noqa
from application.schemas.resource_rating_schema import (  # noqa
    BaseResourceRatingSchema,
)
