from pydantic import BaseModel


class BaseFiltersSchema(BaseModel):
    count: int
    offset: int
