from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from django.conf import settings
from django.db.models import Q

from .common import get_role


def get_category_access_rule(prefix, value, role=None, lookup=None):
    query = (
        f"metainfo__access__{role}__{lookup}" if role else "metainfo__access__has_key"
    )

    return Q(
        Q(**{f"{prefix}category__{query}": value})
        | Q(**{f"{prefix}category__parent__{query}": value})
    )


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):  # pragma: no cover
        if get_role(request.caluma_info.context.user) != "public":
            return queryset

        return queryset.none()

    def document_and_file_filter(self, user, prefix=""):
        role = get_role(user)
        normal_permissions = ["Admin", "Read", "Write"]

        aggregated_filter = Q()
        for permission in normal_permissions:
            # directly readable categories
            aggregated_filter |= get_category_access_rule(
                prefix, permission, role, "istartswith"
            )

        return (
            aggregated_filter
            | Q(
                # categories where only documents from my own service are readable
                get_category_access_rule(prefix, "Internal", role, "icontains")
                & Q(**{f"{prefix}created_by_group": user.group})
            )
            | Q(
                # instances where i'm invitee
                get_category_access_rule(prefix, "applicant")
                & Q(
                    **{
                        f"{prefix}instance_document__instance__involved_applicants__invitee__username": user.username
                    }
                )
            )
        )

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        return queryset.filter(
            self.document_and_file_filter(request.caluma_info.context.user)
        ).distinct()

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        # Limitations for `Document` should also be enforced on `File`.
        return queryset.filter(
            self.document_and_file_filter(
                request.caluma_info.context.user, "document__"
            )
        ).distinct()

    @filter_queryset_for(Category)
    def filter_queryset_for_category(self, queryset, request):
        if "swagger" in request.path:  # pragma: no cover
            return queryset.none()

        role = get_role(request.caluma_info.context.user)
        # TODO: need to evaluate some permissions to avoid displaying categories at useless times
        return queryset.filter(
            Q(metainfo__access__has_key=role)
            | Q(parent__metainfo__access__has_key=role)
        )

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        if get_role(request.caluma_info.context.user) == "support":
            return queryset

        if get_role(request.caluma_info.context.user) == settings.APPLICATION.get(
            "ALEXANDRIA", {}
        ).get("PUBLIC_ROLE", "public"):
            return queryset.none()

        return queryset.filter(created_by_group=request.caluma_info.context.user.group)
