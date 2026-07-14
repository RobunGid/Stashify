from domain.filters.base import BaseFilters
from sqlalchemy import Select


def apply_pagination_to_statement(statement: Select, filters: BaseFilters):
    if filters.offset is not None:
        statement = statement.offset(filters.offset)
    if filters.count is not None:
        statement = statement.limit(filters.count)
    return statement
