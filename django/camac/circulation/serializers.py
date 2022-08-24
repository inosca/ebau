from rest_framework_json_api import serializers

from camac.core.models import Activation, Circulation
from camac.user.serializers import ServiceSerializer


class CirculationSerializer(serializers.ModelSerializer):
    included_serializers = {
        "instance": "camac.instance.serializers.InstanceSerializer",
        "activations": "camac.circulation.serializers.ActivationSerializer",
    }

    class Meta:
        model = Circulation
        fields = ("name", "instance", "activations")


class ActivationSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    """
    Simplify circulation_state as it is currently only read and
    only the name is important. This way we can avoid another api endpoint
    and simply json api structure.
    """

    included_serializers = {
        "circulation": CirculationSerializer,
        "service": ServiceSerializer,
    }

    def get_state(self, activation):
        return activation.circulation_state.name

    class Meta:
        model = Activation
        fields = (
            "circulation",
            "deadline_date",
            "end_date",
            "suspension_date",
            "service",
            "state",
            "reason",
        )
