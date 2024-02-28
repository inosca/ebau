import csv
import itertools
import json
from collections import OrderedDict

from caluma.caluma_form.models import Answer
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import get_language, gettext_noop as _
from rest_framework import serializers

from camac.caluma.api import CalumaApi
from camac.core.translations import get_translations_canton_aware
from camac.user.models import Service
from camac.utils import build_url, clean_join

from ..master_data import MasterData
from . import fields
from .utils import get_option_label, human_readable_date


def sanitize_value(value):
    return value if value is not None else ""


class DMSPlaceholdersSerializer(serializers.Serializer):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)

        instance._master_data = MasterData(instance.case)

    def get_aliased_collection(self, collection):
        return OrderedDict(
            sorted(
                itertools.chain(
                    *[
                        self.get_aliased_field(key, sanitize_value(value))
                        for key, value in collection.items()
                    ]
                )
            )
        )

    def get_aliased_field(self, key, value):
        field = self.fields[key]
        keys = {key.upper()}

        for alias_config in field.aliases:
            for alias in get_translations_canton_aware(alias_config).values():
                keys.add(alias.upper())

        if field.nested_aliases:
            value = self.get_aliased_value(value, field.nested_aliases)

        return [(name, value) for name in keys]

    def get_aliased_value(self, value, aliases):
        parsed_aliases = {
            key: list(
                itertools.chain(
                    *[
                        get_translations_canton_aware(alias).values()
                        for alias in alias_config
                    ]
                )
            )
            for key, alias_config in aliases.items()
        }

        return [self.get_aliased_value_item(item, parsed_aliases) for item in value]

    def get_aliased_value_item(self, item, aliases):
        parsed_item = {}

        for key, value in item.items():
            value = sanitize_value(value)

            if key not in aliases[key]:
                parsed_item[key] = value

            for alias in aliases[key]:
                parsed_item[alias] = value

        return parsed_item

    def to_representation(self, instance):
        return self.get_aliased_collection(super().to_representation(instance))

    @property
    def _readable_fields(self):
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.exclude:
                yield field

    address = fields.JointField(
        fields=[
            fields.JointField(
                fields=[
                    fields.MasterDataField(source="street"),
                    fields.MasterDataField(source="street_number"),
                ]
            ),
            fields.JointField(
                fields=[
                    fields.MasterDataField(source="zip"),
                    fields.MasterDataField(source="city"),
                ]
            ),
        ],
        separator=", ",
        aliases=[_("ADDRESS")],
        description=_("Address of the concerned property"),
    )
    alle_gesuchsteller_name_address = fields.MasterDataPersonField(
        source="applicants",
        fields="__all__",
        aliases=[
            {
                "default": _("ALL_APPLICANTS_NAME_ADDRESS"),
                "so": _("ALL_BUILDERS_NAME_ADDRESS"),
            }
        ],
        description={
            "default": _("Names and addresses of all applicants"),
            "so": _("Names and addresses of all builders"),
        },
    )
    alle_gesuchsteller = fields.MasterDataPersonField(
        source="applicants",
        aliases=[
            {
                "default": _("ALL_APPLICANTS"),
                "so": _("ALL_BUILDERS"),
            }
        ],
        description={
            "default": _("Names of all applicants"),
            "so": _("Names of all builders"),
        },
    )
    alle_grundeigentuemer_name_address = fields.MasterDataPersonField(
        source="landowners",
        fields="__all__",
        aliases=[_("ALL_LANDOWNERS_NAME_ADDRESS")],
        description=_("Names and addresses of all landowners"),
    )
    alle_grundeigentuemer = fields.MasterDataPersonField(
        source="landowners",
        aliases=[_("ALL_LANDOWNERS")],
        description=_("Names of all landowners"),
    )
    alle_projektverfasser_name_address = fields.MasterDataPersonField(
        source="project_authors",
        fields="__all__",
        aliases=[_("ALL_PROJECT_AUTHORS_NAME_ADDRESS")],
        description=_("Names and addresses of all project authors"),
    )
    alle_projektverfasser = fields.MasterDataPersonField(
        source="project_authors",
        aliases=[_("ALL_PROJECT_AUTHORS")],
        description=_("Names of all project authors"),
    )
    base_url = fields.AliasedMethodField(
        aliases=[_("BASE_URL")],
        description=_("The URL of the eBau system"),
    )
    baueingabe_datum = fields.MasterDataField(
        source="submit_date",
        parser=human_readable_date,
        aliases=[_("SUBMIT_DATE")],
        description=_("Date on which the instance was submitted"),
    )
    beschreibung_bauvorhaben = fields.MasterDataField(
        source="proposal",
        aliases=[_("PROPOSAL")],
        description=_("Description of the project"),
    )
    decision_date = fields.DecisionField(
        source="decision-date",
        aliases=[_("DECISION_DATE")],
        description=_("Decision date"),
    )
    description_modification = fields.MasterDataField(
        "description_modification",
        aliases=[_("DESCRIPTION_MODIFICATION")],
        description=_("Project modification"),
    )
    fachstellen_kantonal = fields.InquiriesField(
        aliases=[_("CIRCULATION_ALL"), _("SERVICES_CANTONAL")],
        description=_("Involved organisations of the instance"),
    )
    form_name = fields.AliasedMethodField(
        aliases=[_("FORM_NAME")],
        description=_("Type of the instance"),
    )
    gemeinde_email = fields.MunicipalityField(
        source="email",
        aliases=[_("MUNICIPALITY_EMAIL")],
        description=_("Email address of the municipality"),
    )
    gemeinde_name_adresse = fields.JointField(
        fields=[
            fields.MunicipalityField(
                source="get_name", remove_name_prefix=True, add_municipality_prefix=True
            ),
            fields.MunicipalityField(source="address"),
            fields.JointField(
                fields=[
                    fields.MunicipalityField(source="zip"),
                    fields.MunicipalityField(
                        source="get_trans_attr", source_args=["city"]
                    ),
                ]
            ),
        ],
        separator=", ",
        aliases=[_("MUNICIPALITY_NAME_ADDRESS")],
        description=_("Name and address of the municipality"),
    )
    gemeinde_ort = fields.MunicipalityField(
        source="get_trans_attr",
        source_args=["city"],
        aliases=[_("MUNICIPALITY_CITY")],
        description=_("City of the municipality"),
    )
    gemeinde_telefon = fields.MunicipalityField(
        source="phone",
        aliases=[_("MUNICIPALITY_PHONE")],
        description=_("Phone of the municipality"),
    )
    gemeinde_webseite = fields.MunicipalityField(
        source="website",
        aliases=[_("MUNICIPALITY_WEBSITE")],
        description=_("Website of the municipality"),
    )
    gesuchsteller_address_1 = fields.MasterDataPersonField(
        source="applicants",
        only_first=True,
        fields=["address_1"],
        aliases=[
            {
                "default": _("APPLICANT_ADDRESS_1"),
                "so": _("BUILDER_ADDRESS_1"),
            }
        ],
        description={
            "default": _("Address line 1 of the first applicant"),
            "so": _("Address line 1 of the first builder"),
        },
    )
    gesuchsteller_address_2 = fields.MasterDataPersonField(
        source="applicants",
        only_first=True,
        fields=["address_2"],
        aliases=[
            {
                "default": _("APPLICANT_ADDRESS_2"),
                "so": _("BUILDER_ADDRESS_2"),
            }
        ],
        description={
            "default": _("Address line 2 of the first applicant"),
            "so": _("Address line 2 of the first builder"),
        },
    )
    gesuchsteller_name_address = fields.MasterDataPersonField(
        source="applicants",
        only_first=True,
        fields="__all__",
        aliases=[
            {
                "default": _("APPLICANT_NAME_ADDRESS"),
                "so": _("BUILDER_NAME_ADDRESS"),
            }
        ],
        description={
            "default": _("Name and address of the applicant"),
            "so": _("Name and address of the builder"),
        },
    )
    gesuchsteller = fields.MasterDataPersonField(
        source="applicants",
        only_first=True,
        aliases=[
            {
                "default": _("APPLICANT"),
                "so": _("BUILDER"),
            }
        ],
        description={
            "default": _("Name of the applicant"),
            "so": _("Name of the builder"),
        },
    )
    grundeigentuemer_address_1 = fields.MasterDataPersonField(
        source="landowners",
        only_first=True,
        fields=["address_1"],
        aliases=[_("LANDOWNER_ADDRESS_1")],
        description=_("Address line 1 of the first landowner"),
    )
    grundeigentuemer_address_2 = fields.MasterDataPersonField(
        source="landowners",
        only_first=True,
        fields=["address_2"],
        aliases=[_("LANDOWNER_ADDRESS_2")],
        description=_("Address line 2 of the first landowner"),
    )
    grundeigentuemer_name_address = fields.MasterDataPersonField(
        source="landowners",
        only_first=True,
        fields="__all__",
        aliases=[_("LANDOWNER_NAME_ADDRESS")],
        description=_("Name and address of the landowner"),
    )
    grundeigentuemer = fields.MasterDataPersonField(
        source="landowners",
        only_first=True,
        aliases=[_("LANDOWNER")],
        description=_("Name of the landowner"),
    )
    juristic_name = fields.MasterDataPersonField(
        source="applicants",
        only_first=True,
        fields=["juristic_name"],
        aliases=[_("JURISTIC_NAME")],
        description={
            "default": _("Juristic name of the applicant"),
            "so": _("Juristic name of the builder"),
        },
    )
    koordinaten = fields.AliasedMethodField(
        aliases=[_("COORDINATES")],
        description=_("Coordinates of the parcel"),
    )
    language = fields.AliasedMethodField(
        aliases=[_("LANGUAGE")],
        description=_("Currently selected language"),
    )
    leitbehoerde_address_1 = fields.ResponsibleServiceField(
        source="address",
        aliases=[_("AUTHORITY_ADDRESS_1")],
        description=_("Address line 1 of the authority"),
    )
    leitbehoerde_address_2 = fields.JointField(
        fields=[
            fields.ResponsibleServiceField(source="zip"),
            fields.ResponsibleServiceField(
                source="get_trans_attr",
                source_args=["city"],
            ),
        ],
        aliases=[_("AUTHORITY_ADDRESS_2")],
        description=_("Address line 2 of the authority"),
    )
    leitbehoerde_name_adresse = fields.JointField(
        fields=[
            fields.ResponsibleServiceField(source="get_name"),
            fields.ResponsibleServiceField(source="address"),
            fields.JointField(
                fields=[
                    fields.ResponsibleServiceField(source="zip"),
                    fields.ResponsibleServiceField(
                        source="get_trans_attr", source_args=["city"]
                    ),
                ]
            ),
        ],
        separator=", ",
        aliases=[_("AUTHORITY_NAME_ADDRESS")],
        description=_("Name and address of the authority"),
    )
    leitbehoerde_city = fields.ResponsibleServiceField(
        source="get_trans_attr",
        source_args=["city"],
        aliases=[_("AUTHORITY_CITY")],
        description=_("City of the authority"),
    )
    leitbehoerde_email = fields.ResponsibleServiceField(
        source="email",
        aliases=[_("AUTHORITY_EMAIL")],
        description=_("Email address of the authority"),
    )
    leitbehoerde_name_kurz = fields.ResponsibleServiceField(
        source="get_name",
        remove_name_prefix=True,
        aliases=[_("AUTHORITY_NAME_SHORT")],
        description=_("Short name of the authority"),
    )
    leitbehoerde_name = fields.ResponsibleServiceField(
        source="get_name",
        aliases=[_("AUTHORITY_NAME")],
        description=_("Name of the authority"),
    )
    leitbehoerde_phone = fields.ResponsibleServiceField(
        source="phone",
        aliases=[_("AUTHORITY_PHONE")],
        description=_("Phone of the authority"),
    )
    leitbehoerde_webseite = fields.ResponsibleServiceField(
        source="website",
        aliases=[_("AUTHORITY_WEBSITE")],
        description=_("Website of the authority"),
    )
    meine_organisation_adresse_1 = fields.CurrentServiceField(
        source="address",
        aliases=[_("CURRENT_SERVICE_ADDRESS_1")],
        description=_("Address line 1 of the current service"),
    )
    meine_organisation_adresse_2 = fields.JointField(
        fields=[
            fields.CurrentServiceField(source="zip"),
            fields.CurrentServiceField(source="get_trans_attr", source_args=["city"]),
        ],
        aliases=[_("CURRENT_SERVICE_ADDRESS_2")],
        description=_("Address line 2 of the current service"),
    )
    meine_organisation_email = fields.CurrentServiceField(
        source="email",
        aliases=[_("CURRENT_SERVICE_EMAIL")],
        description=_("Email address of the current service"),
    )
    meine_organisation_name_adresse = fields.JointField(
        fields=[
            fields.CurrentServiceField(source="get_name"),
            fields.CurrentServiceField(source="address"),
            fields.JointField(
                fields=[
                    fields.CurrentServiceField(source="zip"),
                    fields.CurrentServiceField(
                        source="get_trans_attr", source_args=["city"]
                    ),
                ]
            ),
        ],
        separator=", ",
        aliases=[_("CURRENT_SERVICE_NAME_ADDRESS")],
        description=_("Name and address of the current service"),
    )
    meine_organisation_name_kurz = fields.CurrentServiceField(
        source="get_name",
        remove_name_prefix=True,
        aliases=[_("CURRENT_SERVICE_NAME_SHORT")],
        description=_("Short name of the current service"),
    )
    meine_organisation_name = fields.CurrentServiceField(
        source="get_name",
        aliases=[_("CURRENT_SERVICE_NAME")],
        description=_("Name of the current service"),
    )
    meine_organisation_ort = fields.CurrentServiceField(
        source="get_trans_attr",
        source_args=["city"],
        aliases=[_("CURRENT_SERVICE_CITY")],
        description=_("City of the current service"),
    )
    meine_organisation_telefon = fields.CurrentServiceField(
        source="phone",
        aliases=[_("CURRENT_SERVICE_PHONE")],
        description=_("Phone of the current service"),
    )
    meine_organisation_webseite = fields.CurrentServiceField(
        source="website",
        aliases=[_("CURRENT_SERVICE_WEBSITE")],
        description=_("Website of the current service"),
    )
    municipality_address = fields.JointField(
        fields=[
            fields.MunicipalityField(source="address"),
            fields.JointField(
                fields=[
                    fields.MunicipalityField(source="zip"),
                    fields.MunicipalityField(
                        source="get_trans_attr", source_args=["city"]
                    ),
                ]
            ),
        ],
        separator=", ",
        aliases=[_("MUNICIPALITY_ADDRESS")],
        description={
            "default": _("Address of the municipality selected by the applicant"),
            "so": _("Address of the municipality selected by the builder"),
        },
    )
    municipality = fields.MunicipalityField(
        source="get_name",
        remove_name_prefix=True,
        aliases=[_("MUNICIPALITY")],
        description={
            "default": _("Name of the municipality selected by the applicant"),
            "so": _("Name of the municipality selected by the builder"),
        },
    )
    name = fields.DeprecatedField()
    nebenbestimmungen_mapped = fields.InquiriesField(
        only_own=True,
        props=[("service", "FACHSTELLE"), ("ancillary_clauses", "TEXT")],
        aliases=[_("ANCILLARY_CLAUSES_MAPPED")],
    )
    nebenbestimmungen = fields.InquiriesField(
        only_own=True,
        props=["ancillary_clauses"],
        join_by="\n\n",
        aliases=[_("OWN_ANCILLARY_CLAUSES"), _("ANCILLARY_CLAUSES")],
        description=_("Own ancillary clauses"),
    )
    ort = fields.MasterDataField(
        source="city",
        aliases=[_("LOCATION")],
        description=_("The location of the building site"),
    )
    parzelle = fields.AliasedMethodField(
        aliases=[_("PARCEL")],
        description={
            "default": _("Parcel selected by the applicant"),
            "so": _("Parcel selected by the builder"),
        },
    )
    projektverfasser_address_1 = fields.MasterDataPersonField(
        source="project_authors",
        only_first=True,
        fields=["address_1"],
        aliases=[_("PROJECT_AUTHOR_ADDRESS_1")],
        description=_("Address line 1 of the first project author"),
    )
    projektverfasser_address_2 = fields.MasterDataPersonField(
        source="project_authors",
        only_first=True,
        fields=["address_2"],
        aliases=[_("PROJECT_AUTHOR_ADDRESS_2")],
        description=_("Address line 2 of the first project author"),
    )
    projektverfasser_name_address = fields.MasterDataPersonField(
        source="project_authors",
        only_first=True,
        fields="__all__",
        aliases=[_("PROJECT_AUTHOR_NAME_ADDRESS")],
        description=_("Name and addresse of the project author"),
    )
    projektverfasser = fields.MasterDataPersonField(
        source="project_authors",
        only_first=True,
        aliases=[_("PROJECT_AUTHOR")],
        description=_("Name of the project author"),
    )
    publikation_link = fields.AliasedMethodField(
        aliases=[_("PUBLICATION_LINK")],
        description=_("Link to publication"),
    )
    publikation_text = fields.PublicationField(
        source="publikation-text",
        aliases=[_("PUBLICATION_TEXT")],
        description=_("Publication text of the instance"),
    )
    status = fields.AliasedMethodField(
        aliases=[_("STATUS")],
        description=_("Current status of the instance"),
    )
    stellungnahme = fields.InquiriesField(
        only_own=True,
        props=["opinion"],
        join_by="\n\n",
        aliases=[_("OWN_OPINIONS"), _("OPINIONS")],
        description=_("Own opinions"),
    )
    strasse = fields.MasterDataField(
        source="street",
        aliases=[_("STREET")],
        description=_("The street of the building site"),
    )
    today = fields.AliasedMethodField(
        aliases=[_("TODAY")],
        description=_("Current date"),
    )
    zirkulation_fachstellen = fields.InquiriesField(
        service_group="service",
        aliases=[_("CIRCULATION_SERVICES")],
        description=_("Involved services of the instance"),
    )
    zirkulation_gemeinden = fields.InquiriesField(
        service_group="municipality",
        aliases=[_("CIRCULATION_MUNICIPALITIES")],
        description=_("Involved municipalities of the instance"),
    )
    zirkulation_rueckmeldungen = fields.InquiriesField(
        status=WorkItem.STATUS_COMPLETED,
        props=[
            ("opinion", "STELLUNGNAHME"),
            ("ancillary_clauses", "NEBENBESTIMMUNGEN"),
            ("answer", "ANTWORT"),
            ("service", "VON"),
        ],
        aliases=[_("CIRCULATION_FEEDBACK")],
        description=_("Opinions and ancillary clauses of the invited services"),
    )
    eigene_gebuehren_total = fields.BillingEntriesField(
        own=True,
        total=True,
        aliases=[_("OWN_BILLING_ENTRIES_TOTAL")],
        description=_("Total of all own billing entries of the instance"),
    )
    eigene_gebuehren = fields.BillingEntriesField(
        own=True,
        aliases=[_("OWN_BILLING_ENTRIES")],
        description=_("Own billing entries of the instance"),
    )
    gebuehren_total = fields.BillingEntriesField(
        total=True,
        aliases=[_("BILLING_ENTRIES_TOTAL")],
        description=_("Total of all billing entries of the instance"),
    )
    gebuehren = fields.BillingEntriesField(
        aliases=[_("BILLING_ENTRIES")],
        description=_("Billing entries of the instance"),
    )
    dossier_number = fields.MasterDataField(
        aliases=[_("DOSSIER_NUMBER")],
        description=_("Dossier number of the instance"),
    )
    zustaendig_email = fields.ResponsibleUserField(
        source="email",
        aliases=[_("RESPONSIBLE_EMAIL")],
        description=_("Email address of the responsible employee"),
    )
    zustaendig_name = fields.ResponsibleUserField(
        source="full_name",
        aliases=[_("RESPONSIBLE_NAME")],
        description=_("Name of the responsible employee"),
    )
    zustaendig_phone = fields.ResponsibleUserField(
        source="phone",
        aliases=[_("RESPONSIBLE_PHONE")],
        description=_("Phone of the responsible employee"),
    )

    def get_base_url(self, instance):
        return settings.INTERNAL_BASE_URL

    def get_form_name(self, instance):
        return instance.case.document.form.name.get(get_language())

    def get_koordinaten(self, instance):
        return clean_join(
            *[
                clean_join(
                    *[
                        f"{int(plot.get(key)):,}".replace(",", "’")
                        for key in ["coord_east", "coord_north"]
                        if plot.get(key)
                    ],
                    separator=" / ",
                )
                for plot in instance._master_data.plot_data
            ],
            separator="; ",
        )

    def get_language(self, instance):
        return get_language()

    def get_parzelle(self, instance):
        return clean_join(
            *[plot.get("plot_number") for plot in instance._master_data.plot_data],
            separator=", ",
        )

    def get_publikation_link(self, instance):
        return build_url(settings.PUBLIC_BASE_URL, f"public-instances/{instance.pk}")

    def get_status(self, instance):
        return instance.instance_state.get_name()

    def get_today(self, instance):
        return human_readable_date(now().date())

    class Meta:
        exclude = []


