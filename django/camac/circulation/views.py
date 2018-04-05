import django_excel
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework_json_api import views

from camac.core.models import Activation, Circulation
from camac.instance.mixins import InstanceQuerysetMixin

from . import filters, serializers


class CirculationView(views.AutoPrefetchMixin,
                      views.PrefetchForIncludesHelperMixin,
                      InstanceQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Circulation.objects.all()
    serializer_class = serializers.CirculationSerializer
    filter_class = filters.CirculationFilterSet


class ActivationView(views.AutoPrefetchMixin,
                     views.PrefetchForIncludesHelperMixin,
                     InstanceQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    instance_field = 'circulation.instance'
    serializer_class = serializers.ActivationSerializer
    queryset = Activation.objects.all()
    filter_class = filters.ActivationFilterSet

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.select_related('circulation_state')

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        return queryset.filter(service=self.request.group.service)

    @list_route(methods=['get'])
    def export(self, request):
        """Export filtered activations to given file format."""
        queryset = self.get_queryset().select_related(
            'circulation__instance__location', 'circulation__instance__user',
            'circulation__instance__form',
            'circulation__instance__instance_state')
        queryset = self.filter_queryset(queryset)

        # TODO: verify columns once form data is clear
        content = [
            [
                activation.circulation.instance.pk,
                activation.circulation.instance.identifier,
                activation.circulation.instance.form.description,
                (
                    activation.circulation.instance.location and
                    activation.circulation.instance.location.name
                ),
                activation.circulation.instance.instance_state.name,
                activation.circulation.instance.instance_state.description,
                activation.circulation_state.name,
                activation.reason,
                activation.deadline_date,
            ]
            for activation in queryset
        ]

        sheet = django_excel.pe.Sheet(content)
        return django_excel.make_response(
            sheet, file_type='xlsx', file_name='list.xlsx')
