from typing import List

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: str
    
    name: str

    resources: "List[ResourceSchema]" = Field(default_factory=list)
    
from .resource_schema import ResourceSchema