class GrDMSPlaceholdersSerializer(DMSPlaceholdersSerializer):
    instance_id = fields.AliasedIntegerField(
        source="pk",
        aliases=[_("ID")],
        description=_("ID of the instance"),
    )
    bauentscheid = fields.DecisionField(
        source="decision-decision",
        aliases=[_("DECISION")],
        description=_("Decision"),
    )
    beginn_publikationsorgan_gemeinde = fields.PublicationField(
        source="beginn-publikationsorgan-gemeinde",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("START_PUBLICATION_MUNICIPALITY")],
        description=_(
            "Start date of the publication in the publication organ of the municipality"
        ),
    )
    ende_publikationsorgan_gemeinde = fields.PublicationField(
        source="ende-publikationsorgan-gemeinde",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("END_PUBLICATION_MUNICIPALITY")],
        description=_(
            "End date of the publication in the publication organ of the municipality"
        ),
    )
    beginn_publikation_kantonsamtsblatt = fields.PublicationField(
        source="beginn-publikation-kantonsamtsblatt",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("START_PUBLICATION_CANTON")],
        description=_("Start date of the publication in the cantonal Gazette"),
    )
    ende_publikation_kantonsamtsblatt = fields.PublicationField(
        source="ende-publikation-kantonsamtsblatt",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("END_PUBLICATION_CANTON")],
        description=_("End date of the publication in the cantonal Gazette"),
    )
    entscheiddokumente = fields.AlexandriaSimpleDocumentField(
        mark="decision",
        aliases=[_("DECISION_DOCUMENTS")],
        description=_("All documents marked as decision documents"),
    )
    zonenplan = fields.AliasedMethodField(
        aliases=[_("ZONING_PLAN")],
        description=_("Zoning plan"),
    )
    genereller_gestaltungsplan = fields.AliasedMethodField(
        aliases=[_("GENERAL_DESIGN_PLAN")],
        description=_("General design plan"),
    )
    genereller_erschliessungsplan = fields.AliasedMethodField(
        aliases=[_("GENERAL_ACCESS_PLAN")],
        description=_("General access plan"),
    )
    folgeplanung = fields.AliasedMethodField(
        aliases=[_("FOLLOWUP_PLANNING")],
        description=_("Follow-up planning"),
    )
    koordinaten = fields.AliasedMethodField(
        aliases=[_("COORDINATES")],
        description=_("Coordinates of the parcel"),
    )
    gebaeudeversicherungsnummer = fields.AliasedMethodField(
        aliases=[_("BUILDING_INSURANCE_NUMBER")],
        description=_("Building insurance number"),
    )
    documents = fields.AlexandriaDocumentField(
        aliases=[_("DOCUMENTS")],
        description=_("Documents with metadata"),
    )

    def get_zonenplan(self, instance):
        answer = Answer.objects.filter(
            question_id="zonenplan", document_id=instance.case.document.pk
        )
        return answer.first().value if answer else ""

    def get_genereller_gestaltungsplan(self, instance):
        answer = Answer.objects.filter(
            question_id="genereller-gestaltungsplan",
            document_id=instance.case.document.pk,
        )
        return answer.first().value if answer else ""

    def get_genereller_erschliessungsplan(self, instance):
        answer = Answer.objects.filter(
            question_id="genereller-erschliessungsplan",
            document_id=instance.case.document.pk,
        )
        return answer.first().value if answer else ""

    def get_folgeplanung(self, instance):
        answer = Answer.objects.filter(
            question_id="folgeplanung", document_id=instance.case.document.pk
        )
        return answer.first().value if answer else ""

    def get_koordinaten(self, instance):
        coordinates = [
            json.loads(answer.value)["markers"]
            for answer in Answer.objects.filter(
                question_id="gis-map", document_id=instance.case.document.pk
            )
            if answer.value
        ]

        if not coordinates:  # pragma: no cover
            return ""

        data = []
        for coordinate in coordinates[0]:
            x = f"{round(coordinate['x']):_}".replace("_", "’")
            y = f"{round(coordinate['y']):_}".replace("_", "’")
            data.append(f"{x} / {y}")
        return "; ".join(data)

    def get_gebaeudeversicherungsnummer(self, instance):
        values = Answer.objects.filter(
            document__family_id=instance.case.document.pk,
            question_id="amtliche-gebaeudenummer",
        ).values_list("value", flat=True)
        return ", ".join([str(v) for v in values])

    class Meta:
        exclude = [
            "eigene_gebuehren_total",
            "eigene_gebuehren",
            "gebuehren_total",
            "gebuehren",
            "gemeinde_webseite",
            "leitbehoerde_name_adresse",
            "leitbehoerde_webseite",
            "meine_organisation_webseite",
            "zustaendig_email",
            "zustaendig_phone",
        ]


