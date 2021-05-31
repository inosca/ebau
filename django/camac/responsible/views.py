from rest_framework_json_api.views import ModelViewSet

from camac.instance.mixins import InstanceEditableMixin
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ResponsibleServiceView(InstanceEditableMixin, ModelViewSet):
    """
    View to handle responsible services.

    This view handles the model ResponsibleService which is used to capture
    a responsible user in the instance resource "Zuständigkeit".
    """

    swagger_schema = None
    serializer_class = serializers.ResponsibleServiceSerializer
    filterset_class = filters.ResponsibleServiceFilterSet
    queryset = models.ResponsibleService.objects.all()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_service(self):
        return True

    def has_update_permission_for_municipality(self):
        return True
