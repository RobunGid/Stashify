from application.keyboards.base import BackToMenuKeyboardBuilderMixin
from application.keyboards.resources import ResourceItemKeyboardBuilder, ResourceListKeyboardBuilder


class SearchResourceItemKeyboardBuilder(ResourceItemKeyboardBuilder):
    def _back_callback(self) -> str:
        return "search_resource"


class SearchResourceListKeyboardBuilder(ResourceListKeyboardBuilder, BackToMenuKeyboardBuilderMixin):
    pass
