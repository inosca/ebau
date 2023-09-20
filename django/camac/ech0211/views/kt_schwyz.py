import logging

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from ...constants.kt_bern import ECH_BASE_DELIVERY
from ...constants.kt_schwyz import FORM_DESCRIPTIONS
from ...instance.models import Instance
from ...swagger.utils import get_operation_description, group_param
from .. import formatters
from ..mixins import ECHInstanceQuerysetMixin
from ..serializers import ApplicationsSerializer

logger = logging.getLogger(__name__)


class ApplicationView(ECHInstanceQuerysetMixin, RetrieveModelMixin, GenericViewSet):
    instance_field = None
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    queryset = Instance.objects.filter(form__description__in=FORM_DESCRIPTIONS)
    instance_field = None

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param],
        operation_summary="Get baseDelivery for instance",
        operation_description=get_operation_description(),
        responses={"200": "eCH-0211 baseDelivery"},
    )
    def retrieve(self, request, instance_id=None, **kwargs):
        qs = self.get_queryset()
        instance = get_object_or_404(qs, pk=instance_id)
        base_delivery_formatter = formatters.BaseDeliveryFormatter("kt_schwyz")
        try:
            xml_data = formatters.delivery(
                instance,
                answers={"ech-subject": instance.form.get_name()},
                message_type=ECH_BASE_DELIVERY,
                eventBaseDelivery=base_delivery_formatter.format_base_delivery(
                    instance
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise
        response = HttpResponse(xml_data)
        response["Content-Type"] = "application/xml"
        return response


class ApplicationsView(ECHInstanceQuerysetMixin, ListModelMixin, GenericViewSet):
    instance_field = None
    serializer_class = ApplicationsSerializer
    queryset = Instance.objects
    instance_field = None
    filter_backends = []

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param],
        operation_summary="Get list of accessible instances",
        operation_description=get_operation_description(),
    )
    def list(self, request, *args, **kwargs):  # pragma: no cover
        return super().list(request, *args, **kwargs)
