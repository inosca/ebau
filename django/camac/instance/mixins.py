from django.utils.translation import gettext as _
from rest_framework import exceptions

from camac.core.models import Circulation
from camac.request import get_request
from camac.user.permissions import permission_aware

from . import models


class InstanceQuerysetMixin(object):
    """
    Mixin to filter queryset by instances which may be read by given role.

    Define `instance_field` where instance is located on model.
    """

    instance_field = 'instance'

    def _get_instance_filter_expr(self, field, expr=None):
        """Get filter expression of field on given model."""
        result = field

        if self.instance_field:
            result = self.instance_field + '__' + result

        if expr:
            result = result + '__' + expr

        return result

    def get_base_queryset(self):
        """Get base query queryset for role specific filters.

        Per default `self.queryset` is used but may be overwritten.
        """
        return super().get_queryset()

    @permission_aware
    def get_queryset(self):
        queryset = self.get_base_queryset()
        user_field = self._get_instance_filter_expr('user')

        return queryset.filter(
            **{user_field: self.request.user}
        )

    def get_queryset_for_municipality(self):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr('pk', 'in')

        instances = models.Instance.objects.filter(
            location=self.request.group.locations.all()
        )
        return queryset.filter(
            **{instance_field: instances}
        )

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr('pk', 'in')

        instances = Circulation.objects.filter(
            activations__service=self.request.group.service
        ).values('instance')
        # use subquery to avoid duplicates
        return queryset.filter(
            **{instance_field: instances}
        )

    def get_queryset_for_canton(self):
        return self.get_base_queryset()


class InstanceValidationMixin(object):
    """Mixin to validate whether instance may be accessed by group role."""

    @permission_aware
    def validate_instance(self, instance):
        user = get_request(self).user
        if instance.user != user:
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_municipality(self, instance):
        group = get_request(self).group

        if not group.locations.filter(pk=instance.location_id).exists():
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_service(self, instance):
        service = get_request(self).group.service
        circulations = instance.circulations.all()
        if not circulations.filter(activations__service=service).exists():
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_canton(self, instance):
        return instance
