import django_excel
from django.conf import settings
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.settings import api_settings
from rest_framework_json_api import views

from camac.core.models import WorkflowEntry
from camac.notification.serializers import NotificationTemplateSendmailSerializer

from .. import filters, models, serializers
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

    @action(methods=["get"], detail=False)
    def export(self, request):
        """Export filtered instances to given file format."""
        fields_queryset = models.FormField.objects.filter(instance=OuterRef("pk"))
        queryset = (
            self.get_queryset()
            .select_related("location", "user", "form", "instance_state")
            .annotate(
                applicants=Subquery(
                    fields_queryset.filter(name="projektverfasser-planer").values(
                        "value"
                    )[:1]
                )
            )
            .annotate(
                description=Subquery(
                    fields_queryset.filter(name="bezeichnung").values("value")[:1]
                )
            )
        )
        queryset = self.filter_queryset(queryset)

        content = [
            [
                instance.pk,
                instance.identifier,
                instance.form.description,
                instance.location and instance.location.name,
                ", ".join(
                    [applicant["name"] for applicant in (instance.applicants or [])]
                ),
                instance.description,
                instance.instance_state.name,
                instance.instance_state.description,
            ]
            for instance in queryset
        ]

        sheet = django_excel.pe.Sheet(content)
        return django_excel.make_response(
            sheet, file_type="xlsx", file_name="list.xlsx"
        )

    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.InstanceSubmitSerializer,
    )
    @transaction.atomic
    def submit(self, request, pk=None):
        instance = self.get_object()

        # change state of instance
        data = {
            "previous_instance_state": instance.instance_state.pk,
            "instance_state": models.InstanceState.objects.get(name="subm").pk,
        }

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # create workflow item when configured
        workflow_item = settings.APPLICATION["SUBMIT"].get("WORKFLOW_ITEM")
        if workflow_item:
            WorkflowEntry.objects.create(
                group=1,
                workflow_item_id=workflow_item,
                instance_id=pk,
                workflow_date=timezone.now(),
            )

        # send notification email when configured
        notification_template = settings.APPLICATION["SUBMIT"].get(
            "NOTIFICATION_TEMPLATE"
        )
        if notification_template:
            context = self.get_serializer_context()
            sendmail_data = {
                "recipient_types": ["municipality"],
                "notification_template": {
                    "type": "notification-templates",
                    "id": notification_template,
                },
                "instance": {"id": pk, "type": "instances"},
            }
            sendmail_serializer = NotificationTemplateSendmailSerializer(
                data=sendmail_data, context=context
            )
            sendmail_serializer.is_valid(raise_exception=True)
            sendmail_serializer.save()

        return response.Response(data=serializer.data)
