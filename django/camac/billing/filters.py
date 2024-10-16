from caluma.caluma_form.models import Answer
from django.conf import settings
from django.db.models import (
    CharField,
    OuterRef,
    Value,
)
from django.db.models.functions import Cast, Coalesce, NullIf, Replace, Trim
from django.utils.translation import gettext
from django_filters.rest_framework import DateFilter, FilterSet
from rest_framework.filters import BaseFilterBackend
from rest_framework.serializers import ValidationError

from camac.billing.models import BillingV2Entry
from camac.instance.export.filters import ConcatWS, StringAggSubquery


class BillingV2EntryFilterSet(FilterSet):
    date_added_before = DateFilter(field_name="date_added", lookup_expr="lte")
    date_added_after = DateFilter(field_name="date_added", lookup_expr="gte")

    class Meta:
        model = BillingV2Entry
        fields = [
            "instance",
            "date_added_before",
            "date_added_after",
        ]


class BillingV2EntryExportFilterBackend(BaseFilterBackend):
    def _validate_qs_size(self, queryset):
        if queryset.count() > settings.BILLING_EXPORT_MAX_RECORDS:  # pragma: no cover
            raise ValidationError(
                gettext(
                    "Too many records in output. Reduce "
                    "data range using filters to below {max}",
                ).format(
                    max=settings.BILLING_EXPORT_MAX_RECORDS,
                )
            )

    def filter_queryset(self, request, queryset, view):
        self._validate_qs_size(queryset)

        def get_answer(
            slug: str,
            ref: str = "instance__case__document_id",
            all_answers: bool = False,
        ):
            """
            Fetch answers filtered by a question ID and document reference, optionally fetching all answers.

            Args:
                slug (str): The question ID to filter answers.
                ref (str, optional): The reference field for the document. Defaults to 'instance__case__document_id'.
                all_answers (bool, optional): If True, fetch all answers by document family,
                                            otherwise fetch the first one by document ID. Defaults to False.

            Returns:
                QuerySet: A queryset containing the string values of the answers.
            """
            document_key = "document__family" if all_answers else "document_id"
            filter_kwargs = {
                "question_id": slug,
                document_key: OuterRef(ref),
            }

            queryset = (
                Answer.objects.filter(**filter_kwargs)
                .annotate(
                    string_value=NullIf(
                        Trim(
                            Replace(
                                Cast("value", output_field=CharField()),
                                Value('"'),
                                Value(""),
                            )
                        ),
                        Value(""),
                    )
                )
                .values("string_value")
            )

            # We don't join to the answerdoc, but enforce explicit order by
            # rowdocument's creation date. This is precise enough to ensure
            # all columns in output will be sorted in the same way
            queryset = queryset.order_by("document__created_at")

            return queryset if all_answers else queryset[:1]

        # We need to put a `NullIf` function around the street and city in order
        # to filter them out properly if empty. This is needed because
        # `CONCAT_WS` always returns a string, even if all concatenated values
        # are empty.
        address = Coalesce(
            get_answer("standort-migriert"),
            ConcatWS(
                NullIf(
                    ConcatWS(
                        get_answer("strasse-flurname"),
                        get_answer("nr"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                NullIf(
                    ConcatWS(
                        get_answer("plz-grundstueck-v3"),
                        get_answer("ort-grundstueck"),
                        delimiter=" ",
                    ),
                    Value(""),
                ),
                delimiter=", ",
            ),
        )

        parcels = StringAggSubquery(
            get_answer(slug="parzellennummer", all_answers=True),
            column_name="string_value",
            delimiter=", ",
        )

        coordinate_X = StringAggSubquery(
            get_answer(slug="lagekoordinaten-ost", all_answers=True),
            column_name="string_value",
            delimiter=", ",
        )

        coordinate_Y = StringAggSubquery(
            get_answer(slug="lagekoordinaten-nord", all_answers=True),
            column_name="string_value",
            delimiter=", ",
        )

        return queryset.annotate(
            address=address,
            parcels=parcels,
            coordinate_X=coordinate_X,
            coordinate_Y=coordinate_Y,
        )
