from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import relations, serializers

from camac.instance.models import Instance
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.views import send_mail
from camac.user.models import User

from . import models


class MultilingualField(serializers.Field):
    """
    Custom field for our legacy multilingual model fields.

    Make sure you pop the value from `validated_data` and handle any modifications to
    the translation table.
    """

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return value.get_trans_attr(self.source or self.field_name)

    def to_internal_value(self, data):
        return data


class MultilingualSerializer(serializers.Serializer):
    name = MultilingualField()


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
                workflow_item_id=settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get(
                    "PUBLICATION"
                ),
                instance_id=instance.instance.pk,
                workflow_date=camac_now,
            )

            work_item = workflow_models.WorkItem.objects.filter(
                **{
                    "task_id": "publication",
                    "case__meta__camac-instance-id": self.instance.instance.pk,
                    "status": workflow_models.WorkItem.STATUS_READY,
                }
            ).first()

            # TODO: test this
            if work_item:  # pragma: no cover
                workflow_api.complete_work_item(
                    work_item=work_item,
                    user=self.context["request"].caluma_info.context.user,
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
    user = relations.ResourceRelatedField(
        queryset=User.objects, default=serializers.CurrentUserDefault()
    )
    status = serializers.ChoiceField(
        choices=models.PublicationEntryUserPermission.STATES
    )

    included_serializers = {"user": "camac.user.serializers.UserSerializer"}

    @transaction.atomic
    def create(self, validated_data):
        validated_data["status"] = models.PublicationEntryUserPermission.PENDING
        permission = super().create(validated_data)

        # send notification email when configured
        notification_template = settings.APPLICATION["NOTIFICATIONS"].get(
            "PUBLICATION_PERMISSION"
        )

        if notification_template:
            send_mail(
                notification_template,
                self.context,
                PermissionlessNotificationTemplateSendmailSerializer,
                recipient_types=["municipality"],
                instance={
                    "id": validated_data["publication_entry"].instance.pk,
                    "type": "instances",
                },
            )

        return permission

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data["status"] == models.PublicationEntryUserPermission.PENDING:
            raise exceptions.ValidationError("Invalid State")

        return super().update(instance, validated_data)

    class Meta:
        model = models.PublicationEntryUserPermission
        fields = ("status", "publication_entry", "user")
        read_only_fields = ("publication_entry", "user")
        validators = [
            UniqueTogetherValidator(
                queryset=models.PublicationEntryUserPermission.objects.all(),
                fields=["publication_entry", "user"],
            )
        ]
