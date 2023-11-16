from decimal import Decimal

from rest_framework_json_api import serializers

from camac.billing.models import BillingV2Entry
from camac.billing.utils import (
    add_taxes_to_final_rate,
    calculate_final_rate,
    get_totals,
)
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    GroupResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault


class BillingV2EntrySerializer(serializers.ModelSerializer):
    user = CurrentUserResourceRelatedField()
    group = GroupResourceRelatedField(default=CurrentGroupDefault())
    tax_rate = serializers.ChoiceField(choices=[0, 2.5, 2.6, 7.7, 8.1])

    included_serializers = {
        "user": "camac.user.serializers.UserSerializer",
        "group": "camac.user.serializers.GroupSerializer",
    }

    def validate(self, data):
        validated_data = super().validate(data)

        validated_data["final_rate"] = add_taxes_to_final_rate(
            calculate_final_rate(
                calculation=validated_data["calculation"],
                total_cost=validated_data.get("total_cost"),
                percentage=validated_data.get("percentage"),
                hours=validated_data.get("hours"),
                hourly_rate=validated_data.get("hourly_rate"),
            ),
            tax_mode=validated_data["tax_mode"],
            tax_rate=Decimal(validated_data["tax_rate"]),
        )

        return validated_data

    def get_root_meta(self, resource, many):
        """Calculate totals for the returned data.

        Warning: If paginated, this will return the totals of the paginated
        subset - not of all records in the unpaginated queryset.
        """

        if many:
            return {"totals": get_totals(resource)}

        return {}

    class Meta:
        model = BillingV2Entry
        fields = (
            "calculation",
            "date_added",
            "date_charged",
            "final_rate",
            "group",
            "hourly_rate",
            "hours",
            "instance",
            "organization",
            "percentage",
            "tax_mode",
            "tax_rate",
            "text",
            "total_cost",
            "user",
        )
        read_only_fields = (
            "date_added",
            "date_charged",
            "final_rate",
            "group",
            "user",
        )
