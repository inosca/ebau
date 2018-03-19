import django_excel
from django.conf import settings
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from django_downloadview.api import PathDownloadView
from rest_framework import exceptions, response, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework_json_api import views

from . import filters, mixins, models, serializers


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        return models.Form.objects.all()


class FormConfigDownloadView(PathDownloadView, APIView):
    attachment = False
    path = settings.APPLICATION_DIR('form.json')


class InstanceStateView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.InstanceStateSerializer
    ordering = ('sort', 'name')

    def get_queryset(self):
        return models.InstanceState.objects.all()


class InstanceView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    instance_field = None
    """
    Instance field is actually model itself.
    """

    serializer_class = serializers.InstanceSerializer
    filter_class = filters.InstanceFilterSet
    queryset = models.Instance.objects.all()
    ordering_fields = [
        'instance_id',
        'identifier',
        'instance_state__name'
    ]

    def has_object_update_permission(self, instance):
        return (
            instance.instance_state.name == 'new' and
            instance.user == self.request.user
        )

    def has_destroy_permission(self):
        """Disallow destroy of instances."""
        return False

    def has_object_submit_permission(self, instance):
        return instance.user == self.request.user

    def validate_submit(self, instance):
        # TODO: validate form data

        if instance.location is None:
            raise exceptions.ValidationError(_('No location assigned.'))

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
            ).aggregate(max_identifier=Max(
                'identifier'))['max_identifier'] or '00-00-000'
            sequence = int(max_identifier[-3:])

            instance.identifier = '{0}-{1}-{2}'.format(
                location_nr,
                timezone.now().strftime('%y'),
                str(sequence + 1).zfill(3))

    @list_route(methods=['get'])
    def export(self, request):
        """Export filtered instances to given file format."""
        queryset = self.get_queryset().select_related(
            'location', 'user', 'form', 'instance_state'
        )
        queryset = self.filter_queryset(queryset)

        # TODO: verify columns once form data is clear
        content = [
            [
                instance.pk,
                instance.identifier,
                instance.form.description,
                instance.location and instance.location.name,
                instance.user.get_full_name(),
                instance.instance_state.name,
                instance.instance_state.description,
            ]
            for instance in queryset
        ]

        sheet = django_excel.pe.Sheet(content)
        return django_excel.make_response(
            sheet, file_type='xlsx', file_name='list.xlsx'
        )

    @detail_route(methods=['post'])
    def submit(self, request, pk=None):
        instance = self.get_object()

        self.validate_submit(instance)

        self.generate_identifier(instance)
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = models.InstanceState.objects.get(name='comm')
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

    def has_object_update_permission(self, form_field):
        instance = form_field.instance
        return (
            instance.instance_state.name == 'new' and
            instance.user == self.request.user
        )

    def has_object_destroy_permission(self, form_field):
        return self.has_object_update_permission(form_field)
