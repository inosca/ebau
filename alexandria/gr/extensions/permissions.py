from alexandria.core.permissions import (
    BasePermission,
    permission_for,
    object_permission_for,
)
from alexandria.core.models import BaseModel, Document, File, Tag, Category

ADMIN_ROLE = "10000"
APPLICANT_ROLE = "10001"


class CustomPermission(BasePermission):
    @permission_for(BaseModel)
    def has_permission_default(self, request):
        if request.user.is_superuser:
            return True
        return False

    @permission_for(File)
    @permission_for(Document)
    def has_permission_for_document(self, request):
        """
        portal users can create for their own instance
        municipality users can create for their group's instance
        """
        print(request)
        return True

    @object_permission_for(File)
    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, instance):
        if request.user.is_superuser:
            return True
        elif (
            request.user.group_data["relationships"]["role"]["data"]["id"]
            == APPLICANT_ROLE
        ):
            if instance.created_by_user == request.user.username:
                return True

        if instance.created_by_group in request.user.groups:
            return True

        return False

    @permission_for(Tag)
    def has_permission_for_tag(self, request):
        """
        creating tags not allowed for portal users
        """
        self.has_permission_default(request)

    @object_permission_for(Tag)
    def has_object_permission_for_tag(self, request, instance):
        """
        portal users can add tags to their own document
        municipality users can add tags to their group's documents
        """
        if request.user.is_superuser:
            return True
        elif (
            request.user.group_data["relationships"]["role"]["data"]["id"]
            == APPLICANT_ROLE
        ):
            if instance.created_by_user == request.user.username:
                return True

        if instance.created_by_group in request.user.groups:
            return True

        return False
