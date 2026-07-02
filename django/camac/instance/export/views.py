import json
from typing import TYPE_CHECKING

from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption, Option
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.exceptions import BadRequest
from django.db.models import (
    Case,
    Exists,
    F,
    FilteredRelation,
    OuterRef,
    Q,
    Value,
    When,
)
from django.db.models.functions import Coalesce, Concat, Trim
from django.utils.dateparse import parse_datetime
from django.utils.translation import get_language
from rest_framework.generics import ListAPIView

from camac.instance.export import filters, serializers
from camac.instance.export.filters import StringAggSubquery, caluma_answer
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.response import make_xlsx_response

if TYPE_CHECKING:
    from camac.settings.modules.work_item_list_schema import (
        AnnotationsConfig,
    )


def value_or_dash(x):
    return x or "-"


def caluma_option(outer_ref):
    return Option.objects.filter(pk=OuterRef(outer_ref)).values("label__de")[:1]


def parse_number(val):
    """Attempt to convert a value to int or float; return original if it fails."""
    if not isinstance(val, str):  # pragma: no cover
        return val
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def generate_bab_statistics_export_file(start_date, end_date):
    start_date = parse_datetime(start_date)
    end_date = parse_datetime(end_date)
    qs = Instance.objects

    annotations_config: AnnotationsConfig = settings.WORK_ITEM_LIST.annotations

    qs = (
        # bab document
        qs.filter(case__work_items__document__form_id="bab")
        .annotate(bab_document_id=F("case__work_items__document_id"))
        # remove instances without any bab data
        .filter(Exists(Answer.objects.filter(document_id=OuterRef("bab_document_id"))))
        # time range via circulation start date
        .annotate(
            circulation_start_date=WorkItem.objects.filter(
                case__family=OuterRef("case"),
                task=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                status=WorkItem.STATUS_COMPLETED,
            ).values("closed_at")[:1],
        )
        .filter(
            circulation_start_date__isnull=False,
            circulation_start_date__gte=start_date,
            circulation_start_date__lte=end_date,
        )
        # optional first table (LEFT JOIN with condition in ON)
        .annotate(
            bab_table_answers=FilteredRelation(
                "case__work_items__document__answers",
                condition=Q(
                    case__work_items__document__answers__question_id__in=[
                        "bab-lage-flaechenbedarf-tabelle",
                        "versiegelte-entsiegelte-flaechen",
                    ]
                ),
            )
        )
        .annotate(
            bab_table_1=FilteredRelation(
                "bab_table_answers__documents",
                condition=Q(
                    bab_table_answers__documents__form_id="bab-lage-flaechenbedarf-form"
                ),
            ),
            bab_table_2=FilteredRelation(
                "bab_table_answers__documents",
                condition=Q(
                    bab_table_answers__documents__form_id="bab-versiegelte-entsiegelte-flaechen-form"
                ),
            ),
        )
        .annotate(
            bab_table_1_document_id=F("bab_table_1__pk"),
            bab_table_2_document_id=F("bab_table_2__pk"),
        )
        # annotate instance stuff
        .annotate(
            municipality=DynamicOption.objects.filter(
                question_id="municipality",
                document_id=OuterRef("case__family__document_id"),
            )
            .order_by("-created_at")
            .values("label__de")[:1],
            applicant=StringAggSubquery(
                AnswerDocument.objects.filter(
                    answer__question_id=annotations_config.applicants.table_question,
                    answer__document_id=OuterRef("case__family__document_id"),
                )
                .annotate(
                    is_juristic=Exists(
                        Answer.objects.filter(
                            question_id=annotations_config.applicants.is_juristic,
                            document_id=OuterRef("document_id"),
                            value=annotations_config.applicants.is_juristic_yes,
                        )
                    ),
                    name=Case(
                        When(
                            is_juristic=True,
                            then=Trim(
                                Concat(
                                    caluma_answer(
                                        annotations_config.applicants.juristic_name,
                                        "document_id",
                                    ),
                                    Value(", "),
                                    caluma_answer(
                                        annotations_config.applicants.first_name,
                                        "document_id",
                                    ),
                                    Value(" "),
                                    caluma_answer(
                                        annotations_config.applicants.last_name,
                                        "document_id",
                                    ),
                                    Value(", "),
                                    caluma_answer(
                                        annotations_config.applicants.street,
                                        "document_id",
                                    ),
                                    Value(" "),
                                    caluma_answer(
                                        annotations_config.applicants.street_number,
                                        "document_id",
                                    ),
                                    Value(", "),
                                    caluma_answer(
                                        annotations_config.applicants.zip, "document_id"
                                    ),
                                    Value(" "),
                                    caluma_answer(
                                        annotations_config.applicants.city,
                                        "document_id",
                                    ),
                                )
                            ),
                        ),
                        default=Trim(
                            Concat(
                                caluma_answer(
                                    annotations_config.applicants.first_name,
                                    "document_id",
                                ),
                                Value(" "),
                                caluma_answer(
                                    annotations_config.applicants.last_name,
                                    "document_id",
                                ),
                                Value(", "),
                                caluma_answer(
                                    annotations_config.applicants.street,
                                    "document_id",
                                ),
                                Value(" "),
                                caluma_answer(
                                    annotations_config.applicants.street_number,
                                    "document_id",
                                ),
                                Value(", "),
                                caluma_answer(
                                    annotations_config.applicants.zip, "document_id"
                                ),
                                Value(" "),
                                caluma_answer(
                                    annotations_config.applicants.city,
                                    "document_id",
                                ),
                            ),
                        ),
                    ),
                )
                .values("name"),
                column_name="name",
                delimiter=", ",
            ),
            instance_description=Coalesce(
                *[
                    caluma_answer(desc_slug, "case__family__document_id")
                    for desc_slug in annotations_config.description
                ]
            ),
            instance_name=F(f"case__family__document__form__name__{get_language()}"),
        )
        # annotate bab stuff
        .annotate(
            bab_art_der_massnahme=caluma_answer(
                "bab-art-der-massnahme", "bab_document_id"
            ),
            bab_objektart=caluma_answer("bab-objektart", "bab_document_id"),
            bab_objektbeschrieb=caluma_answer("objektbeschrieb", "bab_document_id"),
            bab_nutzung_nach_rpg=caluma_answer(
                "bab-nutzung-nach-rpg", "bab_document_id"
            ),
            bab_bewilligungsgrund=caluma_answer(
                "bab-bewilligungsgrund", "bab_document_id"
            ),
            bab_entscheid=caluma_answer("bab-entscheid", "bab_document_id"),
            bab_typ_der_auftraggeber=caluma_answer(
                "bab-typ-der-auftraggeber", "bab_document_id"
            ),
            bab_grundnutzung=caluma_answer(
                "bab-grundnutzung", "bab_table_1_document_id"
            ),
            bab_flaechenbedarf_grundnutzung=caluma_answer(
                "bab-flaechenbedarf-grundnutzung", "bab_table_1_document_id"
            ),
            bab_flaechenbedarf_fruchtfolgeflaechen=caluma_answer(
                "bab-flaechenbedarf-fruchtfolgeflaechen", "bab_document_id"
            ),
            bab_kompensation_fruchtfolgeflaechen=caluma_answer(
                "bab-kompensation-fruchtfolgeflaechen", "bab_document_id"
            ),
            bab_neue_gebaeude=caluma_answer("bab-neue-gebaeude", "bab_document_id"),
            bab_gebaeude_abbruch=caluma_answer(
                "bab-gebaeude-abbruch", "bab_document_id"
            ),
            bab_anzahl_gebaeude_unter_schutz=caluma_answer(
                "anzahl-gebaeude-unter-schutz", "bab_document_id"
            ),
            bab_versiegelt_oder_entsiegelt=caluma_answer(
                "versiegelt-oder-entsiegelt", "bab_document_id"
            ),
            bab_art_versiegelung=caluma_answer(
                "bab-art-versiegelung", "bab_table_2_document_id"
            ),
            bab_versiegelung_flaeche=caluma_answer(
                "bab-versiegelung-flaeche", "bab_table_2_document_id"
            ),
            bab_nutzung_versiegelte_flaeche=caluma_answer(
                "bab-nutzung-versiegelte-flaeche", "bab_table_2_document_id"
            ),
            bab_soemmerungsgebiet=caluma_answer(
                "soemmerungsgebiet", "bab_table_2_document_id"
            ),
        )
        # annotations for choice questions
        .annotate(
            bab_art_der_massnahme=caluma_option("bab_art_der_massnahme"),
            bab_objektart=caluma_option("bab_objektart"),
            bab_nutzung_nach_rpg=caluma_option("bab_nutzung_nach_rpg"),
            bab_bewilligungsgrund=caluma_option("bab_bewilligungsgrund"),
            bab_entscheid=caluma_option("bab_entscheid"),
            bab_typ_der_auftraggeber=caluma_option("bab_typ_der_auftraggeber"),
            bab_grundnutzung=caluma_option("bab_grundnutzung"),
            bab_versiegelt_oder_entsiegelt=caluma_option(
                "bab_versiegelt_oder_entsiegelt"
            ),
            bab_art_versiegelung=caluma_option("bab_art_versiegelung"),
            bab_nutzung_versiegelte_flaeche=caluma_option(
                "bab_nutzung_versiegelte_flaeche"
            ),
            bab_soemmerungsgebiet=caluma_option("bab_soemmerungsgebiet"),
        )
    )

    header = [
        "Gemeinde",
        "Gesuchsteller",
        "Beschrieb",
        "Dossier-Nr.",
        "ID",
        "Verfahrenstyp",
        "Art der Massnahme",
        "Objektart",
        "Objektbeschrieb",
        "Nutzung nach RPG",
        "Bewilligungsgrund - Rechtliche Grundlage RPG / RPV",
        "Entscheid",
        "Typ der Auftraggeber - Gesuchsteller (gemäss GWR)",
        "Lage / Flächenbedarf: Grundnutzung",
        "Lage / Flächenbedarf: Flächenbedarf nach Grundnutzung (m²)",
        "Flächenbedarf Fruchtfolgeflächen (m²)",
        "Kompensation Fruchtfolgeflächen (m²)",
        "Anzahl neue Gebäude (neu erstellte Bauten)",
        "Anzahl Gebäude die abgebrochen werden",
        "Anzahl Gebäude die neu unter Schutz gestellt wurden",
        "Werden Flächen neu versiegelt oder entsiegelt?",
        "Versiegelte / entsiegelte Flächen: Art der Ver- bzw. Entsiegelung",
        "Versiegelte / entsiegelte Flächen: Fläche (m²)",
        "Versiegelte / entsiegelte Flächen: Nutzung der versiegelten Flächen",
        "Versiegelte / entsiegelte Flächen: Liegt das Vorhaben in einem Sömmerungsgebiet",
    ]

    data = []

    for row in qs:
        data.append(
            [
                value_or_dash(row.municipality),
                value_or_dash(row.applicant),
                value_or_dash(row.instance_description),
                str(row.case.meta["dossier-number"]),
                str(row.pk),
                value_or_dash(row.instance_name),
                value_or_dash(row.bab_art_der_massnahme),
                value_or_dash(row.bab_objektart),
                value_or_dash(row.bab_objektbeschrieb),
                value_or_dash(row.bab_nutzung_nach_rpg),
                value_or_dash(row.bab_bewilligungsgrund),
                value_or_dash(row.bab_entscheid),
                value_or_dash(row.bab_typ_der_auftraggeber),
                value_or_dash(row.bab_grundnutzung),
                value_or_dash(row.bab_flaechenbedarf_grundnutzung),
                value_or_dash(row.bab_flaechenbedarf_fruchtfolgeflaechen),
                value_or_dash(row.bab_kompensation_fruchtfolgeflaechen),
                value_or_dash(row.bab_neue_gebaeude),
                value_or_dash(row.bab_gebaeude_abbruch),
                value_or_dash(row.bab_anzahl_gebaeude_unter_schutz),
                value_or_dash(row.bab_versiegelt_oder_entsiegelt),
                value_or_dash(row.bab_art_versiegelung),
                value_or_dash(row.bab_versiegelung_flaeche),
                value_or_dash(row.bab_nutzung_versiegelte_flaeche),
                value_or_dash(row.bab_soemmerungsgebiet),
            ]
        )
    return header, data


