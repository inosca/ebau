from rest_framework_json_api import serializers

from camac.user.relations import (
    CurrentUserFormDataResourceRelatedField,
    GroupFormDataResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault

from . import models
from .validation import validate_zip_archive_structure, verify_source_file


class DossierImportSerializer(serializers.ModelSerializer):
    user = CurrentUserFormDataResourceRelatedField()
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    location_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.DossierImport
        fields = (
            "status",
            "service",
            "group",
            "user",
            "location",
            "location_id",
            "id",
            "messages",
            "source_file",
            "mime_type",
            "dossier_loader_type",
        )
        read_only_fields = ("id", "date", "messages", "service", "status")

    included_serializers = {
        "user": "camac.user.serializers.UserSerializer",
        "service": "camac.user.serializers.ServiceSerializer",
        "location": "camac.user.serializers.LocationSerializer",
    }

    def __init__(self, *args, **kwargs):
        self._warnings = []
        super().__init__(*args, **kwargs)

    def validate_source_file(self, source_file):
        return verify_source_file(source_file)

    def create(self, validated_data):
        dossier_import = super().create(validated_data)
        dossier_import.status = dossier_import.IMPORT_STATUS_IMPORT_INPROGRESS
        dossier_import.service = (
            validated_data.get("group") and validated_data["group"].service
        )
        dossier_import.save()
        dossier_import = validate_zip_archive_structure(str(dossier_import.pk))
        if dossier_import.status == dossier_import.IMPORT_STATUS_VALIDATION_FAILED:
            dossier_import.source_file.delete()
        return dossier_import