class BeDMSPlaceholdersSerializer(DMSPlaceholdersSerializer):
    bauvorhaben = fields.JointField(
        fields=[
            fields.MasterDataField(
                source="project", parser=get_option_label, join_by=", "
            ),
            fields.MasterDataField(source="proposal"),
        ],
        separator=", ",
        aliases=[_("PROJECT")],
        description=_("Project of the instance"),
    )
    ebau_number = fields.MasterDataField(
        source="dossier_number",
        aliases=[_("EBAU_NUMBER")],
        description=_("The eBau number of the instance"),
    )
    instance_id = fields.AliasedIntegerField(
        source="pk",
        aliases=[_("INSTANCE_ID")],
        description=_("ID of the instance"),
    )
    alcohol_serving = fields.MasterDataField(
        aliases=[_("ALCOHOL_SERVING")],
        description=_("With or without alcohol serving"),
    )
    administrative_district = fields.AliasedMethodField(
        aliases=[_("ADMINISTRATIVE_DISTRICT")],
        description=_("Administrative district"),
    )
    alle_gebaeudeeigentuemer_name_address = fields.MasterDataPersonField(
        source="building_owners",
        fields="__all__",
        aliases=[_("ALL_BUILDING_OWNERS_NAME_ADDRESS")],
        description=_("Names and addresses of all building owners"),
    )
    alle_gebaeudeeigentuemer = fields.MasterDataPersonField(
        source="building_owners",
        aliases=[_("ALL_BUILDING_OWNERS")],
        description=_("Names of all building owners"),
    )
    alle_vertreter_name_address = fields.MasterDataPersonField(
        source="legal_representatives",
        fields="__all__",
        aliases=[_("ALL_LEGAL_REPRESENTATIVES_NAME_ADDRESS")],
        description=_("Names and addresses of all legal representatives"),
    )
    alle_vertreter = fields.MasterDataPersonField(
        source="legal_representatives",
        aliases=[_("ALL_LEGAL_REPRESENTATIVES")],
        description=_("Names of all legal representatives"),
    )
    bauentscheid_baubewilligungsfrei = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-building-permit-free",
        aliases=[_("DECISION_BUILDING_PERMIT_FREE")],
    )
    bauentscheid_bauabschlag_mit_whst = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-construction-tee-with-restoration",
        aliases=[_("DECISION_CONSTRUCTION_TEE_WITH_RESTORATION")],
    )
    bauentscheid_bauabschlag_ohne_whst = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-construction-tee-without-restoration",
        aliases=[_("DECISION_CONSTRUCTION_TEE_WITHOUT_RESTORATION")],
    )
    bauentscheid_bauabschlag = fields.DecisionField(
        source="decision-approval-type",
        compare_to=[
            "decision-approval-type-construction-tee-with-restoration"
            "decision-approval-type-construction-tee-without-restoration",
        ],
        aliases=[_("DECISION_CONSTRUCTION_TEE")],
    )
    bauentscheid_baubewilligung = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-building-permit",
        aliases=[_("DECISION_BUILDING_PERMIT")],
    )
    bauentscheid_generell = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-general-building-permit",
        aliases=[_("DECISION_GENERAL")],
    )
    bauentscheid_gesamt = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-overall-building-permit",
        aliases=[_("DECISION_OVERALL")],
    )
    bauentscheid_klein = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-small-building-permit",
        aliases=[_("DECISION_SMALL")],
    )
    bauentscheid_positiv_teilweise = fields.DecisionField(
        source="decision-decision-assessment",
        compare_to=[
            "decision-decision-assessment-accepted",
            "decision-decision-assessment-positive",
            "decision-decision-assessment-positive-with-reservation",
        ],
        aliases=[_("DECISION_POSITIVE_PARTIAL")],
    )
    bauentscheid_positiv = fields.DecisionField(
        source="decision-decision-assessment",
        compare_to=[
            "decision-decision-assessment-accepted",
            "decision-decision-assessment-positive",
        ],
        aliases=[_("DECISION_POSITIVE")],
    )
    bauentscheid_projektaenderung = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-project-modification",
        aliases=[_("DECISION_PROJECT_MODIFICATION")],
    )
    bauentscheid_teilbaubewilligung = fields.DecisionField(
        source="decision-approval-type",
        compare_to="decision-approval-type-partial-building-permit",
        aliases=[_("DECISION_PARTIAL_BUILDING_PERMIT")],
    )
    bauentscheid_type = fields.DecisionField(
        source="decision-approval-type",
        use_identifier=True,
        aliases=[_("DECISION_TYPE")],
        description=_("Decision type"),
    )
    bauentscheid = fields.DecisionField(
        source="decision-decision-assessment",
        aliases=[_("DECISION")],
        description=_("Decision"),
    )
    construction_group = fields.MasterDataField(
        aliases=[_("CONSTRUCTION_GROUP")],
        description=_("Boolean placeholder for the 'construction_group' form field."),
        parser=get_option_label,
    )
    construction_group_designation = fields.MasterDataField(
        aliases=[_("CONSTRUCTION_GROUP_DESIGNATION")],
        description=_(
            "Placeholder for the 'construction_group_designation' form field."
        ),
    )
    contract = fields.MasterDataField(
        aliases=[_("CONTRACT")],
        description=_("Boolean placeholder for the 'contract' form field."),
        parser=get_option_label,
    )
    contract_start = fields.MasterDataField(
        parser=human_readable_date,
        aliases=[_("CONTRACT_START")],
        description=_("Date placeholder for the 'contract_start' form field"),
    )
    conservable = fields.MasterDataField(
        aliases=[_("CONSERVABLE")],
        description=_("Boolean placeholder for the 'conservable' form field."),
        parser=get_option_label,
    )
    k_object = fields.MasterDataField(
        aliases=[_("K_OBJECT")],
        description=_("Boolean placeholder for the 'k_object' form field."),
        parser=get_option_label,
    )
    decision_type = fields.DecisionField(
        source="decision-approval-type",
        use_identifier=True,
    )
    decision = fields.DecisionField(
        source="decision-decision-assessment",
        use_identifier=True,
    )
    dossier_link = fields.AliasedMethodField()
    email = fields.DeprecatedField()
    fachstellen_kantonal_list = fields.InquiriesField(
        props=["service_with_prefix"],
        join_by="\n",
        aliases=[_("SERVICES_CANTONAL_LIST")],
        description=_("Names of all involved cantonal services as list"),
    )
    gebaeudeeigentuemer_address_1 = fields.MasterDataPersonField(
        source="building_owners",
        only_first=True,
        fields=["address_1"],
        aliases=[_("BUILDING_OWNER_ADDRESS_1")],
        description=_("Address line 1 of the building owner"),
    )
    gebaeudeeigentuemer_address_2 = fields.MasterDataPersonField(
        source="building_owners",
        only_first=True,
        fields=["address_2"],
        aliases=[_("BUILDING_OWNER_ADDRESS_2")],
        description=_("Address line 2 of the building owner"),
    )
    gebaeudeeigentuemer_name_address = fields.MasterDataPersonField(
        source="building_owners",
        only_first=True,
        fields="__all__",
        aliases=[_("BUILDING_OWNER_NAME_ADDRESS")],
        description=_("Name and address of the building owner"),
    )
    gebaeudeeigentuemer = fields.MasterDataPersonField(
        source="building_owners",
        only_first=True,
        aliases=[_("BUILDING_OWNER")],
        description=_("Name of the building owner"),
    )
    gemeinde_adresse_1 = fields.MunicipalityField(
        source="address",
        aliases=[_("MUNICIPALITY_ADDRESS_1")],
        description=_("Address line 1 of the municipality"),
    )
    gemeinde_adresse_2 = fields.JointField(
        fields=[
            fields.MunicipalityField(source="zip"),
            fields.MunicipalityField(source="get_trans_attr", source_args=["city"]),
        ],
        aliases=[_("MUNICIPALITY_ADDRESS_2")],
        description=_("Address line 2 of the municipality"),
    )
    gewaesserschutzbereich = fields.MasterDataField(
        source="water_protection_area",
        parser=get_option_label,
        join_by=", ",
        aliases=[_("WATER_PROTECTION_AREA")],
        description=_("Water protection area"),
    )
    interior_seating = fields.MasterDataField(
        sum_by="total_seats",
        aliases=[_("INTERIOR_SEATING")],
        description=_("Sum of all interior seating"),
    )
    inventar = fields.AliasedMethodField(
        aliases=[_("INVENTORY")],
        description=_("Inventory"),
    )
    lastenausgleichsbegehren = fields.LegalSubmissionField(
        type="legal-submission-type-load-compensation-request",
        aliases=[_("LOAD_COMPENSATION_REQUESTS")],
        description=_('All legal submissions of the type "load compensation request"'),
    )
    leitperson = fields.ResponsibleUserField(
        source="full_name",
        aliases=[_("RESPONSIBLE_USER")],
        description=_("Responsible user of the authority"),
    )
    modification_date = fields.DeprecatedField()
    modification_time = fields.DeprecatedField()
    neighbors = fields.InformationOfNeighborsField(
        type="neighbors",
        aliases=[_("NEIGHBORS")],
    )
    objections = fields.LegalSubmissionField(
        type="legal-submission-type-objection",
        aliases=[_("OBJECTIONS")],
        description=_('All legal submissions of the type "objection"'),
    )
    opposing = fields.LegalClaimantsField(
        type="legal-submission-type-objection",
        aliases=[_("OPPOSING")],
        description=_("Opposing with address"),
    )
    legal_custodians = fields.LegalClaimantsField(
        type="legal-submission-type-legal-custody",
        aliases=[_("LEGAL_CUSTODIANS")],
        description=_("Legal custodians with address"),
    )
    load_compensation_requesting = fields.LegalClaimantsField(
        type="legal-submission-type-load-compensation-request",
        aliases=[_("LOAD_COMPENSATION_REQUESTING")],
        description=_("Load compensation requesting with address"),
    )
    legal_claimants = fields.LegalClaimantsField(
        aliases=[_("LEGAL_CLAIMANTS")],
        description=_("All legal claimants with address"),
    )
    outside_seating = fields.MasterDataField(
        aliases=[_("OUTSIDE_SEATING")],
        description=_("All outside seating"),
    )
    information_of_neighbors_link = fields.InformationOfNeighborsField(
        type="link",
        aliases=[_("INFORMATION_OF_NEIGHBORS_LINK")],
    )
    information_of_neighbors_qr_code = fields.InformationOfNeighborsField(
        type="qr_code",
        aliases=[_("INFORMATION_OF_NEIGHBORS_QR_CODE")],
    )
    nutzung = fields.MasterDataField(
        source="usage_type",
        join_by=", ",
        aliases=[_("USAGE_TYPE")],
        description=_("Usage type"),
    )
    nutzungszone = fields.MasterDataField(
        source="usage_zone",
        aliases=[_("USAGE_ZONE")],
        description=_("Usage zone"),
    )
    protected = fields.MasterDataField(
        aliases=[_("PROTECTED")],
        description=_("Boolean placeholder for the 'protected' form field."),
        parser=get_option_label,
    )
    protection_area = fields.MasterDataField(
        parser=get_option_label,
        join_by=", ",
        aliases=[_("PROTECTION_AREA")],
        description=_("Protection area"),
    )
    public = fields.MasterDataField(
        parser=get_option_label,
        aliases=[_("PUBLIC")],
        description=_("Hospitality public"),
    )
    publikation_1_anzeiger = fields.PublicationField(
        source="publikation-1-publikation-anzeiger",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_1_GAZETTE")],
        description=_("Date of the first publication in the gazette"),
    )
    publikation_2_anzeiger = fields.PublicationField(
        source="publikation-2-publikation-anzeiger",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_2_GAZETTE")],
        description=_("Date of the second publication in the gazette"),
    )
    publikation_amtsblatt = fields.PublicationField(
        source="publikation-amtsblatt",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_OFFICIAL_GAZETTE")],
        description=_("Date of the publication in the official gazette"),
    )
    publikation_anzeiger_name = fields.PublicationField(
        source="publikation-anzeiger-von",
        aliases=[_("PUBLICATION_GAZETTE_NAME")],
        description=_("Name of the gazette"),
    )
    publikation_ende = fields.PublicationField(
        source="publikation-ablaufdatum",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_END")],
        description=_("End date of the publication of the instance"),
    )
    publikation_start = fields.PublicationField(
        source="publikation-startdatum",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_START")],
        description=_("Start date of the publication of the instance"),
    )
    rechtsverwahrungen = fields.LegalSubmissionField(
        type="legal-submission-type-legal-custody",
        aliases=[_("LEGAL_CUSTODIES")],
        description=_('All legal submissions of the type "legal custody"'),
    )
    rrb = fields.MasterDataField(
        aliases=[_("RRB")],
        description=_("Boolean placeholder for the 'rrb' form field."),
        parser=get_option_label,
    )
    rrb_start = fields.MasterDataField(
        parser=human_readable_date,
        aliases=[_("RRB_START")],
        description=_("Date placeholder for the 'rrb_start' form field"),
    )
    sachverhalt = fields.MasterDataField(
        source="situation",
        aliases=[_("SITUATION")],
        description=_("Situation of the request"),
    )
    stichworte = fields.AliasedMethodField(
        aliases=[_("TAGS")],
        description=_("List of all tags"),
    )
    ueberbauungsordnung = fields.MasterDataField(
        source="development_regulations",
        aliases=[_("DEVELOPMENT_REGULATIONS")],
        description=_("Recorded development regulations of the applicant"),
    )
    uvp_ja_nein = fields.AliasedMethodField()
    vertreter_address_1 = fields.MasterDataPersonField(
        source="legal_representatives",
        only_first=True,
        fields=["address_1"],
        aliases=[_("LEGAL_REPRESENTATIVE_ADDRESS_1")],
        description=_("Address line 1 of the legal representative"),
    )
    vertreter_address_2 = fields.MasterDataPersonField(
        source="legal_representatives",
        only_first=True,
        fields=["address_2"],
        aliases=[_("LEGAL_REPRESENTATIVE_ADDRESS_2")],
        description=_("Address line 2 of the legal representative"),
    )
    vertreter_name_address = fields.MasterDataPersonField(
        source="legal_representatives",
        only_first=True,
        fields="__all__",
        aliases=[_("LEGAL_REPRESENTATIVE_NAME_ADDRESS")],
        description=_("Name and address of the legal representative"),
    )
    vertreter = fields.MasterDataPersonField(
        source="legal_representatives",
        only_first=True,
        aliases=[_("LEGAL_REPRESENTATIVE")],
        description=_("Name of the legal representative"),
    )
    zirkulation_rsta = fields.InquiriesField(
        service_group="district",
        aliases=[_("CIRCULATION_DISTRICT")],
        description=_("Involved districts of the instance"),
    )
    number_of_accomodated_persons = fields.MasterDataField(
        aliases=[_("NUMBER_OF_ACCOMODATED_PERSONS")],
        description=_("Number of accomodated persons"),
    )
    lifts = fields.MasterDataField(
        aliases=[_("LIFTS")],
        description=_("Lifts"),
        nested_aliases={
            "system_type": [_("SYSTEM_TYPE")],
            "new_or_existing": [_("NEW_OR_EXISTING")],
        },
    )
    dimension_height = fields.MasterDataField(
        parser=get_option_label,
        join_by=", ",
        aliases=[_("DIMENSION_HEIGHT")],
        description=_("Height"),
    )
    building_distances = fields.MasterDataField(
        aliases=[_("BUILDING_DISTANCES")],
        description=_("Distances between adjacent buildings"),
        nested_aliases={"side": [_("SIDE")], "distance": [_("DISTANCE")]},
    )
    hazardous_substances = fields.MasterDataField(
        aliases=[_("HAZARDOUS_SUBSTANCES")],
        description=_("Hazardous substances"),
        nested_aliases={
            "material": [_("MATERIAL")],
            "material_group": [_("MATERIAL_GROUP")],
            "amount": [_("AMOUNT")],
        },
    )
    ventilation_systems = fields.MasterDataField(
        aliases=[_("VENTILATION_SYSTEMS")],
        description=_("Ventilation systems"),
        nested_aliases={
            "system_type": [_("TYPE")],
            "air_volume": [_("AIR_VOLUME")],
            "new_or_existing": [_("NEW_OR_EXISTING")],
        },
    )
    rooms_with_more_than_50_persons = fields.MasterDataField(
        aliases=[_("ROOMS_WITH_MORE_THAN_50_PERSONS")],
        description=_("List of rooms with more than 50 persons"),
        nested_aliases={
            "room": [_("ROOM")],
            "number_of_persons": [_("NUMBER_OF_PERSONS")],
        },
    )
    room_occupancy_rooms_more_than_50_persons = fields.MasterDataField(
        aliases=[_("ROOM_OCCUPANCY_ROOMS_MORE_THAN_50_PERSONS")],
        description=_("Room occupancy rooms more than 50 persons"),
    )
    solar_panels = fields.MasterDataField(
        aliases=[_("SOLAR_PANELS")],
        description=_("Solar panels"),
        nested_aliases={
            "type": [_("TYPE")],
            "energy_storage": [_("ENERGY_STORAGE")],
            "energy_storage_capacity": [_("ENERGY_STORAGE_CAPACITY")],
            "new_or_existing": [_("NEW_OR_EXISTING")],
        },
    )
    stfv_short_report_date = fields.MasterDataField(
        aliases=[_("STFV_SHORT_REPORT_DATE")],
        description=_("STFV short report date"),
        parser=human_readable_date,
    )
    stfv_critial_value_exceeded = fields.MasterDataField(
        aliases=[_("STFV_CRITIAL_VALUE_EXCEEDED")],
        description=_("StfV critial value exceeded"),
        parser=get_option_label,
        join_by=", ",
    )
    stfv_short_report_date = fields.MasterDataField(
        aliases=[_("STFV_SHORT_REPORT_DATE")],
        description=_("STFV short report date"),
        parser=human_readable_date,
    )
    fire_protection_systems = fields.MasterDataField(
        aliases=[_("FIRE_PROTECTION_SYSTEMS")],
        description=_("Fire protection systems"),
        nested_aliases={
            "type": [_("TYPE")],
            "new_or_existing": [_("NEW_OR_EXISTING")],
        },
    )
    heating_systems = fields.MasterDataField(
        aliases=[_("HEATING_SYSTEMS")],
        description=_("Heating systems"),
        nested_aliases={
            "type": [_("TYPE")],
            "power": [_("POWER")],
            "combusitble_storage": [_("COMBUSITBLE_STORAGE")],
            "storage_amount": [_("STORAGE_AMOUNT")],
            "new_or_existing": [_("NEW_OR_EXISTING")],
        },
    )
    construction_costs = fields.MasterDataField(
        aliases=[_("CONSTRUCTION_COSTS")],
        description=_("Construction costs"),
    )
    floor_area = fields.MasterDataField(
        aliases=[_("FLOOR_AREA")],
        description=_("Floor area"),
    )
    qs_responsible = fields.MasterDataPersonField(
        aliases=[_("QS_RESPONSIBLE")],
        description=_("Name of the person responsible for QS"),
    )

    def get_administrative_district(self, instance):
        sheet = settings.APPLICATION.get("MUNICIPALITY_DATA_SHEET")
        if not sheet:  # pragma: no cover
            return None

        reader = csv.DictReader(open(sheet))
        municipalities = {row["Gemeinde"]: row["Verwaltungskreis"] for row in reader}

        caluma_api = CalumaApi()
        municipality_id = caluma_api.get_gemeinde(instance.case.document)
        municipality = (
            Service.objects.get(pk=municipality_id)
            .get_name("de")
            .replace("Leitbehörde ", "")
            if municipality_id
            else ""
        )
        return municipalities.get(municipality, "")

    def get_dossier_link(self, instance):
        return instance.get_internal_url()

    def get_inventar(self, instance):
        inventory = []

        for question in [
            "schuetzenswert",
            "erhaltenswert",
            "k-objekt",
            "baugruppe-bauinventar",
            "rrb",
            "vertrag",
        ]:
            answer = instance.case.document.answers.filter(question_id=question).first()

            if not answer or not answer.value == f"{question}-ja":
                continue

            if question in ["rrb", "vertrag"]:
                date_answer = instance.case.document.answers.filter(
                    question_id=f"{question}-vom"
                ).first()

                if date_answer:
                    inventory.append(
                        f"{date_answer.question.label.get(get_language())} {human_readable_date(date_answer.date)}"
                    )
                    continue
            elif question == "baugruppe-bauinventar":
                description = instance.case.document.answers.filter(
                    question_id="bezeichnung-baugruppe"
                ).first()

                if description:
                    inventory.append(
                        f"{answer.question.label.get(get_language())}: {description.value}"
                    )
                    continue

            inventory.append(answer.question.label.get(get_language()))

        return ", ".join(inventory)

    def get_stichworte(self, instance):
        return clean_join(
            *instance.tags.filter(service=self.context["request"].group.service)
            .order_by("pk")
            .values_list("name", flat=True),
            separator=", ",
        )

    def get_uvp_ja_nein(self, instance):
        return "mit-uvp" in instance.case.document.form_id

    class Meta:
        exclude = [
            "dossier_number",
            "gemeinde_webseite",
            "leitbehoerde_name_adresse",
            "leitbehoerde_webseite",
            "meine_organisation_webseite",
            "ort",
            "strasse",
        ]


