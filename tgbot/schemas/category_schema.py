from typing import List

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CategorySchema(BaseModel):
    id: UUID4
    
    name: str

    resources: "List[ResourceSchema]" = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
    
from .resource_schema import ResourceSchema