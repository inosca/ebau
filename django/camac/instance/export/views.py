import django_excel
from django.conf import settings
from rest_framework.generics import ListAPIView

from camac.instance.export.filters import (
    InstanceExportFilterBackend,
    InstanceExportFilterBackendBE,
    InstanceExportFilterBackendSZ,
)
from camac.instance.export.serializers import (
    InstanceExportSerializer,
    InstanceExportSerializerBE,
    InstanceExportSerializerSZ,
)
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance


class InstanceExportView(ListAPIView, InstanceQuerysetMixin):
    instance_field = None
    queryset = Instance.objects

    def get_serializer_class(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return InstanceExportSerializerBE
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return InstanceExportSerializerSZ

        return InstanceExportSerializer

    @property
    def filter_backends(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return [InstanceExportFilterBackendBE]
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return [InstanceExportFilterBackendSZ]

        return [InstanceExportFilterBackend]

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        return django_excel.make_response(django_excel.pe.Sheet(data), file_type="xlsx")
