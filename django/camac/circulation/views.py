import django_excel
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models import OuterRef, Subquery
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_json_api import views

from camac.caluma.api import CalumaApi
from camac.core.models import Activation, Circulation, CirculationState
from camac.instance.filters import FormFieldOrdering
from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.models import FormField
from camac.notification.utils import send_mail

from . import filters, serializers


class CirculationView(InstanceQuerysetMixin, InstanceEditableMixin, views.ModelViewSet):
    swagger_schema = None
    queryset = Circulation.objects.select_related("instance")
    serializer_class = serializers.CirculationSerializer
    filterset_class = filters.CirculationFilterSet
    http_method_names = ["get", "patch", "delete"]
    prefetch_for_includes = {
        "activations": [
            "activations__circulation",
            "activations__circulation_state",
            "instance__circulations",
        ]
    }

    def has_base_object_permission(self, instance):
        return self.has_editable_permission(self.get_instance(instance))

    def has_object_destroy_permission(self, instance):
        return (
            self.has_base_object_permission(instance)
            and instance.service == self.request.group.service
            and not instance.activations.count()
        )

    def has_object_update_permission(self, instance):
        return False

    def has_object_sync_permission(self, instance):
        return self.has_base_object_permission(instance)

    def has_object_end_permission(self, instance):
        return (
            self.has_base_object_permission(instance)
            and instance.service == self.request.group.service
        )

    @transaction.atomic
    def perform_destroy(self, circulation):
        work_item = WorkItem.objects.filter(
            **{"meta__circulation-id": circulation.pk}
        ).first()

        # delete circulation
        super().perform_destroy(circulation)

        if work_item:
            # skip work item to continue the workflow
            skip_work_item(
                work_item=work_item,
                user=self.request.caluma_info.context.user,
                context={"no-history": True},
            )

            # remove obsolete work item
            work_item.delete()

    @action(methods=["PATCH"], detail=True)
    @transaction.atomic
    def sync(self, request, pk=None):
        CalumaApi().sync_circulation(
            self.get_object(), request.caluma_info.context.user
        )

        return Response([], 204)

    @action(methods=["PATCH"], detail=True)
    @transaction.atomic
    def end(self, request, pk=None):
        circulation = self.get_object()

        # skip ready circulation work item
        work_item = WorkItem.objects.filter(
            **{"meta__circulation-id": circulation.pk, "status": WorkItem.STATUS_READY}
        ).first()
        if work_item:
            skip_work_item(
                work_item=work_item, user=self.request.caluma_info.context.user
            )

        # send notifications
        notification_config = settings.APPLICATION["NOTIFICATIONS"].get(
            "END_CIRCULATION", []
        )
        for config in notification_config:
            send_mail(
                config["template_slug"],
                self.get_serializer_context(),
                recipient_types=config["recipient_types"],
                instance={"type": "instances", "id": circulation.instance.pk},
                circulation={"type": "circulations", "id": circulation.pk},
            )

        # set state of all activations to done
        circulation.activations.update(
            circulation_state=CirculationState.objects.get(name="DONE")
        )

        return Response([], 204)


class ActivationView(InstanceQuerysetMixin, views.ReadOnlyModelViewSet):
    swagger_schema = None
    instance_field = "circulation.instance"
    serializer_class = serializers.ActivationSerializer
    queryset = Activation.objects.select_related("circulation")
    filterset_class = filters.ActivationFilterSet
    prefetch_for_includes = {"circulation": ["circulation__activations"]}
    ordering_fields = (
        "circulation__instance__identifier",
        "circulation__instance__form__description",
        "circulation__instance__location__name",
        "circulation__instance__instance_state__name",
        "circulation__instance__instance_state__description",
        "reason",
        "deadline_date",
        "circulation_state__name",
    )
    search_fields = (
        "=circulation__instance__identifier",
        "=circulation__instance__location__name",
        "@service__name",
        "@circulation__instance__form__description",
        "circulation__instance__fields__value",
    )
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [FormFieldOrdering]

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.select_related("circulation_state")

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        return queryset.filter(service=self.request.group.service)

    @action(methods=["get"], detail=False)
    def export(self, request):
        """Export filtered activations to given file format."""
        resource_instance_state_ids = [
            val.strip() for val in request.query_params["instance-state-ids"].split(",")
        ]

        fields_queryset = FormField.objects.filter(
            instance=OuterRef("circulation__instance")
        )
        queryset = (
            self.get_queryset()
            .select_related(
                "circulation__instance__location",
                "circulation__instance__user",
                "circulation__instance__form",
                "circulation__instance__instance_state",
            )
            .annotate(
                applicants=Subquery(
                    fields_queryset.filter(
                        name__in=[
                            "projektverfasser-planer",
                            "projektverfasser-planer-v2",
                        ]
                    ).values("value")
                )
            )
            .annotate(
                description=Subquery(
                    fields_queryset.filter(name="bezeichnung").values("value")[:1]
                )
            )
        ).filter(circulation__instance__instance_state__in=resource_instance_state_ids)

        queryset = self.filter_queryset(queryset)

        def applicant_names(activation):
            overrides = FormField.objects.filter(
                instance=activation.circulation.instance,
                name="projektverfasser-planer-override",
            ).values("value")

            applicants = overrides if len(overrides) else (activation.applicants or [])

            return ", ".join(
                [
                    f"{applicant.get('firma', '')} {applicant.get('vorname', '')} {applicant.get('name', '')}".strip()
                    for applicant in applicants
                ]
            )

        content = [
            [
                activation.circulation.instance.pk,
                activation.circulation.instance.identifier,
                activation.circulation.instance.form.description,
                (
                    activation.circulation.instance.location
                    and activation.circulation.instance.location.name
                ),
                applicant_names(activation),
                activation.description,
                activation.reason,
                activation.circulation.instance.instance_state.name,
                activation.circulation.instance.instance_state.description,
                activation.deadline_date.strftime("%d.%m.%Y"),
                activation.circulation_state.name,
            ]
            for activation in queryset
        ]

        sheet = django_excel.pe.Sheet(content)
        return django_excel.make_response(
            sheet, file_type="xlsx", file_name="list.xlsx"
        )
