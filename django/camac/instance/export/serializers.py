import csv
import datetime
from collections import OrderedDict

from dateutil.parser import parse as dateutil_parse
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import serializers

from camac.utils import clean_join


class SubmitDateField(serializers.DateField):
    """Custom date field that can parse a string value to a proper date."""

    def to_representation(self, value):
        if not value:  # pragma: no cover
            return None

        if not isinstance(value, datetime.datetime):
            value = dateutil_parse(value)

        return super().to_representation(value.date())


class InstanceExportListSerializer(serializers.ListSerializer):
    """Custom list serializer that prepends a row of field labels to the data."""

    def to_representation(self, data):
        header = [field.label for field in self.child.fields.values()]
        rows = [list(row.values()) for row in super().to_representation(data)]

        return [header] + rows


class InstanceExportSerializer(serializers.Serializer):
    responsible_user = serializers.CharField(label=_("Responsible"))
    inquiry_in_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Arrival Department"),
    )
    inquiry_out_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Departure Department"),
    )
    inquiry_answer = serializers.CharField(label=_("Assessment"))
    involved_services = serializers.CharField(label=_("Involved Departments"))

    def get_fields(self):
        """Make sure fields are ordered by the `Meta.fields` property if given."""

        declared_fields = super().get_fields()
        field_names = getattr(self.Meta, "fields", None)

        if not field_names:  # pragma: no cover
            return declared_fields

        fields = OrderedDict()

        for field_name in field_names:
            assert field_name in declared_fields, (
                f"The field '{field_name}' was declared in the 'fields' option "
                "but is not included on the serializer "
                f"'{self.__class__.__name__}'."
            )

            fields[field_name] = declared_fields[field_name]

        return fields

    class Meta:
        list_serializer_class = InstanceExportListSerializer


class InstanceExportSerializerBE(InstanceExportSerializer):
    ebau_number = serializers.CharField(
        source="case.meta.ebau-number",
        default=None,
        label=_("eBau number"),
    )
    dossier_number = serializers.IntegerField(source="pk", label=_("Instance number"))
    form_name = serializers.CharField(
        source="case.document.form.name",
        label=_("Application Type"),
    )
    address = serializers.CharField(label=_("Address"))
    parcels = serializers.CharField(label=_("Parcels"))
    submit_date = SubmitDateField(
        source="case.meta.submit-date",
        default=None,
        format=settings.SHORT_DATE_FORMAT,
        label=_("Submission Date"),
    )
    instance_state_name = serializers.CharField(label=_("Status"))
    applicants = serializers.CharField(label=_("Applicant"))
    applicants_emails = serializers.CharField(label=_("Applicants emails"))
    municipality = serializers.CharField(label=_("Municipality"))
    district = serializers.SerializerMethodField(label=_("Administrative District"))
    region = serializers.SerializerMethodField(label=_("Administrative Region"))
    in_rsta_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Arrival RSTA"),
    )
    decision_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Decision"),
    )
    sb1_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("SB1 submission date"),
    )
    sb2_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("SB2 submission date"),
    )
    tags = serializers.CharField(source="tag_names", label=_("Tags"))
    building_project = serializers.CharField(label=_("Building project"))

    def load_municipality_sheet(self):
        reader = csv.DictReader(
            open(settings.APPLICATION.get("MUNICIPALITY_DATA_SHEET"))
        )

        return {
            row["Gemeinde"]: {
                key: row[key] for key in ["Verwaltungskreis", "Verwaltungsregion"]
            }
            for row in reader
        }

    @property
    def municipality_sheet(self):
        return cache.get_or_set(
            "municipality_sheet", lambda: self.load_municipality_sheet(), timeout=None
        )

    def get_district(self, instance):
        return self.municipality_sheet.get(instance.municipality, {}).get(
            "Verwaltungskreis", ""
        )

    def get_region(self, instance):
        return self.municipality_sheet.get(instance.municipality, {}).get(
            "Verwaltungsregion", ""
        )

    class Meta(InstanceExportSerializer.Meta):
        # Define order of the fields
        fields = (
            "ebau_number",
            "dossier_number",
            "form_name",
            "address",
            "parcels",
            "building_project",
            "submit_date",
            "instance_state_name",
            "responsible_user",
            "applicants",
            "applicants_emails",
            "municipality",
            "district",
            "region",
            "in_rsta_date",
            "inquiry_in_date",
            "inquiry_out_date",
            "decision_date",
            "sb1_date",
            "sb2_date",
            "inquiry_answer",
            "involved_services",
            "tags",
        )


class InstanceExportSerializerSZ(InstanceExportSerializer):
    dossier_number = serializers.CharField(
        source="identifier", label=_("Instance number")
    )
    form_name = serializers.CharField(
        source="form.description",
        label=_("Building permit type"),
    )
    municipality = serializers.CharField(
        source="location.name", label=_("Lead authority")
    )
    applicants = serializers.SerializerMethodField(label=_("Builder"))
    intent = serializers.CharField(label=_("Intent"))
    address = serializers.CharField(label=_("Address"))
    instance_state_name = serializers.CharField(
        source="instance_state.description", label=_("Status")
    )
    submit_date = SubmitDateField(
        default=None,
        format=settings.SHORT_DATE_FORMAT,
        label=_("Submission Date"),
    )
    inquiry_answer = serializers.CharField(label=_("Inquiry Assessment"))
    decision_date_communal = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Decision Date Communal"),
    )
    decision_date_cantonal = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Decision Date Cantonal"),
    )

    def get_applicants(self, instance):
        def answer(applicant, key):
            # Check for missing keys and None values (imported instances)
            value = applicant.get(key) or ""
            return value.strip()

        return clean_join(
            *[
                (
                    answer(applicant, "firma")
                    if answer(applicant, "firma")
                    else clean_join(
                        answer(applicant, "vorname"),
                        answer(applicant, "name"),
                    )
                )
                for applicant in instance.applicants
            ],
            separator=", ",
        )

    class Meta(InstanceExportSerializer.Meta):
        # Define order of the fields
        fields = (
            "dossier_number",
            "form_name",
            "municipality",
            "applicants",
            "intent",
            "address",
            "instance_state_name",
            "responsible_user",
            "submit_date",
            "inquiry_in_date",
            "inquiry_out_date",
            "inquiry_answer",
            # "involved_services",
            "decision_date_communal",
            "decision_date_cantonal",
        )
