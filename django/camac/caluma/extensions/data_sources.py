from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from caluma.caluma_form.models import Document
from django.core.cache import cache
from django.utils.translation import gettext as _, override

from camac.caluma.utils import find_answer
from camac.core.models import Authority
from camac.document.models import Attachment
from camac.user.models import Location, Service

from .countries import COUNTRIES


def get_municipality_label(service, municipality_prefix=False):
    translations = service.trans.all()
    label = {}

    for translation in translations:
        name = (
            translation.name.replace(
                "Leitbehörde", "Gemeinde" if municipality_prefix else ""
            ).replace(
                "Autorité directrice", "Municipalité" if municipality_prefix else ""
            )
        ).strip()

        if service.disabled:
            with override(translation.language):
                postfix = _("not activated")
                text = f"{name} ({postfix})"
        else:
            text = name

        label[translation.language] = text

    for language in ["de", "fr"]:
        if language not in label.keys():
            label[language] = list(label.values())[0]

    return label


def get_others_option():
    label = {}

    for language in ["de", "fr"]:
        with override(language):
            label[language] = _("Others")

    return ["-1", label]


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
    "Koordinationsstelle Umweltschutz AfU": [
        [251, "Internes Mitberichtsverfahren AfU"],
        [252, "Internes Mitberichtsverfahren nach Artikel 30 BG Umweltschutz"],
        [253, "Internes Mitberichtsverfahren / Bewilligungsverfahren gemäss UVP"],
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

        data = sorted(
            [
                [str(service.pk), get_municipality_label(service, True)]
                for service in services
            ],
            key=lambda x: x[1]["de"].casefold(),
        ) + [get_others_option()]

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
        instance_id = context.get("instanceId")

        document = Document.objects.get(case__instance__pk=instance_id)
        rows = find_answer(document, "personalien-grundeigentumerin")

        if not rows:  # pragma: no cover
            return

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
