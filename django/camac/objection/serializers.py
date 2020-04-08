from django.utils.translation import gettext as _
from drf_extra_fields.fields import DateTimeRangeField
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
    timeframe = DateTimeRangeField()

    included_serializers = {"instance": "camac.instance.serializers.InstanceSerializer"}

    class Meta:
        model = models.ObjectionTimeframe
        fields = ("instance", "timeframe")
