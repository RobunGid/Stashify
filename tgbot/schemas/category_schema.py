from typing import List

from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    
    name: str

    resources: "List[ResourceSchema]"
    
from resource_schema import ResourceSchema