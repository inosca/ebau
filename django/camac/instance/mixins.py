from camac.core.models import Circulation

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

    def get_queryset_for_applicant(self):
        queryset = self.get_base_queryset()
        user_field = self._get_instance_filter_expr('user')

        return queryset.filter(
            **{user_field: self.request.user}
        )

    def get_queryset_for_municipality(self):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr('pk', 'in')

        instances = models.Instance.locations.through.objects.filter(
            location=self.request.group.locations.all()
        ).values('instance')

        # use subquery to avoid duplicates
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
