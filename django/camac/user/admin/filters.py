from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class DisabledFilter(SimpleListFilter):
    title = _("Disabled?")
    parameter_name = "disabled"

    def lookups(self, request, model_admin):
        return (
            (1, _("Yes")),
            (0, _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            return queryset.filter(disabled=value)

        return queryset
