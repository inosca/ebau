from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from caluma.caluma_form.models import Document
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _, gettext_noop, override

from camac.caluma.utils import find_answer
from camac.core.models import Authority
from camac.document.models import Attachment
from camac.instance.models import Instance
from camac.user.models import Location, Service

from .countries import COUNTRIES

LANGUAGES = [key for key, _ in settings.LANGUAGES]


def get_municipality_label(service, municipality_prefix=False):
    translations = service.trans.all()
    label = {}

    for translation in translations:
        name = translation.name

        with override(translation.language):
            for prefix in [_("Authority"), _("Municipality")]:
                name = name.replace(
                    prefix, _("Municipality") if municipality_prefix else ""
                ).strip()

            if service.disabled:
                postfix = _("not activated")
                name = f"{name} ({postfix})"

        label[translation.language] = name

    for language in LANGUAGES:
        if language not in label.keys():
            label[language] = list(label.values())[0]

    return label


def get_additional_option(slug="-1", text=gettext_noop("Others")):
    label = {}

    for language in LANGUAGES:
        with override(language):
            label[language] = _(text)

    return [slug, label]


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    def get_data(self, user, question, context):
        cache_key = f"data_source_{type(self).__name__}"
        include_disabled = (
            hasattr(user, "group")
            and Service.objects.filter(
                pk=user.group, service_group__name="district"
            ).exists()
            or (hasattr(user, "camac_role") and user.camac_role == "support")
        )

        if include_disabled:
            cache_key += "_with_disabled"
            filters = {}
        else:
            filters = {"disabled": False}

        return cache.get_or_set(cache_key, lambda: self._get_data(filters), 3600)

    def _get_data(self, filters):
        services = (
            Service.objects.select_related("service_group")
            .filter(
                service_parent__isnull=True,
                service_group__name="municipality",
                **filters,
            )
            .prefetch_related("trans")
        )

        return sorted(
            [[service.pk, get_municipality_label(service)] for service in services],
            key=lambda x: x[1]["de"].casefold(),
        )


class Locations(BaseDataSource):
    info = "List of locations from Camac"

    def get_data(self, user, question, context):
        cache_key = f"data_source_{type(self).__name__}"
        include_special = (
            hasattr(user, "camac_role") and user.camac_role != "Portal User"
        )

        if include_special:
            cache_key += "_with_special"
            filters = {}
        else:
            # UR: Hide "Alle Gemeinden" and "Diverse Gemeinden" for regular applicants
            filters = {"zip__isnull": False}

        return cache.get_or_set(cache_key, lambda: self._get_data(filters), 3600)

    def _get_data(self, filters):
        locations = Location.objects.filter(**filters)

        return sorted(
            [
                [int(loc.communal_federal_number), loc.name]
                for loc in locations.iterator()
            ],
            key=lambda x: x[1].casefold(),
        )


