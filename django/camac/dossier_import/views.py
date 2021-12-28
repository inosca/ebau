from django_q.tasks import async_task
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet

from camac.dossier_import.importing import perform_import
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.user.permissions import permission_aware


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
        service_id = self.request.group.service_id
        return self.queryset.filter(service_id=service_id)

    def get_queryset_for_support(self):
        return self.queryset

    @action(methods=["POST"], url_path="import-archive", detail=True)
    def import_archive(self, request, pk=None):
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
            # sync=settings.Q_CLUSTER.get("sync", False),
        )
        return Response({"task_id": task_id})
