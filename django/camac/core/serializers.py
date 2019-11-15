from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import exceptions
from rest_framework_json_api import relations, serializers

from camac.instance.models import Instance

from . import models


class MultilingualSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()


class PublicationEntrySerializer(serializers.ModelSerializer):
    instance = relations.ResourceRelatedField(queryset=Instance.objects)
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        # We include this form field to avoid creating a whitelist for fields
        try:
            return obj.instance.fields.get(name="bezeichnung").value
        except ObjectDoesNotExist:
            return ""

    included_serializers = {"instance": "camac.instance.serializers.InstanceSerializer"}

    @transaction.atomic
    def update(self, instance, validated_data):
        if not instance.is_published and validated_data["is_published"]:
            # remove the microseconds because this date is displayed in camac and
            # camac can't handle microseconds..
            camac_now = timezone.now().replace(microsecond=0)

            models.WorkflowEntry.objects.create(
                group=instance.instance.group.pk,
                workflow_item_id=settings.APPLICATION["PUBLICATION"].get(
                    "WORKFLOW_ITEM"
                ),
                instance_id=instance.instance.pk,
                workflow_date=camac_now,
            )

        return super().update(instance, validated_data)

    class Meta:
        model = models.PublicationEntry
        fields = ("instance", "publication_date", "is_published", "description")
        read_only_fields = ("description",)


class PublicationEntryUserPermissionSerializer(serializers.ModelSerializer):
    publication_entry = relations.ResourceRelatedField(
        queryset=models.PublicationEntry.objects
    )

    included_serializers = {"user": "camac.user.serializers.UserSerializer"}

    @transaction.atomic
    def create(self, validated_data):
        if models.PublicationEntryUserPermission.objects.filter(
            publication_entry=validated_data["publication_entry"],
            user=self.context["request"].user,
        ).exists():
            raise exceptions.ValidationError("Entry already exists")

        validated_data["user"] = self.context["request"].user
        validated_data["status"] = "pending"

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data["status"] == "pending":
            raise exceptions.ValidationError("Invalid State")

        return super().update(instance, validated_data)

    class Meta:
        model = models.PublicationEntryUserPermission
        fields = ("status", "publication_entry", "user")
        read_only_fields = ("publication_entry", "user")
