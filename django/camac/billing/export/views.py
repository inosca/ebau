import django_excel as excel
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import ListAPIView
from rest_framework.renderers import BaseRenderer
from rest_framework.settings import api_settings
from rest_framework_json_api import renderers as jsonapi_renderers

from camac.billing.filters import (
    BillingV2EntryExportFilterBackend,
    BillingV2EntryFilterSet,
)
from camac.billing.models import BillingV2Entry
from camac.billing.serializers import BillingV2EntryExportSerializer
from camac.instance.mixins import InstanceQuerysetMixin


class XLSXRenderer(jsonapi_renderers.JSONRenderer, BaseRenderer):
    """
    Excel output renderer for the REST framework.

    This formats the data into an Excel table (instead of JSON for example) as part
    of the regular REST framework infrastructure.

    Use this by setting `renderer_classes = [XLSXRenderer]` in your view class.
    """

    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    format = "xlsx"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context["view"]
        serializer = view.get_serializer()
        fields = serializer.get_fields()
        columns = list(fields)

        is_error = False
        try:
            is_error = (
                isinstance(data[0]["detail"], ErrorDetail) if len(data) else False
            )
        except KeyError:
            pass

        if is_error:
            return super().render(data)

        header = [field.label or name for name, field in fields.items()]

        rows = [[row[col] for col in columns] for row in data]

        sheet = excel.pe.Sheet([header] + rows)

        return excel.make_response(sheet, file_type="xlsx", file_name="list.xlsx")


class BillingV2EntryExportView(InstanceQuerysetMixin, ListAPIView):
    queryset = BillingV2Entry.objects
    serializer_class = BillingV2EntryExportSerializer
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        BillingV2EntryExportFilterBackend,
    ]
    filterset_class = BillingV2EntryFilterSet
    renderer_classes = [XLSXRenderer]

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()
