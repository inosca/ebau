from django.db.models import Q
from generic_permissions.visibilities import filter_queryset_for

from document_merge_service.api.models import Template
from document_merge_service.extensions.utils import get_service_data


class CustomVisibility:
    @filter_queryset_for(Template)
    def filter_templates(self, queryset, request):
        service_data = get_service_data(request)

        return queryset.filter(
            # For own templates visibility we filter by services from request
            Q(meta__service__in=service_data.get("service_ids", []))
            # For shared templates visibility we filter by service_groups from request
            | Q(meta__service_group__in=service_data.get("service_group_slugs", []))
            # For system templates visibility we filter by empty meta
            | (Q(meta__service__isnull=True) & Q(meta__service_group__isnull=True))
        )
