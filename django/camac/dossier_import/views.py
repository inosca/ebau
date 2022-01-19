from django.conf import settings
from django_q.tasks import async_task
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet

from camac.dossier_import.domain_logic import perform_import, transmit_import
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.user.permissions import permission_aware


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

        # TODO send mails

        dossier_import.status = DossierImport.IMPORT_STATUS_CONFIRMED
        dossier_import.save()
        return Response()

    @permission_aware
    def has_object_transmit_permission(self, instance):
        return False

    @permission_aware
    def has_object_transmit_permission_for_support(self, instance):
        return True

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
