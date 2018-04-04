import django_excel
from django.conf import settings
from django_downloadview.api import PathDownloadView
from rest_framework import response, viewsets
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

    @detail_route(
        methods=['post'],
        serializer_class=serializers.InstanceSubmitSerializer
    )
    def submit(self, request, pk=None):
        instance = self.get_object()

        data = {
            'previous_instance_state': instance.instance_state.pk,
            'instance_state': models.InstanceState.objects.get(name='subm').pk
        }

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(data=serializer.data)


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
