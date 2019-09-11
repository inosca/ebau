import io
import mimetypes
from datetime import timedelta

import django_excel
from django.conf import settings
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse
from django.utils import timezone
from docxtpl import DocxTemplate
from rest_framework import exceptions, response, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.settings import api_settings
from rest_framework_json_api import views

from camac.core.models import WorkflowEntry
from camac.notification.serializers import NotificationTemplateSendmailSerializer
from camac.unoconv import convert
from camac.user.permissions import permission_aware

from ..jinja import get_jinja_env
from . import filters, mixins, models, serializers, validators


class InstanceStateView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.InstanceStateSerializer
    ordering = ("sort", "name")

    def get_queryset(self):
        return models.InstanceState.objects.all()


class FormView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FormSerializer

    def get_queryset(self):
        return models.Form.objects.all()


class FormConfigDownloadView(RetrieveAPIView):
    path = settings.APPLICATION_DIR("form.json")

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

    filterset_class = filters.InstanceFilterSet
    queryset = models.Instance.objects.all()
    prefetch_for_includes = {
        "circulations": ["circulations__activations"],
        "active_service": ["services"],
        "responsible_service_users": [
            "responsible_services",
            "responsible_services__responsible_user",
        ],
    }
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
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
        filter_backends = filter_backends + [filters.InstanceFormFieldFilterBackend]

    def get_serializer_class(self):
        backend = settings.APPLICATION["FORM_BACKEND"]

        SERIALIZER_CLASS = {
            "caluma": {
                "submit": serializers.CalumaInstanceSubmitSerializer,
                "report": serializers.CalumaInstanceReportSerializer,
                "finalize": serializers.CalumaInstanceFinalizeSerializer,
                "default": serializers.CalumaInstanceSerializer,
            },
            "camac-ng": {
                "submit": serializers.InstanceSubmitSerializer,
                "default": serializers.InstanceSerializer,
            },
        }

        return SERIALIZER_CLASS[backend].get(
            self.action, SERIALIZER_CLASS[backend]["default"]
        )

    def has_base_permission(self, instance):
        return instance.involved_applicants.filter(invitee=self.request.user).exists()

    def has_object_destroy_permission(self, instance):
        return (
            self.has_base_permission(instance)
            and instance.instance_state.name == "new"
            and instance.previous_instance_state.name == "new"
        )

    def has_object_submit_permission(self, instance):
        return self.has_base_permission(instance) and instance.instance_state.name in (
            "new",
            "nfd",  # kt. schwyz
            # kt. bern (TODO: rejected instances should be copied and resubmitted from "new" state)
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

    @action(methods=["get"], detail=True)
    def export_detail(self, request, pk=None):
        to_type = self.request.query_params.get("type", "docx")
        instance = self.get_object()
        validator = validators.FormDataValidator(instance)

        data = {
            "formName": instance.form.description,
            "instanceIdentifier": instance.identifier,
            "modules": validator.get_active_modules_questions(),
        }

        response = HttpResponse()
        filename = "{0}.{1}".format(instance.form.description, to_type)
        response["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
        response["Content-Type"] = mimetypes.guess_type(filename)[0]

        buf = io.BytesIO()
        doc = DocxTemplate("camac/instance/templates/form-export.docx")
        doc.render(data, get_jinja_env())
        doc.save(buf)

        buf.seek(0)
        if to_type != "docx":
            content = convert(buf, to_type)
            if content is None:
                raise exceptions.ParseError()
            buf = io.BytesIO(content)

        response.write(buf.read())
        return response

    @action(methods=["post"], detail=True)
    @transaction.atomic
    def submit(self, request, pk=None):
        if settings.APPLICATION["FORM_BACKEND"] == "caluma":
            return self._submit_caluma(request, pk)

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
        now = timezone.now()
        camac_now = now - timedelta(microseconds=now.microsecond)

        # create workflow item when configured
        workflow_item = settings.APPLICATION["SUBMIT"].get("WORKFLOW_ITEM")
        if workflow_item:
            WorkflowEntry.objects.create(
                group=1,
                workflow_item_id=workflow_item,
                instance_id=pk,
                workflow_date=camac_now,
            )

        # send notification email when configured
        notification_template = settings.APPLICATION["SUBMIT"].get(
            "NOTIFICATION_TEMPLATE"
        )
        if notification_template and instance.group.service.notification:
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

    def _custom_serializer_action(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(data=serializer.data)

    def _submit_caluma(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @action(methods=["post"], detail=True)
    def report(self, request, pk=None):
        return self._custom_serializer_action(request, pk)

    @action(methods=["post"], detail=True)
    def finalize(self, request, pk=None):
        return self._custom_serializer_action(request, pk)


class InstanceResponsibilityView(mixins.InstanceQuerysetMixin, views.ModelViewSet):

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

    serializer_class = serializers.FormFieldSerializer
    filterset_class = filters.FormFieldFilterSet
    queryset = models.FormField.objects.all()
    instance_editable_permission = "form"

    def has_destroy_permission(self):
        return False

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        permission = perms.get(self.request.group.role.get_name(), "applicant")
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

    serializer_class = serializers.JournalEntrySerializer
    filterset_class = filters.JournalEntryFilterSet
    queryset = models.JournalEntry.objects.all()

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


class IssueView(mixins.InstanceQuerysetMixin, views.ModelViewSet):
    """Issues used for internal use and not viewable by applicant."""

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
