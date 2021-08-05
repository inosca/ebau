from django.conf import settings

from camac.instance.mixins import InstanceQuerysetMixin


class ECHInstanceQuerysetMixin(InstanceQuerysetMixin):
    def get_base_queryset(self):
        return (
            super()
            .get_base_queryset()
            .exclude(case__document__form_id__in=settings.ECH_EXCLUDED_FORMS)
        )
