from rest_framework_json_api.views import ModelViewSet

from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierImportSerializer
from camac.user.permissions import permission_aware


class DossierImportView(ModelViewSet):
    """View class for uploading a ZIP archive with dossier metadata and documents for import."""

    queryset = DossierImport.objects.all()
    serializer_class = DossierImportSerializer
    queryset = DossierImport.objects.all()
    instance_field = None

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_municipality(self):
        service_id = self.request.group.service_id
        return self.queryset.filter(service_id=service_id)

    def get_queryset_for_support(self):
        return self.queryset
