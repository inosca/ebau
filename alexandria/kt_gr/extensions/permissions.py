from alexandria.core.permissions import (
    BasePermission,
    permission_for,
    object_permission_for,
)
from alexandria.core.models import BaseModel, Document, File, Tag


class CustomPermission(BasePermission):
    @permission_for(BaseModel)
    def has_permission_default(self, request):
        return True

    @permission_for(File)
    @permission_for(Document)
    def has_permission_for_document(self, request):
        return True

    @object_permission_for(File)
    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, instance):
        return True

    @permission_for(Tag)
    def has_permission_for_tag(self, request):
        return True

    @object_permission_for(Tag)
    def has_object_permission_for_tag(self, request, instance):
        return True
