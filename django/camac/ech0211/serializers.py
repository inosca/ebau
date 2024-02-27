from alexandria.core.models import Category, Document, File
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoCoreValidationError
from django_clamd.validators import validate_file_infection
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Serializer
from rest_framework_json_api import serializers

from camac.alexandria.extensions.permissions.extension import (
    MODE_CREATE,
    CustomPermission as CustomAlexandriaPermission,
)
from camac.instance.models import Instance


class AllowedCategoryPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Category.objects.filter(
            pk__in=settings.ECH0211.get("ALLOWED_CATEGORIES", []),
        )


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ()


class ECHFileSerializer(Serializer):
    instance = serializers.PrimaryKeyRelatedField(
        queryset=Instance.objects,
        help_text="Instance to link the file to.",
    )
    category = AllowedCategoryPrimaryKeyRelatedField()
    content = serializers.FileField(help_text="File to upload.")

    def validate(self, data):
        validated_data = super().validate(data)

        # This makes sure that the user has permission to create a file in the
        # passed category and also whether the user has permission to see the
        # passed instance so we don't have to check the instance visibility
        # seperately.
        available_permissions = CustomAlexandriaPermission().get_available_permissions(
            self.context["request"],
            validated_data["instance"],
            validated_data["category"],
        )

        if MODE_CREATE not in available_permissions:
            raise PermissionDenied()

        return validated_data

    def validate_content(self, value):
        validate_file_infection(value)
        return value

    def create(self, validated_data):
        user = self.context["request"].user.pk
        group = self.context["request"].group.service_id
        content = validated_data["content"]

        document = Document.objects.create(
            title=content.name,
            category=validated_data["category"],
            metainfo={"camac-instance-id": str(validated_data["instance"].pk)},
            created_by_user=user,
            created_by_group=group,
            modified_by_user=user,
            modified_by_group=group,
        )
        file = File.objects.create(
            document=document,
            name=content.name,
            content=content,
            mime_type=content.content_type,
            size=content.size,
            created_by_user=user,
            created_by_group=group,
            modified_by_user=user,
            modified_by_group=group,
        )

        try:
            file.create_thumbnail()
        except DjangoCoreValidationError:  # pragma: no cover
            # thumbnail could not be generated because of an unsupported
            # mime type
            pass

        return document