class SoDMSPlaceholdersSerializer(DMSPlaceholdersSerializer):
    zirkulation_fachstellen = fields.InquiriesField(
        service_group=["service-cantonal", "service-extra-cantonal"],
        aliases=[_("CIRCULATION_SERVICES")],
        description=_("Involved services of the instance"),
    )
    publikation_start = fields.PublicationField(
        source="publikation-start",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_START")],
        description=_("Start date of the publication of the instance"),
    )
    publikation_ende = fields.PublicationField(
        source="publikation-ende",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_END")],
        description=_("End date of the publication of the instance"),
    )
    publikation_anzeiger = fields.PublicationField(
        source="publikation-anzeiger",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_DATE_GAZETTE")],
        description=_("Date of the publication in the gazette"),
    )
    publikation_amtsblatt = fields.PublicationField(
        source="publikation-amtsblatt",
        value_key="date",
        parser=human_readable_date,
        aliases=[_("PUBLICATION_DATE_OFFICIAL_GAZETTE")],
        description=_("Date of the publication in the official gazette"),
    )
    einsprechende = fields.LegalClaimantsField(
        aliases=[_("OPPOSING")],
        description=_("Opposing with address"),
    )
    entscheiddokumente = fields.AlexandriaDocumentField(
        mark="decision",
        aliases=[_("DECISION_DOCUMENTS")],
        description=_("All documents marked as decision documents"),
    )
    eingereichte_unterlagen = fields.AlexandriaDocumentField(
        category="beilagen-zum-gesuch",
        include_child_categories=True,
        aliases=[_("SUBMITTED_DOCUMENTS")],
        description=_("All submitted documents"),
    )
    eingereichte_plaene = fields.AlexandriaDocumentField(
        category="beilagen-zum-gesuch-projektplaene-projektbeschrieb",
        aliases=[_("SUBMITTED_PLANS")],
        description=_("All submitted plans"),
    )
    nutzungsplanung_grundnutzung = fields.MasterDataField(
        source="land_use_planning_land_use",
        aliases=[_("LAND_USE_PLANNING_LAND_USE")],
        description=_("Land use planning (land use)"),
    )
    publikation_organ = fields.PublicationField(
        source="publikation-organ",
        value_key="selected_options",
        parser=lambda options: [
            {
                "NAME": str(option.label),
                "EMAIL": option.meta.get("email"),
            }
            for option in options
        ],
        aliases=[_("PUBLICATION_ORGAN")],
        nested_aliases={
            "NAME": [_("NAME")],
            "EMAIL": [_("EMAIL")],
        },
        description=_("Publication organ of the instance"),
    )

    class Meta:
        exclude = [
            "description_modification",
            "nebenbestimmungen",
            "stellungnahme",
            "publikation_text",
            "language",
            "zirkulation_rueckmeldungen",
            "strasse",
            "ort",
            # TODO: Remove this if all authentication mechanisms provide a phone
            # number for the user
            "zustaendig_phone",
        ]
