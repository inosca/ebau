from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.utils.translation import gettext as _
from django_q.tasks import async_task
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet

from camac.core.views import SendfileHttpResponse
from camac.dossier_import.domain_logic import (
    clean_import,
    perform_import,
    set_status_callback,
    transmit_import,
    undo_import,
)
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.instance.models import Instance
from camac.user.permissions import permission_aware
from camac.utils import build_url


def is_prod():
    return (
        "local" not in settings.INTERNAL_BASE_URL
        and "test" not in settings.INTERNAL_BASE_URL
        and "-t" not in settings.INTERNAL_BASE_URL
    )


class DossierImportView(ModelViewSet):
    """View class for uploading a ZIP archive with dossier metadata and documents for import."""

    serializer_class = DossierImportSerializer
    queryset = DossierImport.objects.all().order_by("-created_at")

    instance_field = None

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_municipality(self):
        if is_prod():
            return self.queryset.none()

        groups = self.request.group.service.groups.all()
        return self.queryset.filter(group_id__in=groups)

    def get_queryset_for_support(self):
        return self.queryset.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if any(
            [
                Instance.objects.filter(
                    **{"case__meta__import-id": str(instance.pk)}
                ).exists(),
                Case.objects.filter(**{"meta__import-id": str(instance.pk)}).exists(),
            ]
        ):
            raise ValidationError(
                _(
                    "Cannot delete this import. There are still cases and instances referring to this import. Revert the import before deletion."
                )
            )
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.get_object().update_async_status()
        return super().retrieve(request, *args, **kwargs)

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
        dossier_import.status = DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS
        task_id = async_task(
            perform_import,
            dossier_import,
            hook=set_status_callback,
            # sync=settings.Q_CLUSTER.get("sync", True),  # TODO: running tasks sync does not work at
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
        subject = _("A dossier import for %(group)s has been approved") % {
            "group": dossier_import.group.get_name()
        }
        body = _("The approved dossiers can be viewed here:\n%(import_url)s") % {
            "import_url": build_url(
                settings.INTERNAL_BASE_URL,
                settings.DOSSIER_IMPORT["RESOURCE_ID_PATH"],
                str(dossier_import.pk),
            )
        }  # resource_id for dossier_import tab
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
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_aware
    def has_object_create_permission(self, instance):  # pragma: no cover
        return not is_prod()

    def has_object_create_permission_for_support(self, instance):  # pragma: no cover
        return True

    @permission_aware
    def has_object_transmit_permission(self, instance):
        return False

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

    @action(methods=["GET"], url_path="download", detail=True)
    def download(self, request, pk=None):
        dossier_import = self.get_object()

        return SendfileHttpResponse(
            content_type="application/zip",
            filename=dossier_import.filename(),
            base_path=settings.MEDIA_ROOT,
            file_path=f"/dossier_imports/files/{dossier_import.pk}/{dossier_import.filename()}",
        )

    @permission_aware
    def has_object_undo_permission(self, instance):  # pragma: no cover
        return False

    @permission_aware
    def has_object_undo_permission_for_municipality(self, instance):
        return instance.status in [
            DossierImport.IMPORT_STATUS_IMPORTED,
            DossierImport.IMPORT_STATUS_IMPORT_FAILED,
        ]

    @permission_aware
    def has_object_undo_permission_for_support(self, instance):
        return instance.status not in [
            DossierImport.IMPORT_STATUS_NEW,
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS,
        ]

    @action(methods=["POST"], url_path="undo", detail=True)
    def undo(self, request, pk=None):
        # removes all instances and cases that came with the import
        # - removes the dossier-import instance on success
        instance = self.get_object()
        instance.status = DossierImport.IMPORT_STATUS_UNDO_IN_PROGRESS
        task_id = async_task(undo_import, instance, hook=set_status_callback)
        instance.task_id = task_id
        instance.save()
        return Response({"task_id": task_id})

    @permission_aware
    def has_object_clean_permission(self, instance):  # pragma: no cover
        return False

    @permission_aware
    def has_object_clean_permission_for_support(self, instance):
        return True

    @action(methods=["POST"], url_path="clean", detail=True)
    def clean(self, request, pk=None):
        # removes the source archive from the file system
        # to clean up space.
        #  - does not remove any database entries.
        #  - does not remove the import instance
        clean_import(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
