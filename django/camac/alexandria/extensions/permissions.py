from alexandria.core.models import BaseModel, Category, Document, File, Tag
from alexandria.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from django.conf import settings

from camac.user.utils import get_group

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

        user = request.caluma_info.context.user
        category = Category.objects.get(pk=request.data["category"]["id"])
        permission = category.metainfo["access"].get(get_role(user))
        if not permission:
            return False

        return globals()[f"{permission}Permission"]().can_write(get_group(request))

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, document):
        user = request.caluma_info.context.user
        permission = document.category.metainfo["access"].get(get_role(user))
        if not permission:  # pragma: no cover
            return False

        if request.method == "DELETE":
            return globals()[f"{permission}Permission"]().can_destroy(
                get_group(request), document
            )

        return globals()[f"{permission}Permission"]().can_write(
            get_group(request), document
        )

    @permission_for(File)
    def has_permission_for_file(self, request):
        user = request.caluma_info.context.user
        category = Document.objects.get(pk=request.data["document"]["id"]).category
        permission = category.metainfo["access"].get(get_role(user))
        if not permission:
            return False

        return globals()[f"{permission}Permission"]().can_write(get_group(request))

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
    def can_write(cls, group, document=None) -> bool:
        return cls.write

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return cls.destroy


class ReadPermission(Permission):
    """Read permission."""

    pass


class WritePermission(Permission):
    """Read and write permission."""

    write = True


class AdminPermission(WritePermission):
    """Read, write and delete permission."""

    destroy = True


class AdminServicePermission(AdminPermission):
    """Read and write permissions for all attachments, but delete only on attachments owned by the current service."""

    @classmethod
    def is_owned_by_service(cls, group, document) -> bool:
        return not document or int(document.created_by_group) == group.service.pk

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return cls.is_owned_by_service(group, document) and super().can_destroy(
            group, document
        )


class InternalReadPermission(ReadPermission):
    """Read permission on attachments owned by the current service."""

    pass


class InternalAdminPermission(AdminServicePermission):
    """Read, write and delete permission on attachments owned by the current service."""

    @classmethod
    def can_write(cls, group, document) -> bool:
        return cls.is_owned_by_service(group, document) and super().can_write(
            group, document
        )


class AdminDeletableStatePermission(AdminPermission):
    """Read and write permission, but delete only in certain states."""

    deletable_states = []

    @classmethod
    def in_deleteable_state(cls, group, document) -> bool:
        return not document or (
            document.instance_document.instance.instance_state.name
            in cls.deletable_states
        )

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return cls.in_deleteable_state(group, document) and super().can_destroy(
            group,
            document,
        )


# Kt. Gr specific permissions
class KtGrAREPermission(Permission):
    @classmethod
    def is_are_service(cls, group) -> bool:
        return group.service.name == "Amt für Raumentwicklung (ARE)"


class KtGrAdminServiceAREPermission(KtGrAREPermission, AdminServicePermission):
    """Read, write, delete only for ARE Service."""

    @classmethod
    def can_write(cls, group, document=None) -> bool:
        return cls.is_are_service(group) and super().can_write(group, document)

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return cls.is_are_service(group) and super().can_destroy(group, document)


class KtGrReadARECirculationDeletablePermission(
    KtGrAREPermission, AdminDeletableStatePermission
):
    """
    Special permission for the category Stellungnahmen ans ARE.

    Service ARE: Read
    Other services: Read Internal, write, delete only in circulation
    """

    deletable_states = ["circulation"]

    @classmethod
    def can_write(cls, group, document=None) -> bool:
        return not cls.is_are_service(group) and super().can_write(group, document)

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return not cls.is_are_service(group) and super().can_destroy(group, document)
