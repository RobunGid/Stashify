from application.formatters.base import BaseDateFormatter, BaseVerifiedStatusFormatter, DefaultDateFormatter
from application.formatters.resource_item import (
    I18nVerifiedStatusFormatter,
    ResourceItemFormatter,
    ResourceItemTranslateContextBuilder,
)
from dishka import AnyOf, provide, Provider, Scope


class FormattersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_date_formatter(
        self,
    ) -> AnyOf[BaseDateFormatter, DefaultDateFormatter]:
        return DefaultDateFormatter()

    @provide(scope=Scope.REQUEST)
    def get_verified_status_formatter(
        self,
    ) -> AnyOf[BaseVerifiedStatusFormatter, I18nVerifiedStatusFormatter]:
        return I18nVerifiedStatusFormatter()

    @provide(scope=Scope.REQUEST)
    def get_resource_item_formatter(
        self,
        date_formatter: BaseDateFormatter,
        verified_status_formatter: BaseVerifiedStatusFormatter,
    ) -> ResourceItemFormatter:
        return ResourceItemFormatter(
            context_builder=ResourceItemTranslateContextBuilder(
                date_formatter=date_formatter,
                verified_status_formatter=verified_status_formatter,
            ),
        )
