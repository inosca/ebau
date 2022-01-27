import csv
import itertools
from collections import OrderedDict

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from camac.caluma.api import CalumaApi
from camac.objection.models import Objection
from camac.user.models import Service

from ..master_data import MasterData
from . import fields
from .aliases import ALIASES
from .utils import clean_join, get_option_label, human_readable_date


class DMSPlaceholdersSerializer(serializers.Serializer):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)

        instance._master_data = MasterData(instance.case)

    def get_aliases(self, key, prefix):
        return ALIASES.get(clean_join(prefix.upper(), key.upper(), separator="."), [])

    def get_aliased_collection(self, collection, prefix=""):
        return OrderedDict(
            sorted(
                itertools.chain(
                    *[
                        self.get_aliased_field(key, value, prefix)
                        for key, value in collection.items()
                    ]
                )
            )
        )

    def get_aliased_field(self, key, value, prefix=""):
        value = "" if value is None else value

        if isinstance(value, list) and all([isinstance(row, dict) for row in value]):
            value = [self.get_aliased_collection(row, key) for row in value]

        return [(name, value) for name in self.get_aliases(key, prefix) + [key.upper()]]

    def to_representation(self, instance):
        return self.get_aliased_collection(super().to_representation(instance))

    address = fields.JointField(
        fields=[
            fields.JointField(
                fields=[
                    fields.MasterDataField(source="street"),
                    fields.MasterDataField(source="street_number"),
                ]
            ),
            fields.MasterDataField(source="city"),
        ],
        separator=", ",
    )
    administrative_district = serializers.SerializerMethodField()
    alcohol_serving = fields.MasterDataField()
    alle_gebaeudeeigentuemer_name_address = fields.MasterDataPersonField(
        source="building_owners", fields="__all__"
    )
    alle_gebaeudeeigentuemer = fields.MasterDataPersonField(source="building_owners")
    alle_gesuchsteller_name_address = fields.MasterDataPersonField(
        source="applicants", fields="__all__"
    )
    alle_gesuchsteller = fields.MasterDataPersonField(source="applicants")
    alle_grundeigentuemer_name_address = fields.MasterDataPersonField(
        source="landowners", fields="__all__"
    )
    alle_grundeigentuemer = fields.MasterDataPersonField(source="landowners")
    alle_projektverfasser_name_address = fields.MasterDataPersonField(
        source="project_authors", fields="__all__"
    )
    alle_projektverfasser = fields.MasterDataPersonField(source="project_authors")
    alle_vertreter_name_address = fields.MasterDataPersonField(
        source="legal_representatives", fields="__all__"
    )
    alle_vertreter = fields.MasterDataPersonField(source="legal_representatives")
    base_url = serializers.SerializerMethodField()
    baueingabe_datum = fields.MasterDataField(
        source="submit_date", parser=human_readable_date
    )
    bauentscheid_abschreibungsverfuegung = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="ABSCHREIBUNGSVERFUEGUNG"
    )
    bauentscheid_baubewilligungsfrei = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="BAUBEWILLIGUNGSFREI"
    )
    bauentscheid_bauabschlag_mit_whst = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="BAUABSCHLAG_MIT_WHST"
    )
    bauentscheid_bauabschlag_ohne_whst = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="BAUABSCHLAG_OHNE_WHST"
    )
    bauentscheid_bauabschlag = fields.BooleanCompareField(
        source="decision.decision_type",
        compare_to=["BAUABSCHLAG_MIT_WHST", "BAUABSCHLAG_OHNE_WHST"],
    )
    bauentscheid_baubewilligung = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="BAUBEWILLIGUNG"
    )
    bauentscheid_generell = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="GENERELL"
    )
    bauentscheid_gesamt = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="GESAMT"
    )
    bauentscheid_klein = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="KLEIN"
    )
    bauentscheid_positiv_teilweise = fields.BooleanCompareField(
        source="decision.decision",
        compare_to=["positive", "accepted", "conditionallyPositive"],
    )
    bauentscheid_positiv = fields.BooleanCompareField(
        source="decision.decision", compare_to=["positive", "accepted"]
    )
    bauentscheid_projektaenderung = fields.DeprecatedField(value=False)
    bauentscheid_teilbaubewilligung = fields.BooleanCompareField(
        source="decision.decision_type", compare_to="TEILBAUBEWILLIGUNG"
    )
    bauentscheid_type = ReadOnlyField(source="decision.decision_type")
    bauentscheid = serializers.SerializerMethodField()
    bauvorhaben = fields.JointField(
        fields=[
            fields.MasterDataField(
                source="project", parser=get_option_label, join_by=", "
            ),
            fields.MasterDataField(source="proposal"),
        ],
        separator=", ",
    )
    beschreibung_bauvorhaben = fields.MasterDataField(source="proposal")
    decision_date = fields.HumanReadableDateField(source="decision.decision_date")
    decision_type = serializers.ReadOnlyField(source="decision.decision_type")
    decision = serializers.ReadOnlyField(source="decision.decision")
    dossier_link = serializers.SerializerMethodField()
    ebau_number = fields.MasterDataField(source="dossier_number")
    eigene_gebuehren_total = fields.BillingEntriesField(own=True, total=True)
    eigene_gebuehren = fields.BillingEntriesField(own=True)
    email = fields.DeprecatedField()
    fachstellen_kantonal_list = fields.ActivationsField(
        props=["service_with_prefix"], join_by="\n"
    )
    fachstellen_kantonal = fields.ActivationsField()
    form_name = serializers.SerializerMethodField()
    gebaeudeeigentuemer_address_1 = fields.MasterDataPersonField(
        source="building_owners", only_first=True, fields=["address_1"]
    )
    gebaeudeeigentuemer_address_2 = fields.MasterDataPersonField(
        source="building_owners", only_first=True, fields=["address_2"]
    )
    gebaeudeeigentuemer_name_address = fields.MasterDataPersonField(
        source="building_owners", only_first=True, fields="__all__"
    )
    gebaeudeeigentuemer = fields.MasterDataPersonField(
        source="building_owners", only_first=True
    )
    gebuehren_total = fields.BillingEntriesField(total=True)
    gebuehren = fields.BillingEntriesField()
    gemeinde_adresse_1 = fields.MunicipalityField(source="address")
    gemeinde_adresse_2 = fields.JointField(
        fields=[
            fields.MunicipalityField(source="zip"),
            fields.MunicipalityField(source="get_trans_attr", source_args=["city"]),
        ]
    )
    gemeinde_email = fields.MunicipalityField(source="email")
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
    )
    gemeinde_ort = fields.MunicipalityField(
        source="get_trans_attr", source_args=["city"]
    )
    gemeinde_telefon = fields.MunicipalityField(source="phone")
    gesuchsteller_address_1 = fields.MasterDataPersonField(
        source="applicants", only_first=True, fields=["address_1"]
    )
    gesuchsteller_address_2 = fields.MasterDataPersonField(
        source="applicants", only_first=True, fields=["address_2"]
    )
    gesuchsteller_name_address = fields.MasterDataPersonField(
        source="applicants", only_first=True, fields="__all__"
    )
    gesuchsteller = fields.MasterDataPersonField(source="applicants", only_first=True)
    gewaesserschutzbereich = fields.MasterDataField(
        source="water_protection_area", parser=get_option_label, join_by=", "
    )
    grundeigentuemer_address_1 = fields.MasterDataPersonField(
        source="landowners", only_first=True, fields=["address_1"]
    )
    grundeigentuemer_address_2 = fields.MasterDataPersonField(
        source="landowners", only_first=True, fields=["address_2"]
    )
    grundeigentuemer_name_address = fields.MasterDataPersonField(
        source="landowners", only_first=True, fields="__all__"
    )
    grundeigentuemer = fields.MasterDataPersonField(
        source="landowners", only_first=True
    )
    instance_id = serializers.IntegerField(source="pk")
    interior_seating = fields.MasterDataField(sum_by="total_seats")
    inventar = fields.JointField(
        fields=[
            fields.MasterDataField(
                source="monument_worth_protecting", parser=get_option_label
            ),
            fields.MasterDataField(
                source="monument_worth_preserving", parser=get_option_label
            ),
            fields.MasterDataField(source="monument_k_object", parser=get_option_label),
            fields.MasterDataField(
                source="monument_inventory", parser=get_option_label
            ),
            fields.MasterDataField(source="monument_rrb", parser=get_option_label),
            fields.MasterDataField(source="monument_contract", parser=get_option_label),
        ],
        separator=", ",
    )
    juristic_name = fields.MasterDataPersonField(
        source="applicants", only_first=True, fields=["juristic_name"]
    )
    koordinaten = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    leitbehoerde_address_1 = fields.ResponsibleServiceField(source="address")
    leitbehoerde_address_2 = fields.JointField(
        fields=[
            fields.ResponsibleServiceField(source="zip"),
            fields.ResponsibleServiceField(
                source="get_trans_attr",
                source_args=["city"],
            ),
        ]
    )
    leitbehoerde_city = fields.ResponsibleServiceField(
        source="get_trans_attr", source_args=["city"]
    )
    leitbehoerde_email = fields.ResponsibleServiceField(source="email")
    leitbehoerde_name_kurz = fields.ResponsibleServiceField(
        source="get_name", remove_name_prefix=True
    )
    leitbehoerde_name = fields.ResponsibleServiceField(source="get_name")
    leitbehoerde_phone = fields.ResponsibleServiceField(source="phone")
    leitperson = fields.ResponsibleUserField(source="full_name")
    meine_organisation_adresse_1 = fields.CurrentServiceField(source="address")
    meine_organisation_adresse_2 = fields.JointField(
        fields=[
            fields.CurrentServiceField(source="zip"),
            fields.CurrentServiceField(source="get_trans_attr", source_args=["city"]),
        ]
    )
    meine_organisation_email = fields.CurrentServiceField(source="email")
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
    )
    meine_organisation_name_kurz = fields.CurrentServiceField(
        source="get_name", remove_name_prefix=True
    )
    meine_organisation_name = fields.CurrentServiceField(source="get_name")
    meine_organisation_ort = fields.CurrentServiceField(
        source="get_trans_attr", source_args=["city"]
    )
    meine_organisation_telefon = fields.CurrentServiceField(source="phone")
    modification_date = fields.DeprecatedField()
    modification_time = fields.DeprecatedField()
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
    )
    municipality = fields.MunicipalityField(source="get_name", remove_name_prefix=True)
    name = fields.DeprecatedField()
    nebenbestimmungen_mapped = fields.ActivationsField(
        only_own=True, props=[("service", "FACHSTELLE"), ("collateral", "TEXT")]
    )
    nebenbestimmungen = fields.ActivationsField(
        only_own=True, props=["collateral"], join_by="\n\n"
    )
    neighbors = fields.MasterDataDictPersonField()
    opposing = serializers.SerializerMethodField()
    outside_seating = fields.MasterDataField()
    information_of_neighbors_link = fields.InformationOfNeighborsLinkField()
    information_of_neighbors_qr_code = fields.InformationOfNeighborsLinkField(
        as_qrcode=True
    )
    nutzung = fields.MasterDataField(
        source="usage_type", parser=get_option_label, join_by=", "
    )
    nutzungszone = fields.MasterDataField(source="usage_zone")
    parzelle = serializers.SerializerMethodField()
    projektverfasser_address_1 = fields.MasterDataPersonField(
        source="project_authors", only_first=True, fields=["address_1"]
    )
    projektverfasser_address_2 = fields.MasterDataPersonField(
        source="project_authors", only_first=True, fields=["address_2"]
    )
    projektverfasser_name_address = fields.MasterDataPersonField(
        source="project_authors", only_first=True, fields="__all__"
    )
    projektverfasser = fields.MasterDataPersonField(
        source="project_authors", only_first=True
    )
    protection_area = fields.MasterDataField(parser=get_option_label, join_by=", ")
    public = fields.MasterDataField(parser=get_option_label)
    publikation_1_anzeiger = fields.PublicationField(
        source="publikation-1-publikation-anzeiger",
        value_key="date",
        parser=human_readable_date,
    )
    publikation_2_anzeiger = fields.PublicationField(
        source="publikation-2-publikation-anzeiger",
        value_key="date",
        parser=human_readable_date,
    )
    publikation_amtsblatt = fields.PublicationField(
        source="publikation-amtsblatt", value_key="date", parser=human_readable_date
    )
    publikation_anzeiger_name = fields.PublicationField(
        source="publikation-anzeiger-von"
    )
    publikation_ende = fields.PublicationField(
        source="publikation-ablaufdatum", value_key="date", parser=human_readable_date
    )
    publikation_start = fields.PublicationField(
        source="publikation-startdatum", value_key="date", parser=human_readable_date
    )
    publikation_text = fields.PublicationField(source="publikation-text")
    sachverhalt = fields.MasterDataField(source="situation")
    status = serializers.SerializerMethodField()
    stellungnahme = fields.ActivationsField(
        only_own=True, props=["opinion"], join_by="\n\n"
    )
    stichworte = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    ueberbauungsordnung = fields.MasterDataField(source="development_regulations")
    uvp_ja_nein = serializers.SerializerMethodField()
    vertreter_address_1 = fields.MasterDataPersonField(
        source="legal_representatives", only_first=True, fields=["address_1"]
    )
    vertreter_address_2 = fields.MasterDataPersonField(
        source="legal_representatives", only_first=True, fields=["address_2"]
    )
    vertreter_name_address = fields.MasterDataPersonField(
        source="legal_representatives", only_first=True, fields="__all__"
    )
    vertreter = fields.MasterDataPersonField(
        source="legal_representatives", only_first=True
    )
    zirkulation_fachstellen = fields.ActivationsField(
        filters={"service__service_group__name": "service"}
    )
    zirkulation_gemeinden = fields.ActivationsField(
        filters={"service__service_group__name": "municipality"}
    )
    zirkulation_rsta = fields.ActivationsField(
        filters={"service__service_group__name": "district"}
    )
    zirkulation_rueckmeldungen = fields.ActivationsField(
        filters={
            "circulation_state__name": "DONE",
            "circulation_answer__isnull": False,
        },
        props=[
            ("opinion", "STELLUNGNAHME"),
            ("collateral", "NEBENBESTIMMUNGEN"),
            ("answer", "ANTWORT"),
            ("service", "VON"),
        ],
    )
    zustaendig_email = fields.ResponsibleUserField(source="email")
    zustaendig_name = fields.ResponsibleUserField(source="full_name")
    zustaendig_phone = fields.ResponsibleUserField(source="phone")

    def get_administrative_district(self, instance):
        sheet = settings.APPLICATION.get("MUNICIPALITY_DATA_SHEET")
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

    def get_base_url(self, instance):
        return settings.INTERNAL_BASE_URL

    def get_bauentscheid(self, instance):
        types = {
            "positive": _("positive"),
            "negative": _("negative"),
            "conditionallyPositive": _(
                "conditionally positive (project needs to be adjusted)"
            ),
            "retreat": _("retreat"),
            "accepted": _("accepted"),
            "denied": _("denied"),
            "writtenOff": _("written off"),
            "obligated": _("requires building permit"),
            "notObligated": _("does not require building permit"),
            "other": _("other decision"),
        }

        return (
            types.get(instance.decision.decision)
            if hasattr(instance, "decision")
            else None
        )

    def get_dossier_link(self, instance):
        return settings.INTERNAL_INSTANCE_URL_TEMPLATE.format(instance_id=instance.pk)

    def get_form_name(self, instance):
        return instance.case.document.form.name.get(get_language())

    def get_koordinaten(self, instance):
        return clean_join(
            *[
                clean_join(
                    *[
                        f"{int(plot.get(key)):,}".replace(",", "’")
                        for key in ["coord_east", "coord_north"]
                    ],
                    separator=" / ",
                )
                for plot in instance._master_data.plot_data
            ],
            separator="; ",
        )

    def get_language(self, instance):
        return get_language()

    def get_opposing(self, instance):
        objections = Objection.objects.filter(instance=instance)

        data = []
        for objection in objections:
            for opponent in objection.objection_participants.all():
                data.append(
                    {
                        "NAME": ", ".join(
                            filter(None, [opponent.company, opponent.name])
                        ),
                        "ADDRESS": ", ".join(
                            filter(None, [opponent.address, opponent.city])
                        ),
                    }
                )

        return data

    def get_parzelle(self, instance):
        return clean_join(
            *[plot.get("plot_number") for plot in instance._master_data.plot_data],
            separator=", ",
        )

    def get_status(self, instance):
        return instance.instance_state.get_name()

    def get_stichworte(self, instance):
        return clean_join(
            *instance.tags.filter(service=self.context["request"].group.service)
            .order_by("pk")
            .values_list("name", flat=True),
            separator=", ",
        )

    def get_today(self, instance):
        return human_readable_date(now().date())

    def get_uvp_ja_nein(self, instance):
        return "mit-uvp" in instance.case.document.form_id
