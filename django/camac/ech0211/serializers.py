from types import SimpleNamespace

from alexandria.core.api import create_document_file as create_alexandria_document_file
from alexandria.core.models import Category
from django.conf import settings
from django.urls import reverse
from django_clamd.validators import validate_file_infection
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Serializer
from rest_framework_json_api import relations, serializers

from camac.alexandria.extensions.common import (
    has_alexandria_create_permission,
    has_alexandria_move_permission,
)
from camac.core.serializers import MultilingualField
from camac.document import models as document_models
from camac.document.serializers import AttachmentSerializer
from camac.instance.models import Instance
from camac.user import models as user_models

from . import models

DOCUMENT_FIELDS = [
    "instance",
    "date",
    "category",
    "title",
    "mime_type",
    "size",
    "description",
    "created_at",
    "created_by_user",
    "created_by_service",
    "download_url",
]

CATEGORY_FIELDS = [
    "parent",
    "name",
]


class AllowedCategoryPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Category.objects.filter(
            pk__in=settings.ECH0211.get("ALLOWED_CATEGORIES", []),
        )


class AllowedAttachmentSectionPrimaryKeyRelatedField(
    serializers.PrimaryKeyRelatedField
):
    def get_queryset(self):
        return document_models.AttachmentSection.objects.filter(
            pk__in=settings.ECH0211.get("ALLOWED_ATTACHMENT_SECTIONS", []),
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
        if not has_alexandria_create_permission(
            self.context["request"],
            validated_data["instance"],
            validated_data["category"],
        ):
            raise PermissionDenied()

        return validated_data

    def validate_content(self, value):
        validate_file_infection(value)
        return value

    def create(self, validated_data):
        content = validated_data["content"]

        return create_alexandria_document_file(
            user=self.context["request"].user.pk,
            group=self.context["request"].group.service_id,
            category=validated_data["category"],
            document_title=content.name,
            file_name=content.name,
            file_content=content,
            mime_type=content.content_type,
            file_size=content.size,
            additional_document_attributes={
                "metainfo": {"camac-instance-id": str(validated_data["instance"].pk)},
            },
        )


class ECHCamacFileSerializer(Serializer):
    instance = serializers.PrimaryKeyRelatedField(
        queryset=Instance.objects,
        help_text="Instance to link the file to.",
    )
    category = AllowedAttachmentSectionPrimaryKeyRelatedField()
    content = serializers.FileField(help_text="File to upload.")

    def __init__(self, *args, data=None, context=None, **kwargs):
        att_data = (
            {
                "instance": data["instance"],
                "attachment_sections": [data["category"]],
                "path": data["content"],
            }
            if data
            else None
        )
        self._attachment_serializer = AttachmentSerializer(
            data=att_data,
            context=context,
        )
        super().__init__(*args, data=data, context=context, **kwargs)

    def is_valid(self, *, raise_exception=False):
        self_valid = super().is_valid(raise_exception=raise_exception)
        try:
            att_valid = self._attachment_serializer.is_valid(
                raise_exception=raise_exception
            )
        except exceptions.ValidationError as exc:
            if "disallowed-attachment-section" in exc.get_codes().get(
                "attachment_sections", []
            ):
                # This is actually a permission issues, so
                # we should raise 403 not 400
                raise PermissionDenied()

        return self_valid and att_valid

    def create(self, validated_data):
        attachment = self._attachment_serializer.create(
            self._attachment_serializer.validated_data
        )

        # Camac attachments are not split into "document" and "file" structures,
        # thus we're returnign the attachment twice for the same effect
        return attachment, attachment


class ECH0211CamacCategorySerializer(serializers.Serializer):
    parent = relations.SerializerMethodResourceRelatedField(
        model=models.ECH0211CamacCategory,
        allow_null=True,
        source="get_parent",
    )

    name = MultilingualField()

    # Camac document module doesn't know hierarchies, so we
    # just return the name again
    full_name = MultilingualField(source="name")

    description = MultilingualField()

    # Note: We have a slightly differing API here as we don't define
    # `included_serializers` for the parent. This is OK though, as the parent
    # never exists in this implementation

    def get_parent(self, cat):
        # Camac document categories are not hierarchical, but we
        # need to represent the same compatible structure
        return None

    class Meta:
        resource_name = "ech0211-document-categories"
        fields = CATEGORY_FIELDS


class ECH0211CamacDocumentSerializer(serializers.ModelSerializer):
    included_serializers = {"category": ECH0211CamacCategorySerializer}

    instance = serializers.ResourceRelatedField(
        queryset=Instance.objects,
        help_text="Instance to link the file to.",
    )
    category = serializers.ResourceRelatedField(
        queryset=models.ECH0211CamacCategory.objects
    )

    title = serializers.CharField(source="attachment.display_name")
    description = serializers.ReadOnlyField(default="")

    created_at = serializers.DateTimeField(source="date")
    size = serializers.IntegerField()

    created_by_user = serializers.ResourceRelatedField(source="user", read_only=True)
    created_by_service = serializers.ResourceRelatedField(
        source="service", read_only=True
    )

    mime_type = serializers.CharField()
    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj: models.ECH0211Document):
        return reverse("ech-file-detail", args=[obj.pk])

    class Meta:
        resource_name = "ech0211-documents"
        fields = DOCUMENT_FIELDS
        model = models.ECH0211Document


