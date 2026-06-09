from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, UUID4

from utils.OptionalSchema import AllOptional


class ResourceSchemaWithoutCategory(BaseModel):
    resource_id: UUID4

    name: str
    description: str
    links: str
    tags: str
    verified: bool = Field(default=False)

    category_id: UUID4
    quiz: "QuizSchemaWithoutResource | None" = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)


class ResourceSchema(ResourceSchemaWithoutCategory):
    category: "CategorySchemaWithoutResources"
    ratings: list["ResourceRatingWithoutUserAndResourceSchema"] = Field(
        default_factory=list,
    )
    images: list["ResourceImageWithoutResourceSchema"] = Field(default_factory=list)


class UpdateResourceSchemaWithoutCategory(
    ResourceSchemaWithoutCategory,
    metaclass=AllOptional,
):
    pass


from schemas.category_schema import CategorySchemaWithoutResources
from schemas.quiz_schema import QuizSchemaWithoutResource
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema
from schemas.resource_rating_schema import ResourceRatingWithoutUserAndResourceSchema
