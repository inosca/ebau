from rest_framework import viewsets
from rest_framework_json_api import views

from camac.user.permissions import permission_aware

from . import mixins, models, serializers


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        return models.Form.objects.all()


class InstanceView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    instance_field = None
    """
    Instance field is actually model itself.
    """

    serializer_class = serializers.InstanceSerializer
    queryset = models.Instance.objects.all()

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.none()

    def has_update_permission(self):
        """Disallow updating of instance.

        Updates happen through custom actions.'
        """
        return False

    def has_destroy_permission(self):
        """Disallow destroy of instances."""
        return False

    @permission_aware
    def has_create_permission(self):
        """Disallow creating of instances.

        Create is only allowed on certain roles.
        """
        return False

    def has_create_permission_for_applicant(self):
        return True


class FormFieldView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """
    Access form field of an instance.

    Rule is that only applicant may update it but whoever
    is allowed to read instance may read form data as well.
    """

    serializer_class = serializers.FormFieldSerializer
    queryset = models.FormField.objects.all()

    @permission_aware
    def get_queryset(self):
        return models.FormField.objects.none()

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_applicant(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_applicant(self):
        return True

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_applicant(self):
        return True
