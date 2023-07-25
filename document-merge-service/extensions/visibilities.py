from django.db.models import Q
from generic_permissions.visibilities import filter_queryset_for

from document_merge_service.api.models import Template
from document_merge_service.extensions.utils import get_services


class CustomVisibility:
    @filter_queryset_for(Template)
    def filter_templates(self, queryset, request):
        return queryset.filter(
            Q(meta__service__in=get_services(request)) | Q(meta__service__isnull=True)
        )
