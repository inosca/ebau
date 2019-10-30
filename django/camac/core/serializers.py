from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework_json_api import relations, serializers

from camac.instance.models import Instance

from . import models


class MultilingualSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()


class PublicationEntrySerializer(serializers.ModelSerializer):
    instance = relations.ResourceRelatedField(queryset=Instance.objects.all())

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
        fields = ("instance", "publication_date", "is_published")
