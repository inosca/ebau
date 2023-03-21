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

from camac.core.models import InstanceService, WorkflowEntry
from camac.instance.models import FormField, InstanceStateT
from camac.responsible.models import ResponsibleService
from camac.user.models import Service, ServiceT


class StringAggSubquery(Subquery):
    template = "(SELECT STRING_AGG(distinct subquery.%(column_name)s, '%(delimiter)s' ORDER BY subquery.%(column_name)s) FROM (%(subquery)s) AS subquery)"


class ConcatWS(Func):
    function = "CONCAT_WS"
    template = "%(function)s('%(delimiter)s', %(expressions)s)"


class InstanceExportFilterBackend(BaseFilterBackend):
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

        inquiries = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            case__family__instance=OuterRef("pk"),
        ).exclude(
            status=[
                WorkItem.STATUS_CANCELED,
                WorkItem.STATUS_SUSPENDED,
            ]
        )

        own_inquiries = inquiries.filter(
            addressed_groups__contains=[str(current_service)]
        )

        inquiry_in_date = own_inquiries.order_by("child_case__created_at").values(
            "child_case__created_at__date"
        )[:1]

        inquiry_out_date = (
            own_inquiries.filter(status=WorkItem.STATUS_COMPLETED)
            .order_by("-closed_at")
            .values("closed_at__date")[:1]
        )

        inquiry_answer = (
            own_inquiries.filter(status=WorkItem.STATUS_COMPLETED)
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

        def service_name(pk_query):
            if settings.APPLICATION.get("IS_MULTILINGUAL"):
                return ServiceT.objects.filter(
                    service_id=pk_query, language=language
                )  # pragma: no cover

            return Service.objects.filter(pk=pk_query)

        involved_services = StringAggSubquery(
            inquiries.annotate(
                service_name=service_name(
                    Func(
                        Cast(
                            OuterRef("addressed_groups"),
                            output_field=ArrayField(IntegerField()),
                        ),
                        function="ANY",
                    )
                ).values("name")[:1]
            ).values("service_name"),
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

        current_service = request.group.service_id
        language = get_language()

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

        municipality = (
            DynamicOption.objects.filter(
                question_id="gemeinde", document_id=OuterRef("case__document_id")
            )
            .order_by("-created_at")
            .values(f"label__{language}")[:1]
        )

        answer = (
            lambda slug, ref="case__document_id": Answer.objects.filter(
                question_id=slug,
                document_id=OuterRef(ref),
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
            .values("string_value")[:1]
        )

        # We need to put a `NullIf` function around the street and city in order
        # to filter them out properly if empty. This is needed because
        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = Coalesce(
            answer("standort-migriert"),
            ConcatWS(
                NullIf(
                    ConcatWS(
                        answer("strasse-flurname"),
                        answer("nr"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                NullIf(
                    ConcatWS(
                        answer("plz-grundstueck-v3"),
                        answer("ort-grundstueck"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                delimiter=", ",
            ),
        )

        applicants = StringAggSubquery(
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
                        then=answer(
                            "name-juristische-person-gesuchstellerin", "document_id"
                        ),
                    ),
                    default=Trim(
                        Concat(
                            answer("vorname-gesuchstellerin", "document_id"),
                            Value(" "),
                            answer("name-gesuchstellerin", "document_id"),
                        )
                    ),
                ),
            )
            .values("name"),
            column_name="name",
            delimiter=", ",
        )

        tag_names = StringAgg(
            Trim("tags__name"),
            filter=Q(tags__service_id=current_service),
            ordering=Trim("tags__name"),
            distinct=True,
            delimiter=", ",
        )

        instance_state_name = InstanceStateT.objects.filter(
            instance_state_id=OuterRef("instance_state_id"), language=language
        ).values("name")[:1]

        return (
            queryset.annotate(
                in_rsta_date=in_rsta_date,
                decision_date=decision_date,
                municipality=municipality,
                address=address,
                tag_names=tag_names,
                instance_state_name=instance_state_name,
                applicants=applicants,
            )
            .select_related("case", "case__document", "case__document__form")
            .only(
                "case__family",
                "case__meta",
                "case__document__family",
                "case__document__form",
                "case__document__form__name",
            )
        )


class InstanceExportFilterBackendSZ(InstanceExportFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = (
            super().filter_queryset(request, queryset, view).order_by("-identifier")
        )

        answer = (
            lambda name: FormField.objects.filter(
                instance_id=OuterRef("pk"),
                name=name,
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
            .values("string_value")[:1]
        )

        intent = Coalesce(answer("bezeichnung-override"), answer("bezeichnung"))

        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = ConcatWS(
            answer("ortsbezeichnung-des-vorhabens"),
            answer("standort-spezialbezeichnung"),
            answer("standort-ort"),
            delimiter=", ",
        )

        submit_date = (
            WorkflowEntry.objects.filter(instance=OuterRef("pk"), workflow_item_id=10)
            .order_by("workflow_date")
            .values("workflow_date")[:1]
        )

        # TODO: applicants

        decision_date_communal = Answer.objects.filter(
            question_id="bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        decision_date_cantonal = Answer.objects.filter(
            question_id="bewilligungsverfahren-datum-gesamtentscheid",
            document__work_item__case__instance=OuterRef("pk"),
        ).values("date")[:1]

        return queryset.annotate(
            # TODO: applicants=applicants,
            intent=intent,
            address=address,
            submit_date=submit_date,
            decision_date_communal=decision_date_communal,
            decision_date_cantonal=decision_date_cantonal,
        ).select_related("form", "instance_state", "location")
