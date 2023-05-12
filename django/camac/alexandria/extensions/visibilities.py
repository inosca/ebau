from alexandria.core.visibilities import BaseVisibility, filter_queryset_for
from alexandria.core.models import BaseModel, Document, File, Category, Tag
from django.db.models import Q
from django.conf import settings


class CustomVisibility(BaseVisibility):
    def get_role(self, user):
        group = user.get_default_group()
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        return perms.get(group.role.name) if group else "public"

    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        if self.get_role(request.user) == settings.APPLICATION.get("ADMIN_GROUP"):
            return queryset
        return queryset.none()

    def document_file_filter(self, user, prefix=""):
        role = str(self.get_role(user))
        normal_permissions = ["Admin", "Read", "Write"]
        visibility_filter = {}
        for permission in normal_permissions:
            visibility_filter[role] = permission

        return Q(
            # first: directly readable
            Q(
                **{
                    f"{prefix}category__metainfo__access__contained_by": visibility_filter
                }
            )
            |
            # second: categories where only documents from my own service are readable
            Q(
                **{
                    f"{prefix}category__metainfo__access__{role}__icontains": "Internal",
                    f"{prefix}created_by_group": user.get_default_group().pk,
                }
            )
            # third: instances where i'm invitee
            | Q(
                Q(**{f"{prefix}category__metainfo__access__has_key": "applicant"}),
                Q(instance__involved_applicants__invitee=user) | Q(instance__user=user),
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
        return queryset.filter(
            metainfo__access__has_key=str(self.get_role(request.user))
        )

    @filter_queryset_for(Tag)
    def filter_queryset_for_tag(self, queryset, request):
        public_tags = Q(pk__in=settings.APPLICATION.get("ALEXANDRIA.PUBLIC_TAGS", []))
        if self.get_role(request.user) == settings.APPLICATION.get(
            "PORTAL_GROUP"
        ):  # applicant role
            return queryset.filter(public_tags)

        return queryset.filter(
            Q(created_by_group=request.user.get_default_group().pk) | public_tags
        )
