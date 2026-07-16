from __future__ import annotations

from typing import TYPE_CHECKING

from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.http import FileResponse
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet

from camac.dossier_import.domain_logic import (
    clean_import,
    confirm_import,
    schedule_import,
    schedule_transmission,
    schedule_undo_import,
)
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.user.permissions import permission_aware

if TYPE_CHECKING:
    from django.db.models import QuerySet


def is_prod() -> bool:
    """Return `True` if we're on a production system.

    This considers every system that does not contain "local", "test", "-int" or
    "-t" in its URL a production system.
    """

    return (
        "local" not in settings.INTERNAL_BASE_URL
        and "test" not in settings.INTERNAL_BASE_URL
        and "-int" not in settings.INTERNAL_BASE_URL
        and "-t" not in settings.INTERNAL_BASE_URL
    )


class DossierImportView(ModelViewSet):
    """View class for uploading a ZIP archive with dossier metadata and documents for import."""

    serializer_class = DossierImportSerializer
    queryset = DossierImport.objects.order_by("-created_at")

    def has_municipality_base_permission(self) -> bool:
        """Check base permission for municipalities.

        Municipalities can't do anything in production per default. In Kt. SO
        only the support role is allowed to deal with dossier imports.
        """

        return not is_prod() and settings.APPLICATION_NAME != "kt_so"

    @permission_aware
    def get_queryset(self) -> QuerySet[DossierImport]:
        return self.queryset.none()

    def get_queryset_for_municipality(self) -> QuerySet[DossierImport]:
        if not self.has_municipality_base_permission():
            return self.queryset.none()

        groups = self.request.group.service.groups.all()
        return self.queryset.filter(group_id__in=groups)

    def get_queryset_for_support(self) -> QuerySet[DossierImport]:
        return self.queryset.all()

    @permission_aware
    def has_create_permission(self) -> bool:
        return self.has_municipality_base_permission()

    def has_create_permission_for_support(self) -> bool:
        return True

    @permission_aware
    def has_object_destroy_permission(self, obj: DossierImport) -> bool:
        return self.has_municipality_base_permission() and obj.status in [
            DossierImport.Status.VALIDATION_SUCCESSFUL,
            DossierImport.Status.VALIDATION_FAILED,
            DossierImport.Status.UNDONE,
        ]

    def has_object_destroy_permission_for_support(self, obj: DossierImport) -> bool:
        return obj.status in [
            DossierImport.Status.VALIDATION_SUCCESSFUL,
            DossierImport.Status.VALIDATION_FAILED,
            DossierImport.Status.UNDONE,
        ]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        if Case.objects.filter(**{"meta__import-id": str(obj.pk)}).exists():
            raise ValidationError(
                _(
                    "Cannot delete this import as there are still dossiers "
                    "referring to it. Revert the import before deletion."
                )
            )

        return super().destroy(request, *args, **kwargs)

    @permission_aware
    def has_object_start_permission(self, obj: DossierImport) -> bool:
        return (
            self.has_municipality_base_permission()
            and obj.status == DossierImport.Status.VALIDATION_SUCCESSFUL
        )

    def has_object_start_permission_for_support(self, obj: DossierImport) -> bool:
        return obj.status == DossierImport.Status.VALIDATION_SUCCESSFUL

    @action(methods=["POST"], detail=True)
    def start(self, request, pk=None):
        schedule_import(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    def has_object_confirm_permission(self, instance):
        return not is_prod() and instance.status == DossierImport.Status.IMPORTED

    @action(methods=["POST"], detail=True)
    def confirm(self, request, pk=None):
        confirm_import(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_aware
    def has_object_transmit_permission(self, obj: DossierImport) -> bool:
        return False

    def has_object_transmit_permission_for_support(self, obj: DossierImport) -> bool:
        return not is_prod() and obj.status == DossierImport.Status.CONFIRMED

    @action(methods=["POST"], detail=True)
    def transmit(self, request, pk=None):
        schedule_transmission(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=True)
    def download(self, request, pk=None):
        dossier_import = self.get_object()

        return FileResponse(
            dossier_import.source_file,
            content_type="application/zip",
            as_attachment=True,
            filename=dossier_import.filename(),
        )

    @permission_aware
    def has_object_undo_permission(self, obj: DossierImport) -> bool:
        return self.has_municipality_base_permission() and obj.status in [
            DossierImport.Status.IMPORTED,
            DossierImport.Status.IMPORT_FAILED,
            DossierImport.Status.UNDO_FAILED,
        ]

    def has_object_undo_permission_for_support(self, obj: DossierImport) -> bool:
        has_correct_status = obj.status in [
            DossierImport.Status.IMPORTED,
            DossierImport.Status.IMPORT_FAILED,
            DossierImport.Status.CONFIRMED,
            DossierImport.Status.UNDO_FAILED,
        ]

        if settings.APPLICATION_NAME == "kt_so":
            # In Kt. SO we allow undo of an import in production. In all other
            # cantons this is strictly forbidden.
            return has_correct_status

        return not is_prod() and has_correct_status

    @action(methods=["POST"], detail=True)
    def undo(self, request, pk=None):
        schedule_undo_import(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_aware
    def has_object_clean_permission(self, obj: DossierImport) -> bool:
        return False

    def has_object_clean_permission_for_support(self, obj: DossierImport) -> bool:
        return is_prod() and obj.status in [
            DossierImport.Status.IMPORTED,
            DossierImport.Status.CONFIRMED,
            DossierImport.Status.IMPORT_FAILED,
        ]

    @action(methods=["POST"], detail=True)
    def clean(self, request, pk=None):
        clean_import(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
