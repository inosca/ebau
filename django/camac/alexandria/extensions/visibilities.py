from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from django.conf import settings
from django.db.models import Q

from .common import get_role


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        if get_role(request.user) == "support":
            return queryset
        return queryset.none()

    def document_file_filter(self, user, prefix=""):
        role = get_role(user)
        normal_permissions = ["Admin", "Read", "Write"]

        aggregated_filter = Q()
        for permission in normal_permissions:
            # first: directly readable
            aggregated_filter |= Q(
                **{f"{prefix}category__metainfo__access__contains": {role: permission}}
            )

        return (
            aggregated_filter
            | Q(
                # second: categories where only documents from my own service are readable
                **{
                    f"{prefix}category__metainfo__access__{role}__icontains": "Internal",
                    f"{prefix}created_by_group": user.get_default_group().pk,
                }
            )
            | Q(
                # third: instances where i'm invitee
                Q(**{f"{prefix}category__metainfo__access__has_key": "applicant"}),
                Q(
                    **{
                        f"{prefix}instance_document__instance__involved_applicants__invitee": user
                    }
                )
                | Q(**{f"{prefix}instance_document__instance__user": user}),
            )
        )

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, queryset, request):
        return queryset.filter(self.document_file_filter(request.user)).distinct()

    @filter_queryset_for(File)
    def filter_queryset_for_file(self, queryset, request):
        # Limitations for `Document` should also be enforced on `File`.
        return queryset.filter(
            self.document_file_filter(request.user, "document__")
        ).distinct()

    @filter_queryset_for(Category)
    def filter_queryset_for_category(self, queryset, request):
        # category is visible when the role is in the access, regardless of the permission
        return queryset.filter(metainfo__access__has_key=str(get_role(request.user)))

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        public_tags = Q(pk__in=settings.APPLICATION.get("ALEXANDRIA.PUBLIC_TAGS", []))
        if get_role(request.user) == settings.APPLICATION.get(
            "PORTAL_GROUP"
        ):  # applicant role
            return queryset.filter(public_tags)

        return queryset.filter(
            Q(created_by_group=request.user.get_default_group().pk) | public_tags
        )
