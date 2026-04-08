import uuid
from typing import Tuple

from alexandria.core.models import Document as AlexandriaDocument
from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _, gettext_noop, override

from camac.applicants.models import Applicant
from camac.caluma.models import Inquiry
from camac.caluma.utils import find_answer
from camac.core.models import Authority
from camac.core.utils import canton_aware
from camac.document.models import Attachment
from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.instance.placeholders.utils import get_person_name
from camac.sanctions.models import Sanction
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


def on_copy_from_reference_document(
    old_answer: Answer, new_answer: Answer, old_value: Tuple[str, str]
) -> Tuple[str | None, str | None]:
    old_slug, old_label = old_value
    if not old_slug:
        return (None, None)

    try:
        uuid_value = uuid.UUID(old_slug)
    except ValueError:
        return (None, None)

    reference_doc = (
        Document.objects.filter(source_id=uuid_value).order_by("-created_at").first()
    )

    return (str(reference_doc.pk), old_label) if reference_doc else (None, None)


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    @canton_aware
    def get_service_groups(self, user, context):
        """Get service groups to consider as municipalities.

        Return a tuple:
        - list of service group names
        - a cache key
        """
        return (["municipality"], "")

    def get_service_groups_ag(self, user, context):
        service_groups = ["municipality"]
        cache_key = "_applicant"
        is_internal = getattr(user, "camac_role", None) != "applicant"
        is_pgv_gas = False
        if context and "instanceId" in context:
            case = Case.objects.get(instance__pk=context["instanceId"])
            is_pgv_gas = case.document.form_id == "plangenehmigungsverfahren-gas"
        if not user or is_internal or is_pgv_gas:
            service_groups.append("municipality-light")
            if is_internal:
                cache_key = "_non_applicant"
            else:
                cache_key += "_pgv_gas" if is_pgv_gas else "_other"
        return (service_groups, cache_key)

    def get_data(self, user, question, context):
        cache_key = f"data_source_{type(self).__name__}"
        include_disabled = (
            hasattr(user, "group")
            and Service.objects.filter(
                pk=user.group, service_group__name="district"
            ).exists()
            or (hasattr(user, "camac_role") and user.camac_role == "support")
        )

        filters = {}
        group_names, cache_key_addition = self.get_service_groups(user, context)
        cache_key += cache_key_addition

        if include_disabled:
            cache_key += "_with_disabled"
        else:
            filters = {"disabled": False}

        filters["service_group__name__in"] = group_names

        return cache.get_or_set(cache_key, lambda: self._get_data(filters), 300)

    def _get_data(self, filters):
        services = (
            Service.objects.select_related("service_group")
            .filter(
                service_parent__isnull=True,
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
        return list(COUNTRIES.keys())


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

        instance_id = context.get("instanceId")

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            attachment_section_id = question.meta.get("attachmentSection")

            if not attachment_section_id or not instance_id:
                return []

            return Attachment.objects.filter(
                attachment_sections__pk=attachment_section_id,
                instance_id=instance_id,
            ).values_list("pk", flat=True)

        category = question.meta.get("alexandriaCategory")

        if not category or not instance_id:
            return []

        return AlexandriaDocument.objects.filter(
            category=category,
            instance_document__instance_id=instance_id,
        ).values_list("pk", flat=True)


class Landowners(BaseDataSource):
    info = "Selection of the landowners from the current instance"

    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        instance_id = context.get("instanceId")
        if not instance_id:  # pragma: no cover
            return []

        cache_key = f"data_source_{type(self).__name__}_{instance_id}"
        return cache.get_or_set(cache_key, lambda: self._get_data(instance_id), 5)

    def _get_data(self, instance_id):
        case = Case.objects.get(instance__pk=instance_id)
        master_data = MasterData(case)

        people = master_data.landowners

        if settings.APPLICATION_NAME == "kt_so":
            people = master_data.applicants + people

        return [(person["row_id"], get_person_name(person)) for person in people]

    def on_copy(
        self, old_answer: Answer, new_answer: Answer, old_value: Tuple[str, str]
    ) -> Tuple[str | None, str | None]:
        return on_copy_from_reference_document(old_answer, new_answer, old_value)


class PreliminaryClarificationTargets(BaseDataSource):
    info = "List of services that can be selected for preliminary clarifications in Kt. SO & SG"

    @canton_aware
    def filter_services(self, services):  # pragma: no cover
        raise NotImplementedError()

    def filter_services_so(self, services):
        return services.filter(
            service_group__slug__in=[
                "service-cantonal",
                "service-extra-cantonal",
                "service-bab",
            ],
        )

    def filter_services_sg(self, services):
        return services.filter(service_group__slug__in=["coordination", "service"])

    @data_source_cache(timeout=3600)
    def get_data(self, user, question, context):
        services = (
            Service.objects.select_related("service_group")
            .prefetch_related("trans")
            .filter(service_parent__isnull=True, disabled=False)
        )

        services = self.filter_services(services)

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

    def on_copy(
        self, old_answer: Answer, new_answer: Answer, old_value: Tuple[str, str]
    ) -> Tuple[str | None, str | None]:
        return on_copy_from_reference_document(old_answer, new_answer, old_value)


class ServicesForFinalReport(BaseDataSource):
    info = "Services which asked to be invited to the 'Schlussabnahme' (final report) during the distribution phase"

    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        instance = Instance.objects.get(pk=context.get("instanceId"))

        pks_of_services_to_be_invited = []

        for inquiry in Inquiry.objects.for_instance(instance):
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


class Sanctions(BaseDataSource):
    info = (
        "Selection of uncontrolled sanctions for a given step in the current instance"
    )

    def get_data(self, user, question, context):
        if not context:  # pragma: no cover
            return []

        generic_sanction = (
            None,
            _("All sanctions that could be fulfilled until now have been fullfilled"),
        )

        step = question.meta.get("sanction_step")
        if not step:
            return [generic_sanction]

        sanctions = list(
            Sanction.objects.for_instance_id(context.get("instanceId"))
            .pending()
            .for_step(step)
            .values_list("pk", "name")
        )
        if not sanctions:
            return [generic_sanction]

        return sanctions


class Applicants(BaseDataSource):
    info = "All involved applicants"

    @data_source_cache(timeout=5)
    def get_data(self, user, question, context: dict) -> list[list[str, str]]:
        if not context or "instanceId" not in context:
            return []

        applicants = (
            Applicant.objects.filter(instance_id=context["instanceId"])
            .select_related("invitee")
            .order_by("invitee__name", "invitee__surname", "email")
        )

        return [
            [
                str(applicant.pk),
                applicant.invitee.get_full_name()
                if applicant.invitee
                else applicant.email,
            ]
            for applicant in applicants
        ]
