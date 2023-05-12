from alexandria.core.permissions import (
    BasePermission,
    permission_for,
    object_permission_for,
)
from alexandria.core.models import BaseModel, Category, Document, File, Tag


"""
use alexandria as package
intermediate table for instance to document relation
permission/vis on meta 
"""


class CustomPermission(BasePermission):
    @permission_for(BaseModel)
    def has_permission_default(self, request):
        if request.user.role == "support":
            return True

        return False

    @permission_for(File)
    @permission_for(Document)
    def has_permission_for_document(self, request):
        # create document
        category = Category.objects.get(pk=request.data["category"]["id"])
        permission = category.meta["permissions"][request.user.role]

        return globals()[f"{permission}Permission"]().can_write(request)

    @object_permission_for(File)
    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, document):
        # update, delete document
        permission = document.category.meta["permissions"][request.user.role]

        if request.method == "DELETE":
            return globals()[f"{permission}Permission"]().can_destroy(request)

        return globals()[f"{permission}Permission"]().can_write(request)

    @permission_for(File)
    def has_permission_for_file(self, request):
        category = Document.objects.get(pk=request.data["document"]["id"]).category
        permission = category.meta["permissions"][request.user.role]

        return globals()[f"{permission}Permission"]().can_write(request)

    @object_permission_for(File)
    def has_object_permission_for_file(self, request, file):
        permission = file.document.category.meta["permissions"][request.user.role]

        if request.method == "DELETE":
            return globals()[f"{permission}Permission"]().can_destroy(request)

        return globals()[f"{permission}Permission"]().can_write(request)

    @permission_for(Tag)
    def has_permission_for_tag(self, request):
        if request.user.role != "applicant":
            return True

        return False

    @object_permission_for(Tag)
    def has_object_permission_for_tag(self, request, tag):
        if request.user.role == "support":
            return True

        if request.user.role != "applicant":
            return tag.created_by_group == request.user.group

        return False


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
