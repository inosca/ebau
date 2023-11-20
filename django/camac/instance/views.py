import mimetypes
from datetime import timedelta

import django_excel
from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models import CharField, F, OuterRef, Q, Subquery, Value
from django.db.models.expressions import Func
from django.db.models.fields import IntegerField
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings
from rest_framework_json_api import views
from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.caluma.api import CalumaApi
from camac.constants import kt_uri as ur_constants
from camac.core.models import InstanceService, PublicationEntry, WorkflowEntry
from camac.core.views import SendfileHttpResponse
from camac.document.models import Attachment, AttachmentSection
from camac.instance.domain_logic import RejectionLogic
from camac.instance.utils import build_document_prefetch_statements
from camac.notification.utils import send_mail
from camac.swagger.utils import get_operation_description, group_param
from camac.user.permissions import (
    DefaultPermission,
    IsApplication,
    PublicationPermission,
    permission_aware,
)
from camac.utils import DocxRenderer

from ..utils import get_paper_settings
from . import (
    document_merge_service,
    filters,
    gwr_lookups,
    mixins,
    models,
    serializers,
    validators,
)
from .domain_logic import link_instances
from .placeholders.serializers import (
    BeDMSPlaceholdersSerializer,
    DMSPlaceholdersSerializer,
    GrDMSPlaceholdersSerializer,
)


