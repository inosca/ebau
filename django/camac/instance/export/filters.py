from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption, Option
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Case,
    CharField,
    Exists,
    F,
    OuterRef,
    Q,
    QuerySet,
    Subquery,
    Value,
    When,
)
from django.db.models.expressions import Func
from django.db.models.fields import IntegerField
from django.db.models.functions import Cast, Coalesce, Concat, NullIf, Replace, Trim
from django.utils.translation import get_language
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend

from camac.caluma.models import Inquiry
from camac.core.models import InstanceService, WorkflowEntry
from camac.instance.models import FormField, InstanceStateT
from camac.lookups import Any
from camac.responsible.models import ResponsibleService
from camac.user.models import Service, ServiceT


class JsonbText(Func):
    """DB function to cast a JSONB field containing a string to a char field."""

    template = "%(expressions)s #>> '{}'"
    output_field = CharField()


def caluma_answer(slug: str, ref: str = "case__document_id") -> QuerySet:
    """Annotate the answer to a caluma question on a given document as a string.

    This only works for answers to questions of the following types:
    - Text
    - Textarea
    - Choice
    - Dynamic choice (depending on what the data source uses as slug)
    """

    return (
        Answer.objects.filter(question_id=slug, document_id=OuterRef(ref))
        .annotate(string_value=NullIf(Trim(JsonbText(F("value"))), Value("")))
        .values("string_value")[:1]
    )


def camac_ng_answer(name: str) -> QuerySet:
    """Annotate the answer to a camac-ng form field on an instance as a string.

    This only works for form fields that save a string into the JSONB field.
    """
    return (
        FormField.objects.filter(instance_id=OuterRef("pk"), name=name)
        .annotate(string_value=NullIf(Trim(JsonbText(F("value"))), Value("")))
        .values("string_value")[:1]
    )


class StringAggSubquery(Subquery):
    template = "(SELECT STRING_AGG(distinct subquery.%(column_name)s, '%(delimiter)s' ORDER BY subquery.%(column_name)s) FROM (%(subquery)s) AS subquery)"


class ConcatWS(Func):
    function = "CONCAT_WS"
    template = "%(function)s('%(delimiter)s', %(expressions)s)"


