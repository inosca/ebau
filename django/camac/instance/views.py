from rest_framework import viewsets
from rest_framework_json_api import views

from camac.core.models import Circulation
from camac.user.permissions import permission_aware

from . import models, serializers


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        return models.Form.objects.all()


class InstanceQuerysetMixin(views.ModelViewSet):
    instance_field = 'instance'

    def _get_instance_filter_expr(self, field, expr=None):
        """Get filter expression of field on given model."""
        result = field

        if self.instance_field:
            result = self.instance_field + '__' + result

        if expr:
            result = result + '__' + expr

        return result

    def get_queryset_for_applicant(self):
        queryset = super().get_queryset()
        user_field = self._get_instance_filter_expr('user')

        return queryset.filter(
            **{user_field: self.request.user}
        )

    def get_queryset_for_municipality(self):
        queryset = super().get_queryset()
        instance_field = self._get_instance_filter_expr('pk', 'in')

        instances = models.Instance.locations.through.objects.filter(
            location=self.request.group.locations.all()
        ).values('instance')

        # use subquery to avoid duplicates
        return queryset.filter(
            **{instance_field: instances}
        )

    def get_queryset_for_service(self):
        queryset = super().get_queryset()
        instance_field = self._get_instance_filter_expr('pk', 'in')

        instances = Circulation.objects.filter(
            activations__service=self.request.group.service
        ).values('instance')
        # use subquery to avoid duplicates
        return queryset.filter(
            **{instance_field: instances}
        )

    def get_queryset_for_canton(self):
        queryset = super().get_queryset()
        return queryset


class InstanceView(InstanceQuerysetMixin, views.ModelViewSet):
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


class FormFieldView(InstanceQuerysetMixin, views.ModelViewSet):
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
