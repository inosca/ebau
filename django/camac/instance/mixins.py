from django.db.models.constants import LOOKUP_SEP
from django.utils.translation import gettext as _
from rest_framework import exceptions

from camac.attrs import nested_getattr
from camac.core.models import Circulation
from camac.mixins import AttributeMixin
from camac.request import get_request
from camac.user.permissions import permission_aware

from . import models


class InstanceQuerysetMixin(object):
    """
    Mixin to filter queryset by instances which may be read by given role.

    Define `instance_field` where instance is located on model (dot annotation)
    """

    instance_field = 'instance'

    def _get_instance_filter_expr(self, field, expr=None):
        """Get filter expression of field on given model."""
        result = field

        if self.instance_field:
            instance_field = self.instance_field.replace('.', LOOKUP_SEP)
            result = instance_field + LOOKUP_SEP + result

        if expr:
            result = result + LOOKUP_SEP + expr

        return result

    def get_base_queryset(self):
        """Get base query queryset for role specific filters.

        Per default `self.queryset` is used but may be overwritten.
        """
        # instance state is always used to determine permissions
        instance_state_expr = self._get_instance_filter_expr('instance_state')
        return super().get_queryset().select_related(instance_state_expr)

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
            location__in=self.request.group.locations.all()
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


class InstanceEditableMixin(AttributeMixin):
    """Mixin to determine whether action is allowed on given instance.

    Define `instance_editable_permission` what permission is needed to edit.
    Currently there are `document` for attachments and `form` for form data.
    """

    def get_instance(self, obj):
        instance = obj
        instance_field = self.serializer_getattr('instance_field')
        if instance_field:
            instance = nested_getattr(obj, self.instance_field)

        return instance

    def has_editable_permission(self, instance):
        editable_permission = self.serializer_getattr(
            'instance_editable_permission'
        )
        return editable_permission in self.get_editable(instance)

    @permission_aware
    def get_editable(self, instance):
        editable = set()

        if instance.instance_state.name == 'new':
            editable.update(['form', 'document', 'notification'])

        if instance.instance_state.name == 'nfd':
            editable.update(['document', 'notification'])

        if instance.instance_state.name == 'subm':
            editable.add('notification')

        return editable

    def get_editable_for_service(self, instance):
        return {'document', 'notification'}

    def get_editable_for_municipality(self, instance):
        return {'document', 'notification'}

    def get_editable_for_canton(self, instance):
        return {'document', 'notification'}

    def has_object_update_permission(self, obj):
        instance = self.get_instance(obj)
        return self.has_editable_permission(instance)

    def has_object_destroy_permission(self, obj):
        return self.has_object_update_permission(obj)

    def _validate_instance_editablity(self, instance,
                                      is_editable_callable=lambda: True):
        if (
            not self.has_editable_permission(instance) or
            not is_editable_callable()
        ):
            raise exceptions.ValidationError(
                _('Not allowed to add data to instance %(instance)s') % {
                    'instance': instance.pk
                }
            )

        return instance

    @permission_aware
    def validate_instance(self, instance):
        user = get_request(self).user
        return self._validate_instance_editablity(
            instance, lambda: instance.user == user
        )

    def validate_instance_for_municipality(self, instance):
        group = get_request(self).group
        return self._validate_instance_editablity(
            instance,
            lambda: group.locations.filter(pk=instance.location_id).exists()
        )

    def validate_instance_for_service(self, instance):
        service = get_request(self).group.service
        circulations = instance.circulations.all()

        return self._validate_instance_editablity(
            instance,
            lambda: circulations.filter(activations__service=service).exists()
        )

    def validate_instance_for_canton(self, instance):
        return self._validate_instance_editablity(instance)