class ECH0211AlexandriaCategorySerializer(serializers.Serializer):
    parent = serializers.ResourceRelatedField(
        read_only=True,
        model=models.ECH0211AlexandriaCategory,
    )
    name = serializers.CharField()

    full_name = serializers.SerializerMethodField()
    description = serializers.CharField()
    included_serializers = {
        "parent": "camac.ech0211.serializers.ECH0211AlexandriaCategorySerializer"
    }

    def get_full_name(self, obj):
        if obj.parent:
            return " › ".join([str(obj.parent.name), str(obj.name)])
        return str(obj.name)

    class Meta:
        resource_name = "ech0211-document-categories"
        fields = CATEGORY_FIELDS


class ECH0211AlexandriaDocumentSerializer(serializers.ModelSerializer):
    # Note: We do not want to allow includes on the instance, as this would
    # require querying the instances, which would trigger an N+1 issue

    included_serializers = {"category": ECH0211AlexandriaCategorySerializer}

    instance = relations.SerializerMethodResourceRelatedField(
        help_text="Instance to link the file to.",
        source="get_instance",
        model=Instance,
        read_only=True,
        many=False,
    )

    category = serializers.ResourceRelatedField(
        queryset=models.ECH0211AlexandriaCategory.objects
    )

    title = serializers.CharField()
    description = serializers.CharField()
    download_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    size = serializers.SerializerMethodField()
    mime_type = serializers.SerializerMethodField()

    created_by_user = relations.SerializerMethodResourceRelatedField(
        model=user_models.User
    )
    created_by_service = relations.SerializerMethodResourceRelatedField(
        model=user_models.Service
    )

    def get_download_url(self, obj: models.ECH0211AlexandriaDocument):
        file = obj.most_recent_file
        if file:
            return reverse("ech-file-detail", args=[file.pk])

    def get_mime_type(self, obj):
        file = obj.most_recent_file

        if file:
            return file.mime_type

    def get_created_by_user(self, obj):
        # We don't actually lookup the user - instead we return a "simple
        # namespace" containing its PK. This is enough for DRF/JSONAPI to
        # render its relationship
        user = SimpleNamespace(
            pk=obj.created_by_user,
            _meta=SimpleNamespace(model=user_models.User),
        )
        return user

    def get_created_by_service(self, obj):
        # We don't actually lookup the group - instead we return a "simple
        # namespace" containing its PK. This is enough for DRF/JSONAPI to
        # render its relationship
        #
        # Also note that due to Alexandria's data model, created_by_group
        # is not a foreign key, and we actually store the user's service ID
        # in there
        service = SimpleNamespace(
            pk=obj.created_by_group,
            _meta=SimpleNamespace(model=user_models.Service),
        )
        return service

    def get_size(self, doc):
        file = doc.most_recent_file
        return file.size if file else None

    def get_instance(self, doc):
        return doc.instance_document.instance

    def validate_category(self, new_category):
        new_category = super().validate(new_category)
        if new_category and self.instance.category.pk != new_category.pk:
            document = self.instance
            instance = document.instance_document.instance

            if new_category.pk not in settings.ECH0211.get(
                "ALLOWED_CATEGORIES", []
            ) or not has_alexandria_move_permission(
                self.context["request"], instance, document, new_category
            ):
                raise PermissionDenied()

        return new_category

    class Meta:
        resource_name = "ech0211-documents"
        fields = DOCUMENT_FIELDS + ["marks"]
        read_only_fields = ["marks"]
        model = models.ECH0211AlexandriaDocument
