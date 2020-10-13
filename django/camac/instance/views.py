import mimetypes
from datetime import timedelta

import django_excel
from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models import OuterRef, Q, Subquery
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import response, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.settings import api_settings
from rest_framework_json_api import views

from camac.caluma.api import CalumaApi
from camac.core.models import InstanceService, WorkflowEntry
from camac.core.views import SendfileHttpResponse
from camac.document.models import Attachment, AttachmentSection
from camac.notification.views import send_mail
from camac.user.permissions import permission_aware
from camac.utils import DocxRenderer

from ..utils import get_paper_settings
from . import document_merge_service, filters, mixins, models, serializers, validators


class InstanceStateView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.InstanceStateSerializer
    ordering = ("sort", "name")

    def get_queryset(self):
        return models.InstanceState.objects.all()


class FormView(viewsets.ReadOnlyModelViewSet):
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

    def retrieve(self, request, **kwargs):
        with open(self.path) as json_file:
            response = HttpResponse(json_file, content_type="application/json")
            return response


class InstanceView(
    mixins.InstanceQuerysetMixin, mixins.InstanceEditableMixin, views.ModelViewSet
):
    swagger_schema = None
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
        "involved_services": [
            "services",
            "circulations",
            "circulations__activations",
            "circulations__activations__service",
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
    )

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
                "default": serializers.CalumaInstanceSerializer,
            },
            "camac-ng": {
                "submit": serializers.InstanceSubmitSerializer,
                "default": serializers.SchwyzInstanceSerializer,
            },
        }

        return SERIALIZER_CLASS[backend].get(
            self.action, SERIALIZER_CLASS[backend]["default"]
        )

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

    @transaction.atomic
    def destroy(self, request, pk=None):
        instance_id = self.get_object().pk
        response = super().destroy(request, pk=pk)

        if settings.APPLICATION["FORM_BACKEND"] == "caluma":
            CalumaApi().delete_instance_case(instance_id)

        return response

    @action(methods=["get"], detail=False)
    def export_list(self, request):
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
                    [
                        applicant["name"] if "name" in applicant else applicant["firma"]
                        for applicant in (instance.applicants or [])
                    ]
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

    def get_export_detail_data(self, instance, type):
        validator = validators.FormDataValidator(instance)

        data = {
            "formName": instance.form.description,
            "instanceIdentifier": instance.identifier,
            "modules": validator.get_active_modules_questions(),
        }

        renderer = DocxRenderer("camac/instance/templates/form-export.docx", data)
        return renderer.convert(type)

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

        serializer = self.get_serializer(instance, data=data, partial=True)
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

        # send notification email when configured
        notification_template = settings.APPLICATION["NOTIFICATIONS"].get("SUBMIT")
        if notification_template and instance.group.service.notification:
            send_mail(
                notification_template,
                self.get_serializer_context(),
                recipient_types=["municipality"],
                instance={"id": pk, "type": "instances"},
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
            AttachmentSection.objects.filter_group(request.group)[0]
        )
        attachment.save()

        workflow_api.complete_work_item(
            work_item=workflow_models.WorkItem.objects.get(
                **{
                    "task_id__in": settings.APPLICATION["CALUMA"].get("SUBMIT_TASKS"),
                    "status": workflow_models.WorkItem.STATUS_READY,
                    "case__meta__camac-instance-id": instance.pk,
                }
            ),
            user=request.caluma_info.context.user,
        )

        return response.Response(data=serializer.data)

    def _custom_serializer_action(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(data=serializer.data)

    @action(methods=["post"], detail=True)
    def report(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @action(methods=["post"], detail=True)
    def finalize(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @action(methods=["post"], detail=True, url_path="change-responsible-service")
    def change_responsible_service(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(None, 204)

    @action(methods=["get"], detail=True, url_path="generate-pdf")
    def generate_pdf(self, request, pk=None):
        form_slug = self.request.query_params.get("form-slug")
        instance = self.get_object()

        pdf = document_merge_service.DMSHandler().generate_pdf(
            instance, form_slug, request
        )

        response = SendfileHttpResponse(
            content_type="application/pdf", filename=pdf.name, file_obj=pdf.file
        )
        return response


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

    def has_destroy_permission(self):
        return False

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        permission = perms.get(self.request.group.role.name, "applicant")
        questions = [
            question
            for question, value in settings.FORM_CONFIG["questions"].items()
            # all permissions may read per default once they have access to instance
            if permission
            in value.get(
                "restrict",
                [
                    "applicant",
                    "public_reader",
                    "reader",
                    "canton",
                    "municipality",
                    "service",
                ],
            )
        ]

        return queryset.filter(name__in=questions)


class JournalEntryView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """Journal entries used for internal use and not viewable by applicant."""

    swagger_schema = None
    serializer_class = serializers.JournalEntrySerializer
    filterset_class = filters.JournalEntryFilterSet
    queryset = models.JournalEntry.objects.all()

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        query_filter = Q(visibility="all")

        if self.request.group != settings.APPLICATION["PORTAL_GROUP"]:
            service = self.request.group.service
            query_filter |= Q(visibility="own_organization", service=service)
            query_filter |= Q(visibility="authorities")

        return queryset.filter(query_filter)

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission.

        Specific permissions are defined in InstanceQuerysetMixin.
        """

        # TODO applicants currently don't have access to journal entries at all. Giving them access might
        # require a dedicated "applicant" role in our permission layer?
        return models.JournalEntry.objects.none()

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
    group_required = False
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

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter(service=self.request.group.service_id)

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
