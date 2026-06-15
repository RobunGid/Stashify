from dataclasses import dataclass

from aiogram_i18n import I18nContext
from application.formaters.base import BaseFormatter
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


@dataclass
class ResourceItemFormatter(BaseFormatter):
    @staticmethod
    def translate_resource_item(
        resource_item: ResourceItemEntity,
        category_item: CategoryItemEntity,
        i18n: I18nContext,
    ):
        created_at = resource_item.created_at.strftime("%d.%m.%Y %H:%M")

        return i18n.get(
            "list-resources-item",
            resource_item_name=resource_item.name,
            resource_item_description=resource_item.description,
            resource_item_links=resource_item.links,
            resource_item_category_name=category_item.name,
            is_resource_verified="✅ Yes" if resource_item.verified else "❌ No",
            resource_item_tags=resource_item.tags,
            resource_item_created_at=created_at,
        )
