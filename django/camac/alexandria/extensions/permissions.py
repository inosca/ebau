from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from django.conf import settings

from .common import get_role


class CustomPermission(BasePermission):
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

        category = Category.objects.get(pk=request.data["category"]["id"])
        permission = category.metainfo["access"].get(
            get_role(request.caluma_info.context.user)
        )
        if not permission:
            return False

        return globals()[f"{permission}Permission"]().can_write(request)

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, document):
        permission = document.category.metainfo["access"].get(
            get_role(request.caluma_info.context.user)
        )
        if not permission:  # pragma: no cover
            return False

        if request.method == "DELETE":
            return globals()[f"{permission}Permission"]().can_destroy(request)

        return globals()[f"{permission}Permission"]().can_write(request)

    @permission_for(File)
    def has_permission_for_file(self, request):
        category = Document.objects.get(pk=request.data["document"]["id"]).category
        permission = category.metainfo["access"].get(
            get_role(request.caluma_info.context.user)
        )
        if not permission:
            return False

        return globals()[f"{permission}Permission"]().can_write(request)

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


class Permission:
    write = False
    destroy = False

    @classmethod
    def can_write(cls, request) -> bool:
        return cls.write

    @classmethod
    def can_destroy(cls, request) -> bool:
        return cls.destroy


class ReadPermission(Permission):
    pass


class WritePermission(Permission):
    write = True


class AdminPermission(WritePermission):
    destroy = True


class InternalReadPermission(ReadPermission):
    pass


class InternalAdminPermission(AdminPermission):
    pass