from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from django.conf import settings
from django.db.models import Q

from .common import get_role


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
            aggregated_filter |= Q(
                **{
                    f"{prefix}category__metainfo__access__{role}__istartswith": permission
                }
            )

        return (
            aggregated_filter
            | Q(
                # categories where only documents from my own service are readable
                **{
                    f"{prefix}category__metainfo__access__{role}__icontains": "Internal",
                    f"{prefix}created_by_group": user.group,
                }
            )
            | Q(
                # instances where i'm invitee
                Q(**{f"{prefix}category__metainfo__access__has_key": "applicant"}),
                Q(
                    **{
                        f"{prefix}instance_document__instance__involved_applicants__invitee__username": user.username
                    }
                )
                | Q(
                    **{
                        f"{prefix}instance_document__instance__user__username": user.username
                    }
                ),
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

        # TODO: need to evaluate some permissions to avoid displaying categories at useless times
        return queryset.filter(
            metainfo__access__has_key=get_role(request.caluma_info.context.user)
        )

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        if get_role(request.caluma_info.context.user) == "support":
            return queryset

        public_tags = Q(
            pk__in=settings.APPLICATION.get("ALEXANDRIA", {}).get("PUBLIC_TAGS", [])
        )
        if get_role(request.caluma_info.context.user) == settings.APPLICATION.get(
            "ALEXANDRIA", {}
        ).get("PUBLIC_ROLE", "public"):
            return queryset.filter(public_tags)

        return queryset.filter(
            Q(created_by_group=request.caluma_info.context.user.group) | public_tags
        )
