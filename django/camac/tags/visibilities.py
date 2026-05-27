from generic_permissions.visibilities import filter_queryset_for

from camac.tags.models import Keyword, StaticKeyword
from camac.user.permissions import get_role_name


class TagsVisibility:
    def _filter_by_service(self, queryset, request, service):
        role = get_role_name(request.group)

        if role in {"municipality", "service"}:
            return queryset.filter(service=service)
        elif role == "support":
            return queryset

        return queryset.none()

    @filter_queryset_for(Keyword)
    def filter_keywords(self, queryset, request):
        return self._filter_by_service(queryset, request, request.group.service)

    @filter_queryset_for(StaticKeyword)
    def filter_static_keywords(self, queryset, request):
        service = request.group.service
        return self._filter_by_service(
            queryset, request, service.service_parent or service
        )
