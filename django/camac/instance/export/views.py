import django_excel
from django.conf import settings
from rest_framework.generics import ListAPIView

from camac.instance.export import filters, serializers
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance


class InstanceExportView(InstanceQuerysetMixin, ListAPIView):
    instance_field = None
    queryset = Instance.objects

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()

    def get_serializer_class(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return serializers.InstanceExportSerializerBE
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return serializers.InstanceExportSerializerSZ
        elif settings.APPLICATION_NAME == "kt_ag":
            return serializers.InstanceExportSerializerAG

        return serializers.InstanceExportSerializer  # pragma: no cover

    @property
    def filter_backends(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return [filters.InstanceExportFilterBackendBE]
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return [filters.InstanceExportFilterBackendSZ]
        elif settings.APPLICATION_NAME == "kt_ag":
            return [filters.InstanceExportFilterBackendAG]

        return [filters.InstanceExportFilterBackend]  # pragma: no cover

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        return django_excel.make_response(django_excel.pe.Sheet(data), file_type="xlsx")
