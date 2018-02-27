from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions, response, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework_json_api import views

from camac.user.permissions import permission_aware

from . import filters, mixins, models, serializers


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
    filter_class = filters.InstanceFilterSet
    queryset = models.Instance.objects.all()

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.none()

    @permission_aware
    def has_object_update_permission(self, instance):
        return False

    def has_object_update_permission_for_applicant(self, instance):
        return instance.instance_state.name == 'new'

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

    @permission_aware
    def has_submit_permission(self):
        return False

    def has_submit_permission_for_applicant(self):
        return True

    def validate_submit(self, instance):
        # TODO: validate form data and protect it when not new

        if instance.location is None:
            raise exceptions.ValidationError(
                _('No location assigned.')
            )

    def generate_identifier(self, instance):
        """
        Build identifier for instance.

        Format:
        two last digits of communal location number
        year in two digits
        unique sequence

        Example: 11-18-001
        """
        if not instance.identifier:
            location_nr = instance.location.communal_federal_number[-2:]
            year = timezone.now().strftime('%y')

            max_identifier = models.Instance.objects.filter(
                identifier__startswith='{0}-{1}-'.format(location_nr, year)
            ).aggregate(
                max_identifier=Max('identifier')
            )['max_identifier'] or '00-00-000'
            sequence = int(max_identifier[-3:])

            instance.identifier = '{0}-{1}-{2}'.format(
                location_nr,
                timezone.now().strftime('%y'),
                str(sequence + 1).zfill(3)
            )

    @detail_route(methods=['post'])
    def submit(self, request, pk=None):
        instance = self.get_object()

        self.validate_submit(instance)

        self.generate_identifier(instance)
        instance.previous_instance_state = instance.instance_state
        instance.instante_state = models.InstanceState.objects.get(name='comm')
        instance.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FormFieldView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """
    Access form field of an instance.

    Rule is that only applicant may update it but whoever
    is allowed to read instance may read form data as well.
    """

    serializer_class = serializers.FormFieldSerializer
    filter_class = filters.FormFieldFilterSet
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
