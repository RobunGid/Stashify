from keyboards.base import BackToMenuKeyboardBuilderMixin
from keyboards.resources import ResourceItemKeyboardBuilder, ResourceListKeyboardBuilder


class SearchResourceItemKeyboardBuilder(ResourceItemKeyboardBuilder):
    def _back_callback(self) -> str:
        return "search_resource"


class SearchResourceListKeyboardBuilder(ResourceListKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
    pass
