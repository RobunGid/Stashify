from dataclasses import dataclass

from aiogram_i18n import I18nContext
from formaters.base import BaseFormatter

from schemas.resource_schema import ResourceItemSchema


@dataclass
class ResourceItemFormatter(BaseFormatter):
    @staticmethod
    def translate_resource_item(resource_item: ResourceItemSchema, i18n: I18nContext):
        created_at = resource_item.created_at

        return i18n.get(
            "list-resources-item",
            resource_item_name=resource_item.name,
            resource_item_description=resource_item.description,
            resource_item_links=resource_item.links,
            resource_item_category_name=resource_item.category.name,
            is_resource_verified="✅ Yes" if resource_item.verified else "❌ No",
            resource_item_tags=resource_item.tags,
            resource_item_created_at=created_at,
        )
