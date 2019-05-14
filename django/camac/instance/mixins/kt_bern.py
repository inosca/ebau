from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from camac.attrs import nested_getattr
from camac.core.models import Circulation, InstanceService
from camac.mixins import AttributeMixin
from camac.user.permissions import permission_aware


class InstanceQuerysetMixin(object):  # pragma: no cover
    # TODO: One day, we should do exhaustive testing of this ACL stuff
    """
    Mixin to filter queryset by instances which may be read by given role.

    Define `instance_field` where instance is located on model (dot annotation)
    """

    instance_field = "instance"

    def _get_instance_filter_expr(self, field, expr=None):
        """Get filter expression of field on given model."""
        result = field

        if self.instance_field:
            instance_field = self.instance_field.replace(".", LOOKUP_SEP)
            result = instance_field + LOOKUP_SEP + result

        if expr:
            result = result + LOOKUP_SEP + expr

        return result

    def get_base_queryset(self):
        """Get base query queryset for role specific filters.

        Per default `self.queryset` is used but may be overwritten.
        """
        # instance state is always used to determine permissions
        instance_state_expr = self._get_instance_filter_expr("instance_state")
        return super().get_queryset().select_related(instance_state_expr)

    @permission_aware
    def get_queryset(self):
        queryset = self.get_base_queryset()
        user_field = self._get_instance_filter_expr("user")
        return queryset.filter(**{user_field: self.request.user})

    def get_queryset_for_municipality(self):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")
        return queryset.filter(
            Q(**{instance_field: self._instances_with_activation()})
            | Q(**{instance_field: self._instances_involved_in()})
        )

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        instance_field = self._get_instance_filter_expr("pk", "in")
        return queryset.filter(**{instance_field: self._instances_with_activation()})

    def get_queryset_for_support(self):
        return self.get_base_queryset()

    def get_queryset_for_applicant(self):
        queryset = self.get_base_queryset()
        # An applicant needs to be invited on the instance to access it
        return queryset.filter(involved_applicants__user=self.request.user)

    def _instances_with_activation(self):
        return Circulation.objects.filter(
            activations__service=self.request.group.service
        ).values("instance")

    def _instances_involved_in(self):
        return InstanceService.objects.filter(
            service=self.request.group.service
        ).values("instance")


class InstanceEditableMixin(AttributeMixin):  # pragma: no cover
    # TODO: One day, we should do exhaustive testing of this ACL stuff
    """Mixin to determine whether action is allowed on given instance.

    Define `instance_editable_permission` what permission is needed to edit.
    Currently there are `document` for attachments and `form` for form data.
    Set it to None if no specific permission is required.
    """

    def get_instance(self, obj):
        instance = obj
        instance_field = self.serializer_getattr("instance_field")
        if instance_field:
            instance = nested_getattr(obj, self.instance_field)

        return instance

    def has_editable_permission(self, instance):
        editable_permission = self.serializer_getattr("instance_editable_permission")
        return editable_permission is None or editable_permission in self.get_editable(
            instance
        )

    @permission_aware
    def get_editable(self, instance):
        return set()

    def get_editable_for_municipality(self, instance):
        return {"form", "document"}

    def get_editable_for_service(self, instance):
        return {"form", "document"}

    def get_editable_for_support(self, instance):
        return {"form", "document"}

    def get_editable_for_applicant(self, instance):
        if instance.instance_state.name == "Neu":
            return {"instance", "form", "document"}
        else:
            return {"document"}

    def has_object_update_permission(self, obj):
        instance = self.get_instance(obj)
        return self.has_editable_permission(instance)

    def has_object_destroy_permission(self, obj):
        return self.has_object_update_permission(obj)
