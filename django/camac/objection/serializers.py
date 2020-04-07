from django.db import transaction
from django.utils.translation import gettext as _
from psycopg2.extras import DateTimeTZRange
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin

from . import models


class ObjectionParticipantSerializer(serializers.ModelSerializer):
    representative = serializers.BooleanField()
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, data):
        representative_filter = data["objection"].objection_participants.filter(
            representative=1
        )

        if (
            "representative" in data
            and data["representative"]
            and (
                # Check if its updating an existing representative
                (
                    self.instance
                    and representative_filter.exists()
                    and representative_filter.first().pk != self.instance.id
                )
                # Check if its creating a duplicate representative
                or (not self.instance and representative_filter.exists())
            )
        ):
            raise ValidationError(
                _("Objection %(objection) already has a representative")
                % {"objection": data["objection"].pk}
            )

        return data

    class Meta:
        model = models.ObjectionParticipant
        fields = (
            "objection",
            "name",
            "company",
            "email",
            "address",
            "city",
            "phone",
            "representative",
        )


class ObjectionSerializer(serializers.ModelSerializer, InstanceEditableMixin):
    creation_date = serializers.DateField()

    included_serializers = {
        "instance": "camac.instance.serializers.InstanceSerializer",
        "objection_participants": ObjectionParticipantSerializer,
    }

    class Meta:
        model = models.Objection
        fields = ("instance", "creation_date", "objection_participants")


class ObjectionTimeframeSerializer(serializers.ModelSerializer, InstanceEditableMixin):
    start_date = serializers.DateTimeField(required=False, write_only=True)
    end_date = serializers.DateTimeField(write_only=True)

    included_serializers = {"instance": "camac.instance.serializers.InstanceSerializer"}

    @transaction.atomic
    def create(self, validated_data):
        validated_data["timeframe"] = DateTimeTZRange(
            validated_data.get("start_date", None), validated_data["end_date"]
        )
        del validated_data["end_date"]
        if "start_date" in validated_data:
            del validated_data["start_date"]

        timeframe = super().create(validated_data)

        return timeframe

    @transaction.atomic
    def update(self, timeframe, validated_data):
        validated_data["timeframe"] = DateTimeTZRange(
            validated_data.get("start_date", None), validated_data["end_date"]
        )
        del validated_data["end_date"]
        if "start_date" in validated_data:
            del validated_data["start_date"]

        timeframe = super().update(timeframe, validated_data)

        return timeframe

    class Meta:
        model = models.ObjectionTimeframe
        fields = ("instance", "start_date", "end_date", "timeframe")
        read_only_fields = ("timeframe",)