form_mapping_by_koor = {
    "Koordinationsstelle Baugesuche BG": [
        [42, "Internes Mitberichtsverfahren / Genehmigungsverfahren"],
        [46, "Mitberichtverfahren zu Plangenehmigungsverfahren Militär (PGV Militär)"],
        [
            45,
            "Mitberichtverfahren zu Plangenehmigungsverfahren Luftfahrt (PGV Luftfahrt)",
        ],
        [
            250,
            "Mitberichtverfahren zu Plangenehmigungsverfahren Seilbahn (PGV Seilbahn)",
        ],
    ],
    "Koordinationsstelle Baudirektion BD": [
        [223, "PGV öffentliche Gewässer (Artikel 12 WBG)"],
        [224, "PGV private Gewässer (Artikel 19 WBG)"],
        [181, "PGV Kantonsstrasse (Artikel 30 StrG)"],
        [201, "PGV Gemeindestrasse (Artikel 30 StrG)"],
        [221, "PGV Korporationsstrasse (Artikel 30 StrG)"],
        [222, "PGV vereinfachtes Verfahren (Artikel 31 StrG)"],
        [
            225,
            "Konzessionsverfahren Regierungsrat für Anlagen bis 1000 kW (Artikel 18 GNG)",
        ],
        [241, "Konzessionsverfahren Landrat für Anlagen ab 1000 kW (Artikel 18 GNG)"],
        [242, "Konzessionsverfahren Baudirektion für Wärmeentnahmen (Artikel 40 GNG)"],
        [243, "Mitberichtsverfahren / PGV nach Starkstromverordnung (EleG)"],
        [244, "Mitberichtsverfahren / PGV nach Eisenbahngesetz (EBG)"],
        [245, "Mitberichtsverfahren / PGV nach Nationalstrassengesetz (NSG)"],
        [
            246,
            "Konzessionsverfahren Baudirektion Beanspruchung Kantonsgewässer bis 500 m2 (Artikel 3 ORR)",
        ],
        [248, "Internes Mitberichtsverfahren BD"],
        [286, "Land- und Rechtserweb"],
    ],
    "Koordinationsstelle Nutzungsplanung NP": [
        [161, "Internes Mitberichtsverfahren"],
        [46, "Mitberichtverfahren zu Plangenehmigungsverfahren Militär (PGV Militär)"],
        [
            45,
            "Mitberichtverfahren zu Plangenehmigungsverfahren Luftfahrt (PGV Luftfahrt)",
        ],
        [
            250,
            "Mitberichtverfahren zu Plangenehmigungsverfahren Seilbahn (PGV Seilbahn)",
        ],
    ],
    "Koordinationsstelle Energie AfE": [
        [256, "Internes Mitberichtsverfahren AfE"],
        [
            257,
            "Konzessionsverfahren Regierungsrat für Anlagen bis 1000 kW (Artikel 18 GNG)",
        ],
        [258, "Konzessionsverfahren Landrat für Anlagen ab 1000 kW (Artikel 18 GNG)"],
        [259, "Konzessionsverfahren Baudirektion für Wärmeentnahmen (Artikel 40 GNG)"],
        [
            289,
            "Konzessionsverfahren Korporationsgewässer mit Genehmigung durch Regierungsrat (Artikel 15 GNG)",
        ],
    ],
    "Koordinationsstelle Forst und Jagd AFJ": [
        [260, "Internes Mitberichtsverfahren AFJ"],
    ],
    "Koordinationsstelle Landwirtschaft ALA": [
        [254, "Internes Mitberichtsverfahren ALA"],
        [
            255,
            "Internes Mitberichtsverfahren ALA (Korporationsstrassen mit Subventionierung)",
        ],
    ],
    "Koordinationsstelle Sicherheitsdirektion SD": [
        [287, "Internes Mitberichtsverfahren SD AfKP"],
        [288, "Internes Mitberichtsverfahren SD"],
    ],
    "Koordinationsstelle Umwelt AfU": [
        [251, "Internes Mitberichtsverfahren AfU"],
        [252, "Internes Mitberichtsverfahren nach Artikel 30 BG Umweltschutz"],
        [253, "Internes Mitberichtsverfahren / Bewilligungsverfahren gemäss UVP"],
    ],
    "Koordinationsstelle Amt für das Grundbuch AfG": [
        [306, "Internes Mitberichtsverfahren AfG"],
    ],
}


class Mitberichtsverfahren(BaseDataSource):
    info = "List of different types of 'Mitberichtsverfahren' (role-dependent)"

    def get_data(self, user, question, context):
        if not hasattr(user, "camac_role"):  # pragma: no cover
            return []
        return form_mapping_by_koor.get(user.camac_role, [])


class Services(BaseDataSource):
    info = "List of services, municipalities and RSTAs from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, user, question, context):
        services = (
            Service.objects.select_related("service_group")
            .filter(
                service_parent__isnull=True,
                service_group__name__in=[
                    "service",
                    "municipality",
                    "district",
                ],
                disabled=False,
            )
            .prefetch_related("trans")
        )

        data = [get_additional_option()] + sorted(
            [
                [str(service.pk), get_municipality_label(service, True)]
                for service in services
            ],
            key=lambda x: x[1]["de"].casefold(),
        )

        return data


