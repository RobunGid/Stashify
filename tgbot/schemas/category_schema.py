from typing import List

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CategorySchemaWithoutResources(BaseModel):
    id: UUID4
    
    name: str

class CategorySchema(CategorySchemaWithoutResources):
    resources: "List[ResourceSchemaWithoutCategory]" = Field(default_factory=list)
    
    
from .resource_schema import ResourceSchemaWithoutCategory