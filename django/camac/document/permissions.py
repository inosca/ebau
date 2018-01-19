from rest_framework import permissions

from . import models


class AttachmentPermissions(permissions.BasePermission):
    """
    Determines whether set group has permissions to perform action.

    This class only restricts `DELETE` whereas other methods
    are directly handled by attachment view or serializer.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True

        mode = obj.attachment_section.get_mode(request.group)
        return mode == models.ADMIN_PERMISSION
