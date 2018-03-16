from rest_framework import viewsets
from rest_framework_json_api import views

from camac.core.models import Activation, Circulation
from camac.instance.mixins import InstanceQuerysetMixin

from . import serializers


class CirculationView(views.AutoPrefetchMixin,
                      views.PrefetchForIncludesHelperMixin,
                      InstanceQuerysetMixin,
                      viewsets.ReadOnlyModelViewSet):
    queryset = Circulation.objects.all()
    serializer_class = serializers.CirculationSerializer


class ActivationView(views.AutoPrefetchMixin,
                     views.PrefetchForIncludesHelperMixin,
                     InstanceQuerysetMixin,
                     viewsets.ReadOnlyModelViewSet):
    instance_field = 'circulation__instance'
    serializer_class = serializers.ActivationSerializer
    queryset = Activation.objects.all()

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.select_related('circulation_state')

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        return queryset.filter(service=self.request.group.service)