class Countries(BaseDataSource):
    info = "List of all countries in the world with opinionated sorting"

    @data_source_cache(timeout=3600)
    def get_data(self, user, question, context):
        return COUNTRIES


class Authorities(BaseDataSource):
    info = "List of authorities from camac"

    def get_data(self, user, question, context):
        return [[authority.pk, authority.name] for authority in Authority.objects.all()]


class Attachments(BaseDataSource):
    info = "List of attachments in a given attachment section"

    @data_source_cache(timeout=5)
    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        attachment_section_id = question.meta.get("attachmentSection")
        instance_id = context.get("instanceId")

        if not attachment_section_id or not instance_id:
            return []

        return Attachment.objects.filter(
            attachment_sections__pk=attachment_section_id,
            instance_id=instance_id,
        ).values_list("pk", flat=True)


class Landowners(BaseDataSource):
    info = "Selection of the landowners from the current instance"

    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        instance_id = context.get("instanceId")

        document = Document.objects.get(case__instance__pk=instance_id)
        rows = find_answer(document, "personalien-grundeigentumerin")

        if not rows:  # pragma: no cover
            return []

        landowner_data = []
        for row in rows:
            is_juristic = (
                find_answer(
                    row, "juristische-person-grundeigentuemerin", raw_value=True
                )
                == "juristische-person-grundeigentuemerin-ja"
            )

            if is_juristic:
                label = find_answer(row, "name-juristische-person-grundeigentuemerin")
            else:
                label = " ".join(
                    [
                        find_answer(row, "vorname-grundeigentuemerin"),
                        find_answer(row, "name-grundeigentuemerin"),
                    ]
                )

            landowner_data.append((row.pk, label))

        return landowner_data


class PreliminaryClarificationTargets(BaseDataSource):
    info = (
        "List of services that can be selected for preliminary clarifications in Kt. SO"
    )

    @data_source_cache(timeout=3600)
    def get_data(self, user, question, context):
        services = (
            Service.objects.select_related("service_group")
            .filter(
                service_parent__isnull=True,
                service_group__name__in=[
                    "service-cantonal",
                    "service-extra-cantonal",
                    "service-bab",
                ],
                disabled=False,
            )
            .prefetch_related("trans")
        )

        data = [
            get_additional_option(),
            get_additional_option("0", gettext_noop("Local building authority")),
        ] + sorted(
            [
                [str(service.pk), get_municipality_label(service, True)]
                for service in services
            ],
            key=lambda x: x[1]["de"].casefold(),
        )

        return data


class Buildings(BaseDataSource):
    info = "Selection of the buildings from the current instance"

    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        document = Document.objects.get(case__instance__pk=context.get("instanceId"))
        buildings = find_answer(document, "gebaeude")

        return (
            [
                (building.pk, find_answer(building, "gebaeude-bezeichnung"))
                for building in buildings
            ]
            if buildings
            else None
        )


class ServicesForFinalReport(BaseDataSource):
    info = "Services which asked to be invited to the 'Schlussabnahme' (final report) during the distribution phase"

    @data_source_cache(timeout=3600)
    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        instance = Instance.objects.get(pk=context.get("instanceId"))
        distribution_case = instance.case.work_items.get(
            task_id=settings.DISTRIBUTION["DISTRIBUTION_TASK"]
        ).child_case

        pks_of_services_to_be_invited = []

        for inquiry in distribution_case.work_items.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"]
        ):
            if invite_answer := inquiry.child_case.document.answers.filter(
                question_id="inquiry-answer-invite-service"
            ).first():
                if invite_answer.value == "inquiry-answer-invite-service-yes":
                    pks_of_services_to_be_invited.append(*inquiry.addressed_groups)

        return (
            [
                (service.pk, service.name)
                for service in Service.objects.filter(
                    pk__in=pks_of_services_to_be_invited
                )
            ]
            if len(pks_of_services_to_be_invited) > 0
            else None
        )
