from django.db.models import Q
from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from alexandria.core.models import BaseModel, Document, File


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        if request.user.is_superuser:
            return queryset

        return queryset.none()

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        # own and group
        return queryset.filter(
            Q(created_by_user=request.user.username) |
            Q(created_by_group__in=request.user.groups)
        )

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        # Limitations for `Document` should also be enforced on `File`.
        return queryset.filter(
            Q(document__created_by_user=request.user.username) |
            Q(document__created_by_group__in=request.user.groups)
        )
