from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from alexandria.core.models import BaseModel, Document, File, Category, Tag
from .. import settings
from django.db.models import Q


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        if request.user.role == "support":
            return queryset
        return queryset.none()

    def document_file_filter(self, user, prefix=""):
        normal_permissions = ["Admin", "Read", "Write"]
        visibility_filter = {}
        for permission in normal_permissions:
            visibility_filter[user.role] = permission

        return Q(
            # first: directly readable
            Q(**{f"{prefix}category__meta__access__contained_by": visibility_filter})
            |
            # second: categories where only documents from my own service are readable
            Q(
                **{
                    f"{prefix}category__meta__access__{user.role}__icontains": "Internal",
                    f"{prefix}created_by_group": user.group,
                }
            )
            # third: instances where i'm invitee
            | Q(
                Q(**{f"{prefix}category__meta__access__has_key": "applicant"}),
                Q(instances__involved_applicants__invitee=user)
                | Q(instances__user=user),
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
        return queryset.filter(meta__access__has_key=[request.user.role])

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        public_tags = Q(pk__in=settings.PUBLIC_TAGS)
        if request.user.role == "applicant":
            return queryset.filter(public_tags)

        return queryset.filter(Q(created_by_group=request.user.group) | public_tags)