class InstanceStateView(ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.InstanceStateSerializer
    filterset_class = filters.InstanceStateFilterSet
    ordering = ("sort", "name")

    def get_queryset(self):
        return models.InstanceState.objects.prefetch_related("trans").all()


class FormView(ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.FormSerializer
    filterset_class = filters.FormFilterSet

    @permission_aware
    def get_queryset(self):
        return models.Form.objects.filter(form_state__name="Published")

    def get_queryset_for_municipality(self):
        return models.Form.objects.all()


class FormConfigDownloadView(RetrieveAPIView):
    swagger_schema = None
    path = settings.APPLICATION_DIR("form.json")
    permission_classes = [DefaultPermission | PublicationPermission]

    def retrieve(self, request, **kwargs):
        with open(self.path) as json_file:
            response = HttpResponse(json_file, content_type="application/json")
            return response


class InstanceView(
    mixins.InstanceQuerysetMixin, mixins.InstanceEditableMixin, views.ModelViewSet
):
    instance_field = None
    """
    Instance field is actually model itself.
    """
    instance_editable_permission = "instance"

    queryset = models.Instance.objects.select_related("group__service")
    prefetch_for_includes = {
        "circulations": ["circulations__activations"],
        "active_service": ["services"],
        "responsible_service_users": [
            "responsible_services",
            "responsible_services__responsible_user",
        ],
        "location": ["location"],
        "involved_services": ["services"],
        "circulation_initializer_services": [
            "circulations",
        ],
    }
    ordering_fields = (
        "instance_id",
        "identifier",
        "instance_state__name",
        "instance_state__description",
        "form__description",
        "location__communal_federal_number",
        "location__name",
        "creation_date",
    )
    search_fields = (
        "=identifier",
        "=location__name",
        "=circulations__activations__service__name",
        "@form__description",
        "fields__value",
        "instance_state__description",
    )

    if settings.APPLICATION_NAME == "kt_schwyz":  # pragma: no cover
        swagger_schema = None

    @property
    def filter_backends(self):
        filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            filter_backends = filter_backends + [
                filters.InstanceFormFieldFilterBackend,
                filters.FormFieldOrdering,
            ]

        return filter_backends

    @property
    def filterset_class(self):
        if settings.APPLICATION["FORM_BACKEND"] == "caluma":
            return filters.CalumaInstanceFilterSet

        return filters.InstanceFilterSet

    def get_serializer_class(self):
        backend = settings.APPLICATION["FORM_BACKEND"]

        SERIALIZER_CLASS = {
            "caluma": {
                "submit": serializers.CalumaInstanceSubmitSerializer,
                "report": serializers.CalumaInstanceReportSerializer,
                "finalize": serializers.CalumaInstanceFinalizeSerializer,
                "change_responsible_service": serializers.CalumaInstanceChangeResponsibleServiceSerializer,
                "set_ebau_number": serializers.CalumaInstanceSetEbauNumberSerializer,
                "archive": serializers.CalumaInstanceArchiveSerializer,
                "change_form": serializers.CalumaInstanceChangeFormSerializer,
                "fix_work_items": serializers.CalumaInstanceFixWorkItemsSerializer,
                "convert_modification": serializers.CalumaInstanceConvertModificationSerializer,
                "dms_placeholders": {
                    "kt_bern": BeDMSPlaceholdersSerializer,
                    "kt_gr": GrDMSPlaceholdersSerializer,
                    "default": DMSPlaceholdersSerializer,
                },
                "appeal": serializers.CalumaInstanceAppealSerializer,
                "default": serializers.CalumaInstanceSerializer,
                "correction": serializers.CalumaInstanceCorrectionSerializer,
                "rejection": serializers.CalumaInstanceRejectionSerializer,
            },
            "camac-ng": {
                "submit": serializers.InstanceSubmitSerializer,
                "default": serializers.SchwyzInstanceSerializer,
                "change_form": serializers.CamacInstanceChangeFormSerializer,
            },
        }

        serializer_config = SERIALIZER_CLASS[backend].get(
            self.action, SERIALIZER_CLASS[backend]["default"]
        )
        if type(serializer_config) == dict:
            return serializer_config.get(settings.APPLICATION_NAME, "default")

        return serializer_config

    @permission_aware
    def has_base_permission(self, instance):
        return instance.involved_applicants.filter(invitee=self.request.user).exists()

    def has_base_permission_for_municipality(self, instance):
        state = instance.instance_state.name
        group = self.request.group

        return (
            CalumaApi().is_paper(instance)
            and group.service.service_group.pk
            in get_paper_settings(state)["ALLOWED_SERVICE_GROUPS"]
            and group.role.pk in get_paper_settings(state)["ALLOWED_ROLES"]
            and InstanceService.objects.filter(
                active=1, instance=instance, service=group.service
            ).exists()
        )

    def has_base_permission_for_coordination(self, instance):
        return self.has_base_permission_for_municipality(instance)

    def has_object_destroy_permission(self, instance):
        deletable_states = ["new"]
        if settings.APPLICATION["CALUMA"].get("CREATE_IN_PROCESS", False):
            deletable_states.append("comm")

        return (
            self.has_base_permission(instance)
            and instance.instance_state.name in deletable_states
            and instance.previous_instance_state.name in deletable_states
        )

    def has_object_submit_permission(self, instance):
        return self.has_base_permission(instance) and instance.instance_state.name in (
            "new",
            # kt. uri
            "old",
            # kt. schwyz
            "nfd",
            "rejected",
        )

    def has_object_report_permission(self, instance):
        return (
            self.has_base_permission(instance) and instance.instance_state.name == "sb1"
        )

    def has_object_finalize_permission(self, instance):
        return (
            self.has_base_permission(instance) and instance.instance_state.name == "sb2"
        )

    def has_object_change_responsible_service_permission(self, instance):
        return instance.instance_services.filter(
            active=1, service=self.request.group.service
        ).exists()

    @permission_aware
    def has_object_set_ebau_number_permission(self, instance):
        return False

    def has_object_set_ebau_number_permission_for_municipality(self, instance):
        return (
            instance.responsible_service(filter_type="municipality")
            == self.request.group.service
        )

    def has_object_set_ebau_number_permission_for_support(self, instance):
        return True

    @permission_aware
    def has_object_archive_permission(self, instance):
        return False

    def has_object_archive_permission_for_municipality(self, instance):
        return (
            instance.responsible_service(filter_type="municipality")
            == self.request.group.service
        )

    def has_object_archive_permission_for_support(self, instance):
        return True

    @permission_aware
    def has_object_change_form_permission(self, instance):
        return False

    def has_object_change_form_permission_for_municipality(self, instance):
        is_responsible_service = (
            instance.responsible_service(filter_type="municipality")
            == self.request.group.service
        )
        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            return is_responsible_service and instance.instance_state.name == "subm"

        return is_responsible_service

    def has_object_change_form_permission_for_support(self, instance):
        return True

    @permission_aware
    def has_object_fix_work_items_permission(self, instance):
        return False

    def has_object_fix_work_items_permission_for_support(self, instance):
        return True

    @permission_aware
    def has_object_link_permission(self, instance):
        return False

    def has_object_link_permission_for_municipality(self, instance):
        return True

    def has_object_link_permission_for_coordination(self, instance):
        user = self.request.user

        return user.groups.filter(
            pk__in=[ur_constants.KOOR_NP_GROUP_ID, ur_constants.KOOR_BG_GROUP_ID]
        )

    def has_object_unlink_permission(self, instance):
        return self.has_object_link_permission(instance)

    @permission_aware
    def has_object_convert_modification_permission(self, instance):
        return False

    def has_object_convert_modification_permission_for_municipality(self, instance):
        return (
            instance.responsible_service(filter_type="municipality")
            == self.request.group.service
        )

    def has_object_convert_modification_permission_for_support(self, instance):
        return True

    @permission_aware
    def has_object_appeal_permission(self, instance):
        return False

    def has_object_appeal_permission_for_municipality(self, instance):
        return (
            (
                instance.responsible_service(filter_type="municipality")
                == self.request.group.service
            )
            and instance.previous_instance_state.name == "coordination"
            and instance.instance_state.name in ["finished", "sb1"]
        )

    @permission_aware
    def has_object_correction_permission(self, instance):
        return False

    def has_object_correction_permission_for_municipality(self, instance):
        if not settings.CORRECTION:  # pragma: no cover
            return False

        if self.request.group.role.name != "municipality-lead":
            return False

        return instance.instance_state.name in [
            *settings.CORRECTION["ALLOWED_INSTANCE_STATES"],
            settings.CORRECTION["INSTANCE_STATE"],
        ]

    def has_object_correction_permission_for_support(self, instance):
        return True

    def has_object_rejection_permission(self, instance):
        return RejectionLogic.has_permission(instance, self.request.group)

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):  # pragma: no cover
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):  # pragma: no cover
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):  # pragma: no cover
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, pk=None):
        return super().destroy(request, pk=pk)

    @transaction.atomic
    def perform_destroy(self, instance):
        # TODO: this should be done for SZ as well - at least for related cases
        if settings.APPLICATION["FORM_BACKEND"] == "caluma":
            # Get documents related to the instance before deleting the cases
            document_ids = list(
                form_models.Document.objects.filter(
                    Q(family__case__family__instance=instance)
                    | Q(family__work_item__case__family__instance=instance)
                ).values_list("pk", flat=True)
            )

            # Delete cases (and work items via cascading) related to the instance
            workflow_models.Case.objects.filter(family__instance=instance).delete()

            # Delete documents (and answers via cascading) after the cases to avoid
            # protected errors
            form_models.Document.objects.filter(pk__in=document_ids).delete()

        # Delete instance
        super().perform_destroy(instance)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["get"], detail=True, renderer_classes=[JSONRenderer])
    def gwr_data(self, request, pk):
        """Export instance data to GWR."""
        case = workflow_models.Case.objects.get(instance__pk=pk)
        resolver = gwr_lookups.GwrSerializer(case)

        return response.Response(resolver.data)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["get"], detail=False)
    def export_list(self, request):
        """Export filtered instances to given file format."""
        resource_instance_state_ids = [
            val.strip() for val in request.query_params["instance-state-ids"].split(",")
        ]

        fields_queryset = models.FormField.objects.filter(instance=OuterRef("pk"))
        queryset = (
            self.get_queryset()
            .select_related("location", "user", "form", "instance_state")
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
        ).filter(instance_state__in=resource_instance_state_ids)

        queryset = self.filter_queryset(queryset)

        def applicant_names(instance):
            overrides = models.FormField.objects.filter(
                instance=instance, name="projektverfasser-planer-override"
            ).values("value")

            applicants = overrides if len(overrides) else (instance.applicants or [])

            return ", ".join(
                [
                    f"{applicant.get('firma', '')} {applicant.get('vorname', '')} {applicant.get('name', '')}".strip()
                    for applicant in applicants
                ]
            )

        content = [
            [
                instance.pk,
                instance.identifier,
                instance.form.description,
                instance.location and instance.location.name,
                applicant_names(instance),
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

    def get_export_detail_data(self, instance, type):
        validator = validators.FormDataValidator(instance)

        data = {
            "formName": instance.form.description,
            "instanceIdentifier": instance.identifier,
            "modules": validator.get_active_modules_questions(),
        }

        renderer = DocxRenderer("camac/instance/templates/form-export.docx", data)
        return renderer.convert(type)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["get"], detail=True)
    def export_detail(self, request, pk=None):
        to_type = self.request.query_params.get("type", "docx")
        instance = self.get_object()

        response = HttpResponse()
        filename = "{0}.{1}".format(instance.form.description, to_type)
        response["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
        response["Content-Type"] = mimetypes.guess_type(filename)[0]

        buf = self.get_export_detail_data(instance, to_type)

        response.write(buf.read())
        return response

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    @transaction.atomic
    def submit(self, request, pk=None):
        if settings.APPLICATION["FORM_BACKEND"] == "caluma":
            return self._custom_serializer_action(request, pk)
        return self._submit_camac_ng(request, pk)

    def _submit_camac_ng(self, request, pk=None):
        # TODO: move this into the serializer
        instance = self.get_object()

        # change state of instance
        new_instance_state = (
            models.InstanceState.objects.get(name="subm").pk
            if instance.instance_state.name == "new"
            else instance.previous_instance_state.pk
        )
        data = {
            "previous_instance_state": instance.instance_state.pk,
            "instance_state": new_instance_state,
        }
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # remove the microseconds because this date is displayed in camac and
        # camac can't handle microseconds..
        camac_now = timezone.now().replace(microsecond=0)

        # create workflow item when configured
        workflow_item = settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get("SUBMIT")
        if workflow_item:
            WorkflowEntry.objects.create(
                group=1,
                workflow_item_id=workflow_item,
                instance_id=pk,
                workflow_date=camac_now,
            )

        filename = "{0}_{1:%d.%m.%Y}.pdf".format(
            instance.form.description, timezone.now()
        )
        file = File(self.get_export_detail_data(instance, "pdf"))

        attachment = Attachment(
            name=filename,
            instance=instance,
            size=0,
            mime_type="application/pdf",
            question="dokument-projektplane-projektbeschrieb",
            user=request.user,
            group=request.group,
        )
        attachment.path.save(filename, file)
        attachment.size = attachment.path.size
        attachment.attachment_sections.add(
            AttachmentSection.objects.get(
                pk=settings.APPLICATION["STORE_PDF"]["SECTION"]
            )
        )
        attachment.save()

        workflow_api.complete_work_item(
            work_item=instance.case.work_items.get(
                task_id__in=settings.APPLICATION["CALUMA"].get("SUBMIT_TASKS"),
                status=workflow_models.WorkItem.STATUS_READY,
            ),
            user=request.caluma_info.context.user,
        )

        # send notification email when configured
        notification_template = settings.APPLICATION["NOTIFICATIONS"].get("SUBMIT")
        if notification_template and instance.group.service.notification:
            send_mail(
                notification_template,
                self.get_serializer_context(),
                recipient_types=["municipality"],
                instance={"id": pk, "type": "instances"},
            )

        return response.Response(data=serializer.data)

    def _custom_serializer_action(self, request, pk=None, status_code=None):
        serializer = self.get_serializer(
            instance=self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if status_code == status.HTTP_204_NO_CONTENT:
            return response.Response(data=None, status=status_code)

        return response.Response(data=serializer.data, status=status_code)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["patch"], detail=True, url_path="link")
    def link(self, request, pk=None):
        instance = self.get_object()
        try:
            instance_to_link = self.get_queryset().get(
                pk=request.data["data"]["attributes"]["link-to"]
            )
        except models.Instance.DoesNotExist:  # pragma: no cover
            raise ValidationError("Instance to link to not found")

        link_instances(instance, instance_to_link)

        return response.Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["patch"], detail=True, url_path="unlink")
    @transaction.atomic
    def unlink(self, request, pk=None):
        instance = self.get_object()

        instances_with_same_group = models.Instance.objects.filter(
            instance_group=instance.instance_group
        ).exclude(pk=instance.pk)
        # if only two dossiers were in group, unlink both
        if len(instances_with_same_group) == 1:
            instances_with_same_group.update(instance_group=None)

        instance.instance_group = None
        instance.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["patch"], detail=True, url_path="convert-modification")
    def convert_modification(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def report(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def finalize(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True, url_path="change-responsible-service")
    def change_responsible_service(self, request, pk=None):
        return self._custom_serializer_action(request, pk, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True, url_path="set-ebau-number")
    def set_ebau_number(self, request, pk=None):
        return self._custom_serializer_action(request, pk, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["PDF generation service"],
        manual_parameters=[
            group_param,
            openapi.Parameter(
                "form-slug",
                openapi.IN_QUERY,
                description="The form that should be used instead of the main form. E.g. 'sb1' or 'sb2' for self-declaration forms.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_SLUG,
            ),
            openapi.Parameter(
                "document-id",
                openapi.IN_QUERY,
                description="The UUID of the document that should be converted to a PDF. If passed, this will override the form-slug parameter.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
        ],
        operation_description=get_operation_description(["Nexplore"]),
        operation_summary="Generate a PDF for an instance",
        responses={"200": "PDF file"},
    )
    @action(methods=["get"], detail=True, url_path="generate-pdf")
    def generate_pdf(self, request, pk=None):
        form_slug = self.request.query_params.get("form-slug")
        document_id = self.request.query_params.get("document-id")
        template = self.request.query_params.get("template")

        instance = self.get_object()

        pdf = document_merge_service.DMSHandler().generate_pdf(
            instance.pk, request, form_slug, document_id, template
        )

        response = SendfileHttpResponse(
            content_type="application/pdf", filename=pdf.name, file_obj=pdf.file
        )
        return response

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def archive(self, request, pk=None):
        return self._custom_serializer_action(request, pk, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True, url_path="change-form")
    def change_form(self, request, pk=None):
        return self._custom_serializer_action(request, pk, status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True, url_path="fix-work-items")
    def fix_work_items(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @swagger_auto_schema(auto_schema=None)
    @action(
        methods=["get"],
        detail=True,
        renderer_classes=[JSONRenderer],
        url_path="dms-placeholders",
    )
    def dms_placeholders(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object())
        return response.Response(serializer.data)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def appeal(self, request, pk):
        if not settings.APPEAL:
            raise NotFound()

        return self._custom_serializer_action(
            request, pk, status_code=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def correction(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @swagger_auto_schema(auto_schema=None)
    @action(methods=["post"], detail=True)
    def rejection(self, request, pk=None):
        return self._custom_serializer_action(request, pk)


class InstanceResponsibilityView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    swagger_schema = None
    serializer_class = serializers.InstanceResponsibilitySerializer
    filterset_class = filters.InstanceResponsibilityFilterSet
    queryset = models.InstanceResponsibility.objects.all()
    prefetch_for_includes = {"service": ["service__groups"]}

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter(service=self.request.group.service)

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission."""
        queryset = super().get_base_queryset()
        return queryset.none()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_canton(self):
        return True

    def has_update_permission_for_service(self):
        return True

    def has_update_permission_for_municipality(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_canton(self):
        return True

    def has_destroy_permission_for_service(self):
        return True

    def has_destroy_permission_for_municipality(self):
        return True


class FormFieldView(
    mixins.InstanceQuerysetMixin, mixins.InstanceEditableMixin, views.ModelViewSet
):
    """
    Access form field of an instance.

    Rule is that only applicant may update it but whoever
    is allowed to read instance may read form data as well.
    """

    swagger_schema = None
    serializer_class = serializers.FormFieldSerializer
    filterset_class = filters.FormFieldFilterSet
    queryset = models.FormField.objects.all()
    instance_editable_permission = "form"
    permission_classes = [DefaultPermission | PublicationPermission]

    def has_destroy_permission(self):
        return False

    def get_queryset(self):
        return super().get_queryset().visible_for(self.request)


class JournalEntryView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """Journal entries used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.JournalEntrySerializer
    filterset_class = filters.JournalEntryFilterSet
    queryset = models.JournalEntry.objects.all()
    ordering_fields = "creation_date"
    ordering = "-creation_date"

    def get_queryset(self):
        return super().get_queryset().visible_for(self.request)

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_commission(self):
        return False

    def has_create_permission_for_coordination(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_object_update_permission(self, obj):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any journal entries
        return False

    def has_object_update_permission_for_canton(self, obj):
        return obj.user == self.request.user

    def has_object_update_permission_for_coordination(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @permission_aware
    def has_object_destroy_permission(self, obj):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)


class HistoryEntryView(
    mixins.InstanceQuerysetMixin, mixins.InstanceEditableMixin, views.ModelViewSet
):
    """History entries used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.HistoryEntrySerializer
    filterset_class = filters.HistoryEntryFilterSet
    queryset = models.HistoryEntry.objects.all()
    ordering_fields = ("created_at",)

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter(
            Q(service=self.request.group.service_id) | Q(service__isnull=True)
        )

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission."""
        queryset = super().get_base_queryset()
        return queryset.none()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_support(self):
        return True

    @permission_aware
    def has_object_update_permission(self, object):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any history entries
        return False

    def has_object_update_permission_for_support(self, object):
        return True

    @permission_aware
    def has_object_destroy_permission(self, object):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_support(self, object):
        return True


class IssueView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """Issues used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.IssueSerializer
    filterset_class = filters.InstanceIssueFilterSet
    queryset = models.Issue.objects.all()

    def get_queryset(self):
        return super().get_queryset().visible_for(self.request)

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_object_update_permission(self, obj):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any issues
        return False

    def has_object_update_permission_for_canton(self, obj):
        return obj.service == self.request.group.service

    def has_object_update_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @permission_aware
    def has_object_destroy_permission(self, obj):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)


class IssueTemplateView(views.ModelViewSet):
    """Issues templates used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.IssueTemplateSerializer
    filterset_class = filters.IssueTemplateFilterSet
    queryset = models.IssueTemplate.objects.all()

    @permission_aware
    def get_queryset(self):
        return models.IssueTemplate.objects.none()

    def get_queryset_for_canton(self):
        return models.IssueTemplate.objects.all()

    def get_queryset_for_service(self):
        return models.IssueTemplate.objects.filter(service=self.request.group.service)

    def get_queryset_for_municipality(self):
        return models.IssueTemplate.objects.filter(group=self.request.group)

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_object_update_permission(self, obj):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any issues
        return False

    def has_object_update_permission_for_canton(self, obj):
        return obj.service == self.request.group.service

    def has_object_update_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @permission_aware
    def has_object_destroy_permission(self, obj):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)


class IssueTemplateSetView(views.ModelViewSet):
    """Issue sets used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.IssueTemplateSetSerializer
    filterset_class = filters.IssueTemplateSetFilterSet
    queryset = models.IssueTemplateSet.objects.all()

    @permission_aware
    def get_queryset(self):
        return models.IssueTemplateSet.objects.none()

    def get_queryset_for_canton(self):
        return models.IssueTemplateSet.objects.all()

    def get_queryset_for_service(self):
        return models.IssueTemplateSet.objects.filter(
            service=self.request.group.service
        )

    def get_queryset_for_municipality(self):
        return models.IssueTemplateSet.objects.filter(group=self.request.group)

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_object_update_permission(self, obj):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any issues
        return False

    def has_object_update_permission_for_canton(self, obj):
        return obj.service == self.request.group.service

    def has_object_update_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @permission_aware
    def has_object_destroy_permission(self, obj):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.IssueTemplateSetApplySerializer,
    )
    @transaction.atomic
    def apply(self, request, pk=None):
        """Create issues from a issue template set."""
        issue_template_set = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data["instance"]

        issues = []
        for template in issue_template_set.issue_templates.all():
            issues.append(
                models.Issue(
                    group=template.group,
                    instance=instance,
                    service=template.service,
                    user=template.user,
                    deadline_date=timezone.now().date()
                    + timedelta(int(template.deadline_length)),
                    text=template.text,
                )
            )
        models.Issue.objects.bulk_create(issues)

        return response.Response([], 204)


class PublicCalumaInstanceView(mixins.InstanceQuerysetMixin, ListAPIView):
    """Public view for published instances."""

    permission_classes = [
        # This API is used by ÖREB in Kt. Uri
        (IsApplication("kt_uri") & DefaultPermission)
        | PublicationPermission
    ]
    serializer_class = serializers.PublicCalumaInstanceSerializer
    filterset_class = filters.PublicCalumaInstanceFilterSet
    queryset = workflow_models.Case.objects.all()

    instance_field = "instance"

    if settings.APPLICATION_NAME == "kt_uri":  # pragma: no cover

        @swagger_auto_schema(
            tags=["Public caluma instances"],
            operation_summary="Get list of public caluma instances",
            operation_description="Public view for published instances",
        )
        def get(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

    else:
        swagger_schema = None

    @permission_aware
    def get_queryset(self):
        return super().get_queryset().none()

    def get_queryset_for_public(self):
        queryset = (
            super().get_queryset_for_public().annotate(instance_id=F("instance__pk"))
        )

        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            queryset = queryset.prefetch_related("instance__fields")
        elif settings.APPLICATION["FORM_BACKEND"] == "caluma":
            queryset = queryset.prefetch_related(
                *build_document_prefetch_statements(prefix="document")
            )

        if settings.PUBLICATION.get("BACKEND") == "camac-ng":
            queryset = queryset.annotate(
                dossier_nr=Cast(
                    KeyTextTransform("dossier-number", "meta"), CharField()
                ),
                publication_end_date=Subquery(
                    PublicationEntry.objects.filter(
                        instance_id=OuterRef("instance_id")
                    ).values("publication_end_date")[:1]
                ),
            ).order_by("instance__location__name", "publication_end_date", "dossier_nr")
        elif settings.PUBLICATION.get("BACKEND") == "caluma":
            special_id = (
                "ebau-number"
                if settings.APPLICATION_NAME == "kt_bern"
                else "dossier-number"
            )
            queryset = queryset.annotate(
                dossier_nr=Cast(
                    KeyTextTransform(
                        special_id,
                        "meta",
                    ),
                    CharField(),
                ),
                year=Cast(
                    Func(
                        F("dossier_nr"),
                        Value(r"-\d+$"),
                        Value(""),
                        function="regexp_replace",
                    ),
                    IntegerField(),
                ),
                nr=Cast(
                    Func(
                        F("dossier_nr"),
                        Value(r"^\d+-"),
                        Value(""),
                        function="regexp_replace",
                    ),
                    IntegerField(),
                ),
            ).order_by("year", "nr")

        return queryset

    def get_queryset_for_oereb_api(self):
        queryset = (
            super()
            .get_queryset_for_oereb_api(self.request.group)
            .prefetch_related(
                *build_document_prefetch_statements(prefix="document"),
            )
            .annotate(instance_id=F("instance__pk"))
            .filter(Q(meta__oereb_copy__isnull=True) | Q(meta__oereb_copy=False))
        )
        return queryset.annotate(
            dossier_nr=Cast(KeyTextTransform("dossier-number", "meta"), CharField()),
            publication_date=Subquery(
                PublicationEntry.objects.filter(
                    instance_id=OuterRef("instance_id")
                ).values("publication_date")[:1]
            ),
        ).order_by("-publication_date", "dossier_nr")
