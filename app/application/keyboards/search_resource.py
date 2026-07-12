from dataclasses import dataclass
from uuid import UUID

from application.keyboards.base import BackToSearchResourcesKeyboardBuilderMixin, BaseBackKeyboardBuilder
from application.keyboards.resources import (
    ListSearchResourcesItemCallbackFactory,
    ResourceItemDetailsCallbackFactory,
    ResourceItemKeyboardBuilder,
)


@dataclass
class SearchResourceItemKeyboardBuilder(ResourceItemKeyboardBuilder):
    def _back_callback(self) -> str:
        return ListSearchResourcesItemCallbackFactory(page=0, context="menu", query=self.query).pack()

    def _navigation_callback(self, item_id: UUID) -> str:
        return ResourceItemDetailsCallbackFactory(
            resource_item_id=item_id,
            action="select",
            context="srch",
            rating=None,
        ).pack()


@dataclass
class BackToSearchResourcesKeyboardBuilder(BaseBackKeyboardBuilder, BackToSearchResourcesKeyboardBuilderMixin):
    pass
