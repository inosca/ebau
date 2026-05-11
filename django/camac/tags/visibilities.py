from generic_permissions.visibilities import filter_queryset_for

from camac.tags.models import Keyword, StaticKeyword
from camac.user.permissions import get_role_name


class TagsVisibility:
    @filter_queryset_for(Keyword)
    def filter_keywords(self, queryset, request):
        role = get_role_name(request.group)

        if role in {"municipality", "service"}:
            return queryset.filter(service=request.group.service)
        elif role == "support":
            return queryset

        return queryset.none()

    @filter_queryset_for(StaticKeyword)
    def filter_static_keywords(self, queryset, request):
        role = get_role_name(request.group)
        service = request.group.service

        if role in {"municipality", "service"}:
            return queryset.filter(
                service=service.service_parent or service,
            )
        elif role == "support":
            return queryset

        return queryset.none()
