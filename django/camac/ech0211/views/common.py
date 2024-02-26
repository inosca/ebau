from django.core.exceptions import ValidationError
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from camac.ech0211.models import Message
from camac.ech0211.throttling import ECHMessageThrottle
from camac.ech0211.views.kt_bern import last_param
from camac.swagger.utils import get_operation_description, group_param


class MessageView(RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)

    throttle_classes = [ECHMessageThrottle]
    include_in_swagger = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(receiver=self.request.group.service)

    def get_object(self, last=None):
        queryset = self.get_queryset()
        next_message = queryset.first()
        if last:
            try:
                last_message = queryset.get(pk=last)
            except ValidationError:
                raise ParseError("'last' parameter must be a valid UUID")
            except Message.DoesNotExist:
                return

            next_message = queryset.filter(
                created_at__gt=last_message.created_at
            ).first()

        return next_message

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param, last_param],
        operation_summary="Get message",
        operation_description=get_operation_description(),
        responses={"200": "eCH-0211 message"},
    )
    def retrieve(self, request, *args, **kwargs):
        message = self.get_object(request.query_params.get("last"))
        if not message:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        response = HttpResponse(message.body)
        response["Content-Type"] = "application/xml"
        return response
