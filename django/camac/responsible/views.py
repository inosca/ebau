from rest_framework_json_api.views import ModelViewSet

from camac.instance.mixins import InstanceEditableMixin
from camac.permissions.api import PermissionManager
from camac.permissions.switcher import permission_switching_method
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ResponsibleServiceView(InstanceEditableMixin, ModelViewSet):
    """
    View to handle responsible services.

    This view handles the model ResponsibleService which is used to capture
    a responsible user in the instance resource "Zuständigkeit".
    """

    serializer_class = serializers.ResponsibleServiceSerializer
    filterset_class = filters.ResponsibleServiceFilterSet
    queryset = models.ResponsibleService.objects.all()

    @permission_switching_method
    def has_create_permission(self):  # pragma: no cover
        return PermissionManager.from_request(self.request).has_all(
            self.request.data["instance"]["id"], "responsible-write"
        )

    @has_create_permission.register_old
    @permission_aware
    def has_create_permission_rbac(self):
        return False

    def has_create_permission_rbac_for_service(self):
        return True

    def has_create_permission_rbac_for_municipality(self):
        return True

    def has_create_permission_rbac_for_coordination(self):
        return True

    def has_create_permission_rbac_for_geometer(self):
        return True

    def has_create_permission_rbac_for_legal_authority(self):
        return True

    @permission_switching_method
    def has_update_permission(self):  # pragma: no cover
        return PermissionManager.from_request(self.request).has_all(
            self.request.data["instance"]["id"], "responsible-write"
        )

    @has_update_permission.register_old
    @permission_aware
    def has_update_permission_rbac(self):
        return False

    def has_update_permission_rbac_for_service(self):
        return True

    def has_update_permission_rbac_for_municipality(self):
        return True

    def has_update_permission_rbac_for_coordination(self):
        return True

    def has_update_permission_rbac_for_geometer(self):
        return True

    def has_update_permission_rbac_for_legal_authority(self):
        return True
