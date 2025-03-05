from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_noop
from rest_framework_json_api.serializers import ModelSerializer

from camac.core.utils import create_history_entry
from camac.sanctions.models import Sanction, SanctionTemplate
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import (
    CurrentServiceDefault,
    ServiceSerializer,
    UserSerializer,
)


class SanctionSerializer(ModelSerializer):
    created_by_service = ServiceResourceRelatedField(default=CurrentServiceDefault())
    created_by_user = CurrentUserResourceRelatedField()
    included_serializers = {
        "created_by_service": ServiceSerializer,
        "assigned_service": ServiceSerializer,
        "controlled_by_user": UserSerializer,
    }

    class Meta:
        model = Sanction
        read_only_fields = (
            "created_at",
            "created_by_service",
            "created_by_user",
            "controlled_at",
            "controlled_by_user",
            "control_notes",
        )
        fields = read_only_fields + (
            "instance",
            "name",
            "description",
            "assigned_service",
            "control_step",
        )


class SanctionControlSerializer(ModelSerializer):
    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data["controlled_at"] = timezone.now()
        validated_data["controlled_by_user"] = self.context["request"].user

        create_history_entry(
            instance.instance,
            self.context["request"].user,
            gettext_noop("Sanction '%(sanction_name)s' has been controlled."),
            lambda _: {"sanction_name": instance.name},
        )

        return super().update(instance, validated_data)

    class Meta:
        model = Sanction
        fields = ("control_notes",)


class SanctionTemplateSerializer(ModelSerializer):
    created_by_service = ServiceResourceRelatedField(default=CurrentServiceDefault())
    created_by_user = CurrentUserResourceRelatedField()
    included_serializers = {
        "created_by_service": ServiceSerializer,
        "assigned_service": ServiceSerializer,
    }

    class Meta:
        model = SanctionTemplate
        read_only_fields = ("created_at", "created_by_service", "created_by_user")
        fields = read_only_fields + (
            "name",
            "description",
            "assigned_service",
            "control_step",
        )
