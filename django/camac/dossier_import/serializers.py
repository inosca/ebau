from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.user.relations import (
    CurrentUserFormDataResourceRelatedField,
    GroupFormDataResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault

from . import models
from .loaders import InvalidImportDataError
from .validation import validate_zip_archive_structure, verify_source_file


class DossierImportSerializer(serializers.ModelSerializer):
    user = CurrentUserFormDataResourceRelatedField()
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    location_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.DossierImport
        fields = (
            "created_at",
            "status",
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
        read_only_fields = ("id", "created_at", "messages", "status")

    included_serializers = {
        "user": "camac.user.serializers.UserSerializer",
        "group": "camac.user.serializers.GroupSerializer",
        "location": "camac.user.serializers.LocationSerializer",
    }

    def __init__(self, *args, **kwargs):
        self._warnings = []
        super().__init__(*args, **kwargs)

    def validate_source_file(self, source_file):
        return verify_source_file(source_file)

    def validate(self, data):
        if settings.APPLICATION["DOSSIER_IMPORT"].get(
            "LOCATION_REQUIRED", False
        ) and not data.get("location_id"):
            raise ValidationError(_("No location assigned."))
        return data

    def create(self, validated_data):
        dossier_import = super().create(validated_data)
        dossier_import.status = dossier_import.IMPORT_STATUS_IMPORT_INPROGRESS
        dossier_import.save()
        try:
            return validate_zip_archive_structure(str(dossier_import.pk))
        except InvalidImportDataError as e:
            raise ValidationError(e)
