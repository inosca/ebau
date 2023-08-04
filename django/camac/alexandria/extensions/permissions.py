from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from django.conf import settings

from camac.user.utils import get_group

from .common import get_role

if settings.APPLICATION_NAME == "kt_gr":  # pragma: no cover
    import camac.alexandria.extensions.permissions_kt_gr as permissions
else:
    import camac.alexandria.extensions.permissions_base as permissions


class CustomPermission(BasePermission):
    def get_permission(self, name):
        return getattr(permissions, f"{name}Permission")()

    @permission_for(BaseModel)
    def has_permission_default(self, request):  # pragma: no cover
        if get_role(request.caluma_info.context.user) == "support":
            return True

        return False

    @permission_for(Document)
    def has_permission_for_document(self, request):
        # patch and delete are handled in object permissions
        if request.method != "POST":
            return True

        user = request.caluma_info.context.user
        category = Category.objects.get(pk=request.data["category"]["id"])
        permission = category.metainfo["access"].get(get_role(user))
        if not permission:
            return False

        return self.get_permission(permission).can_write(get_group(request))

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, document):
        user = request.caluma_info.context.user
        permission = document.category.metainfo["access"].get(get_role(user))
        if not permission:  # pragma: no cover
            return False

        if request.method == "DELETE":
            return self.get_permission(permission).can_destroy(
                get_group(request), document
            )

        return self.get_permission(permission).can_write(get_group(request), document)

    @permission_for(File)
    def has_permission_for_file(self, request):
        user = request.caluma_info.context.user
        category = Document.objects.get(pk=request.data["document"]["id"]).category
        permission = category.metainfo["access"].get(get_role(user))
        if not permission:
            return False

        return self.get_permission(permission).can_write(get_group(request))

    @permission_for(Tag)
    def has_permission_for_tag(self, request):
        if get_role(request.caluma_info.context.user) != settings.APPLICATION.get(
            "ALEXANDRIA", {}
        ).get("PUBLIC_ROLE", "public"):
            return True

        return False

    @object_permission_for(Tag)
    def has_object_permission_for_tag(self, request, tag):
        if get_role(request.caluma_info.context.user) == "support":
            return True

        if get_role(request.caluma_info.context.user) != settings.APPLICATION.get(
            "ALEXANDRIA", {}
        ).get("PUBLIC_ROLE", "public"):
            return tag.created_by_group == str(request.caluma_info.context.user.group)
