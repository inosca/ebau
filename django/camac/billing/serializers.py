from decimal import Decimal

from django.conf import settings
from django.utils.translation import gettext as _
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

        Warning: This will calculate the totals for the whole filtered queryset
        data. Every paginated request will include the totals for all un-paginated
        results.
        """

        if many:
            view = self.context.get("view")
            filtered_results = view.filter_queryset(view.get_queryset())
            ordered = list(filtered_results.values())

            return {"totals": get_totals(ordered)}

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
            "billing_type",
            "cost_center",
            "legal_basis",
        )
        read_only_fields = (
            "date_added",
            "date_charged",
            "final_rate",
            "group",
            "user",
        )


class BillingV2EntryExportSerializer(BillingV2EntrySerializer):
    date_added = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT, label=_("Date added")
    )
    text = serializers.CharField(label=_("Position"))
    group = serializers.CharField(label=_("Group"))
    user = serializers.CharField(label=_("User"))
    calculation_of_final_rate = serializers.SerializerMethodField(
        label=_("Final Rate (CHF)")
    )
    final_rate = serializers.CharField(label=_("Total (CHF)"))
    ebau_number = serializers.CharField(
        source="instance.case.meta.ebau-number",
        default=None,
        label=_("eBau number"),
    )
    dossier_number = serializers.IntegerField(
        source="instance_id", label=_("Instance number")
    )
    address = serializers.CharField(label=_("Address"))
    parcels = serializers.CharField(label=_("Parcels"))
    coordinates = serializers.SerializerMethodField(label=_("Coordinates"))
    lead_authority = serializers.SerializerMethodField(label=_("Lead authority"))

    def get_calculation_of_final_rate(self, model):
        _tax_mode = (
            _("inclusive")
            if model.tax_mode == BillingV2Entry.TAX_MODE_INCLUSIVE
            else _("exclusive")
        )
        tax = (
            _("%(tax_mode)s  %(tax_rate)s%% VAT")
            % {
                "tax_mode": _tax_mode,
                "tax_rate": model.tax_rate.quantize(Decimal("0.1")),
            }
            if model.tax_mode != BillingV2Entry.TAX_MODE_EXEMPT
            else _("not subject to VAT")
        )

        if model.calculation == BillingV2Entry.CALCULATION_HOURLY:  # hourly
            return _("%(hours)s hours at %(hourly_rate)s %(tax)s") % {
                "hours": model.hours,
                "hourly_rate": model.hourly_rate,
                "tax": tax,
            }

        if model.calculation == BillingV2Entry.CALCULATION_PERCENTAGE:  # percentage
            return _("%(percentage)s of %(total)s %(tax-suffix)s") % {
                "percentage": model.percentage,
                "total": model.total_cost,
                "tax-suffix": tax,
            }

        # model.calculation == BillingV2Entry.CALCULATION_FLAT  # flat
        return f"{model.final_rate} {tax}"

    def get_lead_authority(self, model):
        service = model.instance.responsible_service()
        city = service.get_trans_attr("city")
        return ", ".join(
            str(attr)
            for attr in [service.get_name(), service.address, service.zip, city]
            if attr is not None
        )

    def get_coordinates(self, model):
        if not model.coordinate_X or not model.coordinate_Y:
            return _("No coordinates available")
        else:
            all_x = [val.strip() for val in model.coordinate_X.split(",")]
            all_y = [val.strip() for val in model.coordinate_Y.split(",")]
            coordinates = zip(all_x, all_y)
            coordinates_str = ", ".join([f"{x}/{y}" for x, y in coordinates])
            return coordinates_str

    class Meta:
        model = BillingV2Entry
        # Define order of the fields
        fields = (
            "date_added",
            "text",
            "group",
            "user",
            "calculation_of_final_rate",
            "final_rate",
            "ebau_number",
            "dossier_number",
            "address",
            "parcels",
            "coordinates",
            "lead_authority",
        )
        read_only_fields = (
            "date_added",
            "text",
            "group",
            "user",
            "calculation_of_final_rate",
            "final_rate",
            "ebau_number",
            "dossier_number",
            "address",
            "parcels",
            "coordinates",
            "lead_authority",
        )
