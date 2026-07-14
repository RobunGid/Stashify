from dataclasses import dataclass

from aiogram_i18n import I18nContext
from application.formatters.base import (
    BaseDateFormatter,
    BaseTranslateContextBuilder,
    BaseVerifiedStatusFormatter,
)
from domain.entities.category_item import CategoryItemEntity
from domain.entities.resource_item import ResourceItemEntity


@dataclass
class I18nVerifiedStatusFormatter(BaseVerifiedStatusFormatter):
    def format_status(self, is_verified: bool) -> str:
        return "verified-yes" if is_verified else "verified-no"


@dataclass
class ResourceItemTranslateContextBuilder(BaseTranslateContextBuilder):
    verified_status_formatter: BaseVerifiedStatusFormatter
    date_formatter: BaseDateFormatter

    def build(
        self,
        resource_item_entity: ResourceItemEntity,
        category_item_entity: CategoryItemEntity,
        i18n: I18nContext,
    ) -> dict:
        return {
            "resource_item_name": resource_item_entity.name,
            "resource_item_description": resource_item_entity.description,
            "resource_item_links": resource_item_entity.links,
            "resource_item_category_name": category_item_entity.name,
            "is_resource_verified": i18n.get(
                self.verified_status_formatter.format_status(resource_item_entity.verified),
            ),
            "resource_item_tags": resource_item_entity.tags,
            "resource_item_created_at": self.date_formatter.format_date(resource_item_entity.created_at),
        }


@dataclass
class ResourceItemFormatter:
    context_builder: ResourceItemTranslateContextBuilder

    def format_resource_item(
        self,
        resource_item: ResourceItemEntity,
        category_item: CategoryItemEntity,
        i18n: I18nContext,
    ) -> str:
        context = self.context_builder.build(resource_item, category_item, i18n)
        return i18n.get("list-resources-item", **context)
