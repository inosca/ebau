from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.utils.translation import gettext_lazy as _
from django_q.tasks import async_task
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet

from camac.dossier_import.domain_logic import (
    perform_import,
    transmit_import,
    undo_import,
)
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.user.permissions import permission_aware
from camac.utils import build_url


def is_prod():
    return (
        "sycloud" not in settings.INTERNAL_BASE_URL
        and "local" not in settings.INTERNAL_BASE_URL
    )


class DossierImportView(ModelViewSet):
    """View class for uploading a ZIP archive with dossier metadata and documents for import."""

    queryset = DossierImport.objects.all()
    serializer_class = DossierImportSerializer
    queryset = DossierImport.objects.all().order_by("-created_at")
    instance_field = None
    swagger_schema = None

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_municipality(self):
        if is_prod():
            return self.queryset.none()

        groups = self.request.group.service.groups.all()
        return self.queryset.filter(group_id__in=groups)

    def get_queryset_for_support(self):
        return self.queryset

    @action(methods=["POST"], url_path="start", detail=True)
    def start(self, request, pk=None):
        dossier_import = self.get_object()
        if (
            not dossier_import.status
            == DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL
        ):
            raise ValidationError(
                "Make sure the uploaded archive validates successfully.",
            )
        dossier_import.status = DossierImport.IMPORT_STATUS_IMPORT_INPROGRESS
        dossier_import.save()
        task_id = async_task(
            perform_import,
            dossier_import,
            # sync=settings.Q_CLUSTER.get("sync", False),  # TODO: running tasks sync does not work at
            #  the moment: django-q task loses db connection. maybe related to testing fixtures
        )
        dossier_import.task_id = task_id
        dossier_import.save()
        return Response({"task_id": task_id})

    @action(methods=["POST"], url_path="confirm", detail=True)
    def confirm(self, request, pk=None):
        dossier_import = self.get_object()
        if not dossier_import.status == DossierImport.IMPORT_STATUS_IMPORTED:
            raise ValidationError(
                "Confirming an import is only possible after it has been imported.",
            )
        subject = (
            _("A dossier import for %s has been approved")
            % dossier_import.group.get_name()
        )
        body = _("The approved dossiers can be viewed here:\n%(import_url)s") % dict(
            import_url=build_url(
                settings.INTERNAL_BASE_URL,
                settings.APPLICATION["DOSSIER_IMPORT"]["RESOURCE_ID_PATH"],
                str(dossier_import.pk),
            )
        )  # resource_id for dossier_import tab
        mail_admins(subject, message=body)
        if settings.SUPPORT_EMAIL_ADDRESS:
            send_mail(
                subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                message=body,
                recipient_list=[settings.SUPPORT_EMAIL_ADDRESS],
            )
        dossier_import.status = DossierImport.IMPORT_STATUS_CONFIRMED
        dossier_import.save()
        return Response()

    @permission_aware
    def has_object_transmit_permission(self, instance):
        return False

    @permission_aware
    def has_object_transmit_permission_for_support(self, instance):
        return not is_prod()

    @action(methods=["POST"], url_path="transmit", detail=True)
    def transmit(self, request, pk=None):
        dossier_import = self.get_object()
        if not dossier_import.status == DossierImport.IMPORT_STATUS_CONFIRMED:
            raise ValidationError(
                "Transmitting an import is only possible after it has been confirmed.",
            )

        task_id = async_task(
            transmit_import,
            dossier_import,
            # sync=settings.Q_CLUSTER.get("sync", False),  # TODO: running tasks sync does not work at
            #  the moment: django-q task loses db connection. maybe related to testing fixtures
        )
        dossier_import.task_id = task_id
        dossier_import.status = DossierImport.IMPORT_STATUS_TRANSMITTING
        dossier_import.save()

        return Response({"task_id": task_id})

    @permission_aware
    def has_object_undo_permission(self, instance):  # pragma: no cover
        return False

    @permission_aware
    def has_object_undo_permission_for_municipality(self, instance):
        return instance.status in [
            DossierImport.IMPORT_STATUS_IMPORTED,
        ]

    @permission_aware
    def has_object_undo_permission_for_support(self, instance):
        if is_prod():
            return False

        return instance.status not in [
            DossierImport.IMPORT_STATUS_NEW,
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            DossierImport.IMPORT_STATUS_IMPORT_FAILED,
            DossierImport.IMPORT_STATUS_IMPORT_INPROGRESS,
        ]

    @action(methods=["POST"], url_path="undo", detail=True)
    def undo(self, request, pk=None):
        undo_import(self.get_object())
        return Response()
