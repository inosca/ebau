from rest_framework.settings import api_settings
from rest_framework_json_api import views

from .. import filters, models
from ..mixins import bern as mixins
from ..serializers.bern import BernInstanceSerializer


class InstanceView(
    mixins.InstanceQuerysetMixin, mixins.InstanceEditableMixin, views.ModelViewSet
):
    instance_field = None
    """
    Instance field is actually model itself.
    """
    instance_editable_permission = "instance"

    serializer_class = BernInstanceSerializer
    filterset_class = filters.InstanceFilterSet
    queryset = models.Instance.objects.all()
    prefetch_for_includes = {"circulations": ["circulations__activations"]}
    ordering_fields = (
        "instance_id",
        "identifier",
        "instance_state__name",
        "instance_state__description",
        "form__description",
        "location__communal_federal_number",
        "creation_date",
    )
    search_fields = (
        "=identifier",
        "=location__name",
        "=circulations__activations__service__name",
        "@form__description",
        "fields__value",
    )
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.InstanceFormFieldFilterBackend
    ]
