from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin

from . import models


class ObjectionParticipantSerializer(serializers.ModelSerializer):
    representative = serializers.BooleanField()
    email = serializers.EmailField()

    def validate(self, data):
        print(data)
        if (
            "representative" in data
            and data["representative"]
            and data["objection"]
            .objection_participants.filter(representative=1)
            .exists()
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