class InstanceExportFilterBackend(BaseFilterBackend):
    def annotate_municipality(self):
        return (
            DynamicOption.objects.filter(
                question_id="gemeinde", document_id=OuterRef("case__document_id")
            )
            .order_by("-created_at")
            .values(f"label__{get_language()}")[:1]
        )

    def annotate_instance_state(self):
        return InstanceStateT.objects.filter(
            instance_state_id=OuterRef("instance_state_id"), language=get_language()
        ).values("name")[:1]

    def annotate_building_project(self):
        return caluma_answer("beschreibung-bauvorhaben")

    def annotate_parcels(self):
        return StringAggSubquery(
            Answer.objects.filter(
                question_id="parzellennummer",
                document__family=OuterRef("case__document_id"),
                value__isnull=False,
            )
            .annotate(
                # Return NULL if the answer is empty so this function returns
                # the same on empty answers as on no answer at all.
                string_value=NullIf(
                    Trim(
                        Replace(
                            Cast("value", output_field=CharField()),
                            Value('"'),
                            Value(""),
                        )
                    ),
                    Value(""),
                ),
            )
            .values("string_value"),
            column_name="string_value",
            delimiter=", ",
        )

    def annotate_applicants(self):
        return StringAggSubquery(
            AnswerDocument.objects.filter(
                answer__question_id="personalien-gesuchstellerin",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                is_juristic=Exists(
                    Answer.objects.filter(
                        question_id="juristische-person-gesuchstellerin",
                        document_id=OuterRef("document_id"),
                        value="juristische-person-gesuchstellerin-ja",
                    )
                ),
                name=Case(
                    When(
                        is_juristic=True,
                        then=caluma_answer(
                            "name-juristische-person-gesuchstellerin", "document_id"
                        ),
                    ),
                    default=Trim(
                        Concat(
                            caluma_answer("vorname-gesuchstellerin", "document_id"),
                            Value(" "),
                            caluma_answer("name-gesuchstellerin", "document_id"),
                        )
                    ),
                ),
            )
            .values("name"),
            column_name="name",
            delimiter=", ",
        )

    def annotate_applicants_emails(self):
        return StringAggSubquery(
            AnswerDocument.objects.filter(
                answer__question_id="personalien-gesuchstellerin",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                email=caluma_answer("e-mail-gesuchstellerin", "document_id"),
            )
            .values("email"),
            column_name="email",
            delimiter=", ",
        )

    def filter_instances(self, request, queryset):
        instance_ids = list(
            filter(None, request.query_params.get("instance_id", "").split(","))
        )

        if not instance_ids:
            raise ValidationError("Must provide 'instance_id' query parameter.")
        if len(instance_ids) > 1000:
            raise ValidationError("Maximum 1000 instances allowed at a time.")

        return queryset.filter(pk__in=instance_ids)

    def filter_queryset(self, request, queryset, view):
        queryset = self.filter_instances(request, queryset)

        current_service = request.group.service_id
        language = get_language()

        inquiries = Inquiry.objects.for_instance(OuterRef("pk")).only_active()
        own_inquiries = inquiries.addressed_to(current_service)

        inquiry_in_date = own_inquiries.order_by("child_case__created_at").values(
            "child_case__created_at__date"
        )[:1]

        inquiry_out_date = (
            own_inquiries.only_answered()
            .order_by("-closed_at")
            .values("closed_at__date")[:1]
        )

        inquiry_answer = (
            own_inquiries.only_answered()
            .order_by("-closed_at")
            .annotate(
                label=Answer.objects.filter(
                    question_id=settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
                    document=OuterRef("child_case__document"),
                )
                .annotate(
                    label=Option.objects.filter(
                        # `value` is a JSONBField that when casted to a
                        # CharField will add double quotes around the value. In
                        # order to properly match it with an option we need to
                        # remove those double quotes.
                        pk=Replace(
                            Cast(OuterRef("value"), output_field=CharField()),
                            Value('"'),
                            Value(""),
                        )
                    ).values(f"label__{language}")[:1],
                )
                .values("label")[:1],
            )
            .values("label")[:1]
        )

        def service_name():
            cast = Cast(
                OuterRef("addressed_groups"),
                output_field=ArrayField(IntegerField()),
            )
            if settings.APPLICATION.get("IS_MULTILINGUAL"):
                return ServiceT.objects.filter(
                    Any(F("service_id"), cast), language=language
                )  # pragma: no cover

            return Service.objects.filter(Any(F("pk"), cast))

        involved_services = StringAggSubquery(
            inquiries.annotate(service_name=service_name().values("name")[:1]).values(
                "service_name"
            ),
            column_name="service_name",
            delimiter=", ",
        )

        responsible_user = (
            ResponsibleService.objects.filter(
                instance_id=OuterRef("pk"), service_id=current_service
            )
            .annotate(
                name=Trim(
                    Concat(
                        Trim(F("responsible_user__name")),
                        Value(" "),
                        Trim(F("responsible_user__surname")),
                    )
                )
            )
            .values("name")[:1]
        )

        return queryset.annotate(
            inquiry_in_date=inquiry_in_date,
            inquiry_out_date=inquiry_out_date,
            inquiry_answer=inquiry_answer,
            responsible_user=responsible_user,
            involved_services=involved_services,
        )


