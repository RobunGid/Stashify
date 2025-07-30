from typing import List

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CategorySchema(BaseModel):
    id: UUID4
    
    name: str

    resources: "List[ResourceSchemaWithoutCategory]" = Field(default_factory=list, exclude=("category",))
    model_config = ConfigDict(from_attributes=True, recursive=False)
    
from .resource_schema import ResourceSchemaWithoutCategory