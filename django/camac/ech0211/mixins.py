from django.conf import settings

from camac.constants.kt_schwyz import FORM_DESCRIPTIONS
from camac.instance.mixins import InstanceQuerysetMixin


class ECHInstanceQuerysetMixin(InstanceQuerysetMixin):
    def get_base_queryset(self):
        queryset = super().get_base_queryset()

        if settings.APPLICATION_NAME == "kt_schwyz":
            return queryset.filter(form__description__in=FORM_DESCRIPTIONS)

        return queryset.exclude(case__document__form_id__in=settings.ECH_EXCLUDED_FORMS)