class InstanceExportFilterBackendBE(InstanceExportFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        in_rsta_date = InstanceService.objects.filter(
            active=1,
            service__service_group__name="district",
            instance=OuterRef("pk"),
        ).values("activation_date__date")[:1]

        decision_date = Answer.objects.filter(
            question_id="decision-date",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        sb1_date = WorkItem.objects.filter(
            task_id="sb1",
            status=WorkItem.STATUS_COMPLETED,
            case__instance=OuterRef("pk"),
            closed_at__isnull=False,
        ).values("closed_at__date")[:1]

        sb2_date = WorkItem.objects.filter(
            task_id="sb2",
            status=WorkItem.STATUS_COMPLETED,
            case__instance=OuterRef("pk"),
            closed_at__isnull=False,
        ).values("closed_at__date")[:1]

        # We need to put a `NullIf` function around the street and city in order
        # to filter them out properly if empty. This is needed because
        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = Coalesce(
            caluma_answer("standort-migriert"),
            ConcatWS(
                NullIf(
                    ConcatWS(
                        caluma_answer("strasse-flurname"),
                        caluma_answer("nr"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                NullIf(
                    ConcatWS(
                        caluma_answer("plz-grundstueck-v3"),
                        caluma_answer("ort-grundstueck"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                delimiter=", ",
            ),
        )

        tag_names = StringAgg(
            Trim("tags__name"),
            filter=Q(tags__service_id=request.group.service_id),
            ordering=Trim("tags__name"),
            distinct=True,
            delimiter=", ",
            default="",
        )

        return (
            queryset.annotate(
                in_rsta_date=in_rsta_date,
                decision_date=decision_date,
                sb1_date=sb1_date,
                sb2_date=sb2_date,
                municipality=self.annotate_municipality(),
                address=address,
                parcels=self.annotate_parcels(),
                tag_names=tag_names,
                instance_state_name=self.annotate_instance_state(),
                applicants=self.annotate_applicants(),
                applicants_emails=self.annotate_applicants_emails(),
                building_project=self.annotate_building_project(),
            )
            .select_related("case", "case__document", "case__document__form")
            .only(
                "case__family",
                "case__meta",
                "case__document__family",
                "case__document__form",
                "case__document__form__name",
                "instance_state",
            )
        )


class InstanceExportFilterBackendSZ(InstanceExportFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = (
            super().filter_queryset(request, queryset, view).order_by("-identifier")
        )

        intent = Coalesce(
            camac_ng_answer("bezeichnung-override"),
            camac_ng_answer("bezeichnung"),
        )

        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = ConcatWS(
            camac_ng_answer("ortsbezeichnung-des-vorhabens"),
            camac_ng_answer("standort-spezialbezeichnung"),
            camac_ng_answer("standort-ort"),
            delimiter=", ",
        )

        submit_date = (
            WorkflowEntry.objects.filter(instance=OuterRef("pk"), workflow_item_id=10)
            .order_by("workflow_date")
            .values("workflow_date")[:1]
        )

        applicants = Coalesce(
            FormField.objects.filter(
                name="bauherrschaft-override",
                instance_id=OuterRef("pk"),
                value__isnull=False,
            ).values("value")[:1],
            FormField.objects.filter(
                name__in=[
                    "bauherrschaft",
                    "bauherrschaft-v2",
                    "bauherrschaft-v3",
                ],
                instance_id=OuterRef("pk"),
            ).values("value")[:1],
        )

        decision_date_communal = Answer.objects.filter(
            question_id="bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        decision_date_cantonal = Answer.objects.filter(
            question_id="bewilligungsverfahren-datum-gesamtentscheid",
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        return queryset.annotate(
            applicants=applicants,
            intent=intent,
            address=address,
            submit_date=submit_date,
            decision_date_communal=decision_date_communal,
            decision_date_cantonal=decision_date_cantonal,
        ).select_related("form", "instance_state", "location")


class InstanceExportFilterBackendAG(InstanceExportFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        decision_date = Answer.objects.filter(
            question_id="entscheid-datum",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        # We need to put a `NullIf` function around the street and city in order
        # to filter them out properly if empty. This is needed because
        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = ConcatWS(
            NullIf(
                caluma_answer("street-and-housenumber"),
                Value(""),
            ),
            NullIf(
                caluma_answer("ort-grundstueck"),
                Value(""),
            ),
            delimiter=", ",
        )

        return (
            queryset.annotate(
                decision_date=decision_date,
                address=address,
                parcels=self.annotate_parcels(),
                building_project=self.annotate_building_project(),
                applicants=self.annotate_applicants(),
                applicants_emails=self.annotate_applicants_emails(),
                municipality=self.annotate_municipality(),
                instance_state_name=self.annotate_instance_state(),
            )
            .select_related("case", "case__document", "case__document__form")
            .only(
                "case__family",
                "case__meta",
                "case__document__family",
                "case__document__form",
                "case__document__form__name",
                "instance_state",
            )
        )
