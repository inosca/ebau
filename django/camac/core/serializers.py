from caluma.caluma_workflow import api as workflow_api, models as workflow_models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework_json_api import relations, serializers

from camac.instance.models import Instance

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
            description_overwrite = obj.instance.fields.get(
                name="bezeichnung-override"
            ).value

            return (
                description_overwrite
                or obj.instance.fields.get(name="bezeichnung").value
            )
        except ObjectDoesNotExist:
            return ""

    included_serializers = {"instance": "camac.instance.serializers.InstanceSerializer"}

    @transaction.atomic
    def update(self, instance, validated_data):
        if not instance.is_published and validated_data["is_published"]:

            models.WorkflowEntry.objects.create(
                group=instance.instance.group.pk,
                workflow_item_id=settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get(
                    "PUBLICATION"
                ),
                instance_id=instance.instance.pk,
                # remove the microseconds because this date is displayed in camac and
                # camac can't handle microseconds..
                workflow_date=instance.publication_date.replace(microsecond=0),
            )

            work_item = self.instance.instance.case.work_items.filter(
                task_id="publication", status=workflow_models.WorkItem.STATUS_READY
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
        fields = (
            "instance",
            "publication_date",
            "publication_end_date",
            "is_published",
            "description",
        )
        read_only_fields = ("description",)


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Authority
        fields = ("authority_id", "name")


class WorkflowEntrySerializer(serializers.ModelSerializer):
    workflow_item = relations.ResourceRelatedField(queryset=models.WorkflowItem.objects)

    class Meta:
        model = models.WorkflowEntry
        fields = (
            "workflow_entry_id",
            "workflow_date",
            "instance",
            "workflow_item",
            "group",
        )


class ResourceSerializer(serializers.ModelSerializer, MultilingualSerializer):
    description = MultilingualField()
    link = serializers.SerializerMethodField()

    def get_link(self, obj):
        resource_type = obj.available_resource_id

        if resource_type == "page":
            type_mapping = {
                "/dashboard/faq.phtml": "faq",
                "/dashboard/help.phtml": "help",
                "/dashboard/news.phtml": "news",
            }
            return f"/dashboard/{type_mapping.get(obj.template)}"

        if resource_type == "emberlist":
            instance_states = models.REmberList.objects.get(
                pk=obj.pk
            ).instance_states.split(",")
            return f"/cases?instance_states={instance_states}"

        if resource_type == "workitemlistall":
            return "/work-items"

        return None

    class Meta:
        model = models.Resource
        fields = (
            "name",
            "description",
            "template",
            "class_field",
            "link",
        )


class InstanceResourceSerializer(serializers.ModelSerializer, MultilingualSerializer):
    description = MultilingualField()
    link = serializers.SerializerMethodField()

    def get_link(self, obj):
        ir_type = obj.available_instance_resource_id

        if ir_type == "workitemlistinstance":
            return "work-items"

        if ir_type == "history":
            return "history"

        if ir_type == "page":
            type_mapping = {
                "/ember/instance.phtml": "form",
                "/ember-camac-ng/journal.phtml": "journal",
            }
            return type_mapping.get(obj.template)

        return None

    class Meta:
        model = models.InstanceResource
        fields = (
            "resource",
            "name",
            "description",
            "template",
            "class_field",
            "form_group",
            "link",
        )
