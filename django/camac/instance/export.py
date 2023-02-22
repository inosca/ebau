import csv

import django_excel
from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption, Option
from caluma.caluma_workflow.models import WorkItem
from dateutil.parser import parse as dateutil_parse
from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
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
from django.utils.translation import get_language, gettext as _
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from camac.core.models import InstanceService
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance, InstanceStateT
from camac.responsible.models import ResponsibleService
from camac.user.models import ServiceT


class StringAggSubquery(Subquery):
    template = "(SELECT STRING_AGG(distinct subquery.%(column_name)s, '%(delimiter)s' ORDER BY subquery.%(column_name)s) FROM (%(subquery)s) AS subquery)"


class ConcatWS(Func):
    function = "CONCAT_WS"
    template = "%(function)s('%(delimiter)s', %(expressions)s)"


class SubmitDateField(serializers.DateField):
    """Custom date field that can parse a string value to a proper date."""

    def to_representation(self, value):
        if not value:  # pragma: no cover
            return None

        return super().to_representation(dateutil_parse(value).date())


class InstanceExportListSerializer(serializers.ListSerializer):
    """Custom list serializer that prepends a row of field labels to the data."""

    def to_representation(self, data):
        header = [field.label for field in self.child.fields.values()]
        rows = [list(row.values()) for row in super().to_representation(data)]

        return [header] + rows


class InstanceExportSerializer(serializers.Serializer):
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
    submit_date = SubmitDateField(
        source="case.meta.submit-date",
        format=settings.SHORT_DATE_FORMAT,
        label=_("Submission Date"),
    )
    instance_state_name = serializers.CharField(label=_("Status"))
    responsible_user = serializers.CharField(label=_("Responsible"))
    applicants = serializers.CharField(label=_("Applicant"))
    municipality = serializers.CharField(label=_("Municipality"))
    district = serializers.SerializerMethodField(label=_("Administrative District"))
    region = serializers.SerializerMethodField(label=_("Administrative Region"))
    in_rsta_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Arrival RSTA"),
    )
    inquiry_in_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Arrival Department"),
    )
    inquiry_out_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Departure Department"),
    )
    decision_date = serializers.DateField(
        format=settings.SHORT_DATE_FORMAT,
        label=_("Decision"),
    )
    inquiry_answer = serializers.CharField(label=_("Assessment"))
    involved_services = serializers.CharField(label=_("Involved Departments"))
    tags = serializers.CharField(source="tag_names", label=_("Tags"))

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

    class Meta:
        list_serializer_class = InstanceExportListSerializer


class InstanceExportView(ListAPIView, InstanceQuerysetMixin):
    instance_field = None
    queryset = Instance.objects.all()
    serializer_class = InstanceExportSerializer

    def annotate_queryset(self, queryset):
        current_service = self.request.group.service_id
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

        inquiry_in_date = own_inquiries.order_by("created_at").values(
            "created_at__date"
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

        involved_services = StringAggSubquery(
            inquiries.annotate(
                service_name=ServiceT.objects.filter(
                    service_id=Func(
                        Cast(
                            OuterRef("addressed_groups"),
                            output_field=ArrayField(IntegerField()),
                        ),
                        function="ANY",
                    ),
                    language=language,
                ).values("name")[:1]
            ).values("service_name"),
            column_name="service_name",
            delimiter=", ",
        )

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

        return (
            queryset.annotate(
                in_rsta_date=in_rsta_date,
                decision_date=decision_date,
                inquiry_in_date=inquiry_in_date,
                inquiry_out_date=inquiry_out_date,
                inquiry_answer=inquiry_answer,
                municipality=municipality,
                address=address,
                tag_names=tag_names,
                instance_state_name=instance_state_name,
                responsible_user=responsible_user,
                applicants=applicants,
                involved_services=involved_services,
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

    def get(self, request):
        instance_ids = [
            int(instance_id)
            for instance_id in self.request.query_params.get("instance_id", "").split(
                ","
            )
            if instance_id
        ]

        if not instance_ids:
            return Response(
                "Must provide 'instance_id' query parameter.", HTTP_400_BAD_REQUEST
            )
        if len(instance_ids) > 1000:
            return Response(
                "Maximum 1000 instances allowed at a time.", HTTP_400_BAD_REQUEST
            )

        queryset = self.annotate_queryset(
            self.get_queryset().filter(pk__in=instance_ids)
        )
        data = self.get_serializer(queryset, many=True).data

        return django_excel.make_response(django_excel.pe.Sheet(data), file_type="xlsx")