class InstanceExportView(InstanceQuerysetMixin, ListAPIView):
    instance_field = None
    queryset = Instance.objects

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()

    def get_serializer_class(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return serializers.InstanceExportSerializerBE
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return serializers.InstanceExportSerializerSZ
        elif settings.APPLICATION_NAME == "kt_ag":
            return serializers.InstanceExportSerializerAG
        elif settings.APPLICATION_NAME == "kt_gr":
            return serializers.InstanceExportSerializerGR

        return serializers.InstanceExportSerializer  # pragma: no cover

    @property
    def filter_backends(self):
        if settings.APPLICATION_NAME == "kt_bern":
            return [filters.InstanceExportFilterBackendBE]
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return [filters.InstanceExportFilterBackendSZ]
        elif settings.APPLICATION_NAME == "kt_ag":
            return [filters.InstanceExportFilterBackendAG]
        elif settings.APPLICATION_NAME == "kt_gr":
            return [filters.InstanceExportFilterBackendGR]

        return [filters.InstanceExportFilterBackend]  # pragma: no cover

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        return make_xlsx_response(data, "export.xlsx")


class BabStatisticsExportView(InstanceQuerysetMixin, ListAPIView):
    queryset = Instance.objects

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()

    def post(self, request):
        payload = json.loads(request.body)
        start_date = payload.get("from")
        end_date = payload.get("to")

        if not start_date or not end_date:  # pragma: no cover
            raise BadRequest("Both 'from' and 'to' dates are required")

        # We delete table answers where the document is null because they cause problems for the
        # creation of the excel file
        Answer.objects.filter(
            question_id__in=[
                "bab-lage-flaechenbedarf-tabelle",
                "versiegelte-entsiegelte-flaechen",
            ],
            documents__isnull=True,
        ).delete()

        header, data = generate_bab_statistics_export_file(
            start_date=start_date, end_date=end_date
        )

        cleaned_data = [[parse_number(cell) for cell in row] for row in data]

        sheet_data = [header] + cleaned_data

        return make_xlsx_response(sheet_data, "export.xlsx")
