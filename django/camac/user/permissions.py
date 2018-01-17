from rest_framework import permissions


class IsGroupMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.group)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
