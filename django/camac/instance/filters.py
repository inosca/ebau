import re
from functools import reduce

from caluma.caluma_form.filters import SearchAnswersFilter
from caluma.caluma_form.models import Answer, Document, Option
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import EMPTY_VALUES
from django.db.models import (
    Case as DjangoCase,
    Exists,
    F,
    Func,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import RawSQL
from django.db.models.fields import CharField, TextField
from django.db.models.functions import Cast, Coalesce, Replace
from django.utils.translation import get_language
from django_filters.rest_framework import (
    BaseInFilter,
    BooleanFilter,
    CharFilter,
    DateFilter,
    Filter,
    FilterSet,
    NumberFilter,
)
from rest_framework.filters import BaseFilterBackend, OrderingFilter

from camac.caluma.utils import visible_inquiries_expression
from camac.constants import kt_uri as uri_constants
from camac.filters import (
    CharMultiValueFilter,
    JSONFieldMultiValueFilter,
    NumberMultiValueFilter,
)
from camac.instance.export.filters import StringAggSubquery

from ..core import models as core_models
from ..responsible import models as responsible_models
from . import models


class ResponsibleUserFilter(CharFilter):
    def filter(self, qs, value):
        if value.lower() == "nobody":
            return qs.filter(**{f"{self.field_name}__isnull": True})
        return super().filter(qs, value)


class ResponsibleServiceFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        active_services = core_models.InstanceService.objects.filter(
            active=1,
            service=value,
            **(
                settings.APPLICATION.get("ACTIVE_SERVICES", {})
                .get("MUNICIPALITY", {})
                .get("FILTERS", {})
            ),
        )

        return qs.filter(pk__in=active_services.values("instance_id"))


class ResponsibleServiceUserFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        # restrict to service from request header
        current_service = self.parent.request.group.service

        if value.lower() == "nobody":
            return qs.exclude(
                # exclude all instances which have responsible services
                pk__in=responsible_models.ResponsibleService.objects.filter(
                    service=current_service
                ).values("instance")
            )

        return qs.filter(
            # restrict to current service
            responsible_services__service=current_service,
            responsible_services__responsible_user=value,
        )


class CirculationStateFilter(NumberMultiValueFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value:
            return qs.filter(
                circulations__activations__service=self.parent.request.group.service,
                circulations__activations__circulation_state__pk__in=value,
            )

        return super().filter(qs, value)


class FormNameFilter(CharFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value and value.startswith("-"):
            return qs.exclude(form__name=value[1:])

        return super().filter(qs, value)


class InstanceStateFilterSet(FilterSet):
    instance_state_id = NumberMultiValueFilter()

    class Meta:
        model = models.InstanceState
        fields = ("name", "instance_state_id")


class FormFieldListValueFilter(Filter):
    """
    Filter a JSON field containing a list of values.

    For certain instance form field values the data contained in the
    JSONField is a list of objects, which has the following structure:

        [
            {"name": "jupiter", "size": "large", "color": "yellow"},
            {"name": "mercury", "size": "small", "color": "grey"},
        ]

    This filter allows lookups to be performed on specific
    values in a list of JSON objects. Using the django json field
    filter lookup __contains does not allow for substring searches
    on list values, it only matches the entire key value pair, such
    as for example { "name": "jupiter" }.

    Filter Example:

    Three instance form fields with the name "planets" where the
    json field "value" contains a list:

        Instance 1, form field 1, value: [
            {"name": "jupiter", "size": "large", "color": "yellow"},
            {"name": "mercury", "size": "small", "color": "grey"},
        ],
        Instance 2, form field 2, value: [
            {"name": "mars", "size": "medium", "color": "red"},
        ]
        Instance 3, form field 3, value: [
            {"name": "earth", "size": "medium", "color": "blue"}
        ]

    Filter configuration on the instance model:
        planet = FormFieldListValueFilter(
                    form_field_names=["planets"],
                    keys=["name", "color"]
                )

    Using the filter "planet=u" on the api endpoint "instances" will
    match the following instances:

        Instance 1 (form field 1, due to "name": "jupiter" and "name": "mercury"),
        Instance 3 (form field 3, due to "color": "blue")

    The filter considers all keys if multiple keys are given.
    """

    def __init__(self, form_field_names, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._form_field_names = form_field_names
        self._keys = keys

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        form_fields = models.FormField.objects.all()

        # Use alias() instead of annotate() to only calculate expression if
        # the form field has to be checked for the instance query.
        # In addition, the form field name doesn't have to be prefiltered,
        # since the expression is only evaluated in the instance query where
        # the form field name is checked.
        for key in self._keys:
            form_fields = form_fields.alias(
                **{
                    f"values_{key}": RawSQL(
                        f"""
                            select array_agg({key})
                            from jsonb_to_recordset(value) as ({key} text)
                        """,
                        (),
                        ArrayField(TextField()),
                    ),
                }
            )

        filters = []
        search_values = filter(None, value.strip().split(" "))
        for v in search_values:
            subfilters = [Q(**{f"values_{key}__icontains": v}) for key in self._keys]
            filters.append(reduce(lambda a, b: a | b, subfilters))

        return qs.filter(
            # Use exists() since the instance should be returned as long
            # as at least one form field contains the search value, which
            # limits the searched form fields to the ones contained in
            # the instance queryset and allows the subquery to be terminated
            # as soon as one form field of the instance is found that
            # fulfills the condition.
            Exists(
                form_fields.filter(
                    Q(instance__pk=OuterRef("pk"))
                    & Q(name__in=self._form_field_names)
                    & Q(value__isnull=False)
                    & reduce(lambda a, b: a & b, filters)
                )
            )
        )


class InstanceKeywordSearchFilter(CharFilter):
    def get_processed_form_fields(self):
        # The form fields are converted to a text field,
        # concatenated and then stripped of certain content
        # to make the keyword search more accurate.

        # Remove uuid key / value pairs, which occur in table fields
        regex_uuid = Value(r'(, )?"uuid": "(\w|-)+"')
        # Remove keys which occur in table fields
        regex_keys = Value(r'"(\w|-)+": ')
        # Remove null values in table fields that are casted
        # to the string "null"
        regex_null = Value(r"null")
        # Remove escaping of quotes that are casted to \\"
        regex_escaped_quotes = Value(r'\\"')
        regex_flags = Value("gm")

        regex_replacement_mapping = [
            (regex_uuid, Value(r"")),
            (regex_keys, Value(r"")),
            (regex_null, Value(r'""')),
            (regex_escaped_quotes, Value(r'"')),
        ]

        def regexp_replace(value, regex, replacement):
            return Func(
                value,
                regex,
                replacement,
                regex_flags,
                function="REGEXP_REPLACE",
                output_field=TextField(),
            )

        processed_form_fields = Coalesce(
            StringAggSubquery(
                models.FormField.objects.get_queryset()
                .filter(
                    instance=OuterRef("pk"),
                    value__isnull=False,
                )
                .visible_for(self.parent.request)
                .annotate(value_as_text=Cast(F("value"), TextField()))
                .values("value_as_text"),
                column_name="value_as_text",
                delimiter="|",
            ),
            Value(""),
            output_field=TextField(),
        )

        # Apply all regex replacements to form field query
        for regex, replacement in regex_replacement_mapping:
            processed_form_fields = regexp_replace(
                processed_form_fields, regex, replacement
            )

        return processed_form_fields

    def get_processed_journal_entries(self):
        return Coalesce(
            StringAggSubquery(
                models.JournalEntry.objects.filter(
                    instance=OuterRef("pk"),
                    text__isnull=False,
                )
                .visible_for(self.parent.request)
                .values("text"),
                column_name="text",
                delimiter="|",
            ),
            Value(""),
            output_field=TextField(),
        )

    def get_processed_inquiry_answers(self):
        return Coalesce(
            StringAggSubquery(
                WorkItem.objects.filter(
                    visible_inquiries_expression(self.parent.request.group),
                    case__family__instance=OuterRef("pk"),
                    status=WorkItem.STATUS_COMPLETED,
                )
                .annotate(
                    answers=StringAggSubquery(
                        Answer.objects.filter(
                            question_id__in=[
                                settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
                                settings.DISTRIBUTION["QUESTIONS"]["REQUEST"],
                                settings.DISTRIBUTION["QUESTIONS"]["ANCILLARY_CLAUSES"],
                                settings.DISTRIBUTION["QUESTIONS"]["REASON"],
                                settings.DISTRIBUTION["QUESTIONS"]["RECOMMENDATION"],
                                settings.DISTRIBUTION["QUESTIONS"]["HINT"],
                            ],
                            document=OuterRef("child_case__document"),
                        )
                        .annotate(
                            value_as_text=DjangoCase(
                                When(
                                    question_id=settings.DISTRIBUTION["QUESTIONS"][
                                        "STATUS"
                                    ],
                                    then=Option.objects.filter(
                                        # `value` is a JSONBField that when casted to a
                                        # CharField will add double quotes around the value. In
                                        # order to properly match it with an option we need to
                                        # remove those double quotes.
                                        pk=Replace(
                                            Cast(
                                                OuterRef("value"),
                                                output_field=CharField(),
                                            ),
                                            Value('"'),
                                            Value(""),
                                        )
                                    ).values(f"label__{get_language()}")[:1],
                                ),
                                default=Cast(F("value"), TextField()),
                            )
                        )
                        .values("value_as_text"),
                        column_name="value_as_text",
                        delimiter="|",
                    ),
                )
                .values("answers"),
                column_name="answers",
                delimiter="|",
            ),
            Value(""),
            output_field=TextField(),
        )

    def get_processed_issues(self):
        return Coalesce(
            StringAggSubquery(
                models.Issue.objects.filter(
                    instance=OuterRef("pk"),
                    text__isnull=False,
                )
                .visible_for(self.parent.request)
                .values("text"),
                column_name="text",
                delimiter="|",
            ),
            Value(""),
            output_field=TextField(),
        )

    def filter(self, queryset, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return queryset

        # Input values are split by whitespace.
        # Word groups surrounded by double quotes are
        # treated as a single entity.
        processed_values = [v.strip('"') for v in re.findall(r"(?:\".*?\"|\S)+", value)]

        # Disregard searches that contain a search term
        # which has less than 3 characters
        for val in processed_values:
            if len(val) < 3:
                return queryset.none()

        return self.filter_queryset(processed_values, queryset, value)

    def filter_queryset(self, processed_values, queryset, value):
        # All search terms must be contained in either
        # the form, journal entries or inquiry answers
        filters = Q()
        for val in processed_values:
            filters &= (
                Q(processed_form_fields__icontains=val)
                | Q(processed_journal_entries__icontains=val)
                | Q(processed_inquiry_answers__icontains=val)
                | Q(processed_issues__icontains=val)
            )

        return queryset.annotate(
            processed_form_fields=self.get_processed_form_fields(),
            processed_journal_entries=self.get_processed_journal_entries(),
            processed_inquiry_answers=self.get_processed_inquiry_answers(),
            processed_issues=self.get_processed_issues(),
        ).filter(filters)


class CalumaInstanceKeywordSearchFilter(InstanceKeywordSearchFilter):
    def get_answers(self, queryset, value):
        form_slug_list = settings.APPLICATION["CALUMA"]["INTERNAL_FORMS"]
        # Implemented for internal instances that have only one Document attached
        # to the main Case and the visibility is restricted through InstanceQuerysetMixin
        # For extension for instances with Documents visible to multiple services,
        # visibility restriction needs to be implemented.
        document_queryset = Document.objects.filter(case__instance__in=queryset)
        search_value = [{"questions": [], "forms": form_slug_list, "value": value}]
        return SearchAnswersFilter(document_id="pk").filter(
            document_queryset, search_value
        )

    def filter_queryset(self, processed_values, queryset, value):
        # All search terms must be contained in either
        # the issues,  journal entries or inquiry answers
        filtered_documents = self.get_answers(queryset, value)
        filters = Q()
        for val in processed_values:
            filters &= Q(processed_journal_entries__icontains=val)

        filters = filters | Q(case__document__in=filtered_documents)

        return queryset.annotate(
            processed_journal_entries=self.get_processed_journal_entries(),
        ).filter(filters)


class InstanceSubmitDateFilter(DateFilter):
    def filter(self, qs, value, *args, **kwargs):
        if not value:
            return qs

        return qs.filter(
            **{
                "workflowentry__workflow_item_id": 10,  # Submit date
                f"workflowentry__workflow_date__date__{self.lookup_expr}": value,
            }
        )


class DecisionDateFilter(DateFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        answers = Answer.objects.filter(
            question_id="decision-date",
            document__work_item__task_id="decision",
            document__work_item__status__in=[
                WorkItem.STATUS_COMPLETED,
                WorkItem.STATUS_SKIPPED,
            ],
            **{f"date__{self.lookup_expr}": value},
        )

        return qs.filter(
            pk__in=list(
                answers.values_list(
                    "document__work_item__case__instance__pk", flat=True
                )
            )
        )


class DecisionFilter(BaseInFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        answers = Answer.objects.filter(
            question_id=settings.DECISION["QUESTIONS"]["DECISION"],
            document__work_item__task_id=settings.DECISION["TASK"],
            document__work_item__status__in=[
                WorkItem.STATUS_COMPLETED,
                WorkItem.STATUS_SKIPPED,
            ],
            value__in=value,
        )

        return qs.filter(
            pk__in=list(
                answers.values_list(
                    "document__work_item__case__instance__pk", flat=True
                )
            )
        )


class OerebLegalStateFilter(CharFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        answers = Answer.objects.filter(
            question_id="typ-des-verfahrens",
            value__in=value.split(","),
        )

        return qs.filter(
            pk__in=list(
                answers.values_list("document__case__family__instance__pk", flat=True)
            )
        )


class InquiryStateFilter(CharFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        if value == "pending":
            inquiries = WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                addressed_groups__contains=[str(self.parent.request.group.service_id)],
                status=WorkItem.STATUS_READY,
            )

        elif value == "completed":
            # instances are considered completed if they have at least one completed
            # or skipped inquiry, and no ready inquiry in the same case.
            inquiries = WorkItem.objects.annotate(
                has_open_sibling_inquiry=Exists(
                    WorkItem.objects.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                        status=WorkItem.STATUS_READY,
                        addressed_groups__contains=[
                            str(self.parent.request.group.service_id)
                        ],
                        case=OuterRef("case"),
                    )
                )
            ).filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                addressed_groups__contains=[str(self.parent.request.group.service_id)],
                status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
                has_open_sibling_inquiry=False,
            )

        return qs.filter(
            pk__in=list(inquiries.values_list("case__family__instance__pk", flat=True))
        )


class InquiryDateFilter(DateFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        inquiries = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            addressed_groups__contains=[str(self.parent.request.group.service_id)],
            status__in=[
                WorkItem.STATUS_READY,
                WorkItem.STATUS_COMPLETED,
                WorkItem.STATUS_SKIPPED,
            ],
            **{self.lookup_expr: value},
        )

        if self.lookup_expr.startswith("closed_at"):
            inquiries = inquiries.filter(closed_at__isnull=False)

        return qs.filter(
            pk__in=list(inquiries.values_list("case__family__instance__pk", flat=True))
        )


class InquiryAnswerFilter(BaseInFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        answers = Answer.objects.filter(
            question_id=settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
            value__in=value,
            document__case__parent_work_item__task_id=settings.DISTRIBUTION[
                "INQUIRY_TASK"
            ],
            document__case__parent_work_item__addressed_groups__contains=[
                str(self.parent.request.group.service_id)
            ],
            document__case__parent_work_item__status__in=[
                WorkItem.STATUS_READY,
                WorkItem.STATUS_COMPLETED,
                WorkItem.STATUS_SKIPPED,
            ],
        )

        return qs.filter(
            pk__in=list(
                answers.values_list("document__case__family__instance__pk", flat=True)
            )
        )


class CalumaYesNoFilter(BooleanFilter):
    def __init__(self, question, yes="yes", no="no", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.question = question
        self.yes = yes
        self.no = no

    def filter(self, queryset, value):
        if value in EMPTY_VALUES:
            return queryset

        yes_no_value = "-".join([self.question, self.yes if value else self.no])

        return queryset.filter(
            **{
                "case__document__answers__question_id": self.question,
                "case__document__answers__value": yes_no_value,
            }
        )


class InstanceFilterSet(FilterSet):
    instance_id = NumberMultiValueFilter()
    identifier = CharFilter(field_name="identifier", lookup_expr="icontains")
    # identifier to search instance for linking
    identifier_for_linking = CharFilter(field_name="identifier", lookup_expr="exact")
    service = NumberFilter(method="filter_circulation_service")
    creation_date_after = DateFilter(
        field_name="creation_date__date", lookup_expr="gte"
    )
    tags = CharMultiValueFilter(field_name="tags__name", lookup_expr="all")
    keywords = CharMultiValueFilter(field_name="keywords__name", lookup_expr="all")
    creation_date_before = DateFilter(
        field_name="creation_date__date", lookup_expr="lte"
    )
    submit_date_after_sz = InstanceSubmitDateFilter(lookup_expr="gte")
    submit_date_before_sz = InstanceSubmitDateFilter(lookup_expr="lte")
    instance_state = NumberMultiValueFilter()
    responsible_user = ResponsibleUserFilter(field_name="responsibilities__user")
    responsible_service = ResponsibleServiceFilter()
    responsible_service_user = ResponsibleServiceUserFilter()
    circulation_state = CirculationStateFilter()
    is_applicant = BooleanFilter(
        field_name="involved_applicants__invitee", method="filter_is_applicant"
    )
    form_name = FormNameFilter(field_name="form__name")
    form_name_versioned = NumberFilter(field_name="form__family__pk")
    location = NumberMultiValueFilter()
    address_sz = CharFilter(method="filter_address_sz")
    construction_zone_location_sz = CharFilter(
        method="filter_construction_zone_location_sz"
    )
    keyword_search = InstanceKeywordSearchFilter()
    intent_sz = CharFilter(method="filter_intent_sz")
    plot_sz = FormFieldListValueFilter(
        form_field_names=["parzellen"], keys=["number", "egrid"]
    )
    builder_sz = FormFieldListValueFilter(
        form_field_names=[
            "bauherrschaft",
            "bauherrschaft-v2",
            "bauherrschaft-v3",
            "bauherrschaft-override",
        ],
        keys=["vorname", "name", "firma"],
    )
    landowner_sz = FormFieldListValueFilter(
        form_field_names=[
            "grundeigentumerschaft",
            "grundeigentumerschaft-v2",
            "grundeigentumerschaft-override",
        ],
        keys=["vorname", "name", "firma"],
    )
    applicant_sz = FormFieldListValueFilter(
        form_field_names=[
            "projektverfasser-planer",
            "projektverfasser-planer-v2",
            "projektverfasser-planer-v3",
            "projektverfasser-planer-override",
        ],
        keys=["vorname", "name", "firma"],
    )
    objection_received = BooleanFilter(method="filter_objection_received")
    has_pending_billing_entry = BooleanFilter(method="filter_has_pending_billing_entry")
    has_pending_sanction = BooleanFilter(method="filter_has_pending_sanction")
    pending_sanctions_control_instance = NumberFilter(
        method="filter_pending_sanctions_control_instance"
    )
    with_cantonal_participation = BooleanFilter(
        method="filter_with_cantonal_participation"
    )

    decision_date_after = DecisionDateFilter(lookup_expr="gte")
    decision_date_before = DecisionDateFilter(lookup_expr="lte")
    decision = DecisionFilter()

    oereb_legal_state = OerebLegalStateFilter()

    inquiry_state = InquiryStateFilter()
    inquiry_created_after = InquiryDateFilter(
        lookup_expr="child_case__created_at__date__gte"
    )
    inquiry_created_before = InquiryDateFilter(
        lookup_expr="child_case__created_at__date__lte"
    )
    inquiry_completed_after = InquiryDateFilter(lookup_expr="closed_at__date__gte")
    inquiry_completed_before = InquiryDateFilter(lookup_expr="closed_at__date__lte")
    inquiry_answer = InquiryAnswerFilter()

    def filter_is_applicant(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})

        return queryset.exclude(**{name: self.request.user})

    def filter_objection_received(self, queryset, name, value):
        if value:
            return queryset.filter(objections__isnull=False)
        return queryset

    def filter_has_pending_billing_entry(self, queryset, name, value):
        _filter = {"billing_entries__invoiced": False, "billing_entries__type": 1}

        if value:
            return queryset.filter(**_filter)

        return queryset.exclude(**_filter)

    def filter_has_pending_sanction(self, queryset, name, value):
        _filter = {"sanctions__is_finished": False}

        if value:
            return queryset.filter(**_filter)

        return queryset.exclude(**_filter)

    def filter_pending_sanctions_control_instance(self, queryset, name, value):
        _filter = {
            "sanctions__is_finished": False,
            "sanctions__control_instance_id": value,
        }

        return queryset.filter(**_filter)

    def filter_with_cantonal_participation(self, queryset, name, value):
        return queryset.filter(
            Exists(
                WorkItem.objects.filter(
                    Q(case__family=OuterRef("case"))
                    & Q(task__pk=settings.DISTRIBUTION["INQUIRY_TASK"])
                    & Q(
                        status__in=[
                            WorkItem.STATUS_READY,
                            WorkItem.STATUS_COMPLETED,
                        ]
                    )
                    & Q(addressed_groups__overlap=uri_constants.KOOR_SERVICE_IDS)
                )
            )
        )

    def filter_circulation_service(self, queryset, name, value):
        if settings.DISTRIBUTION:
            pks = [str(pk) for pk in value] if isinstance(value, list) else [str(value)]
            return queryset.filter(
                Exists(
                    WorkItem.objects.filter(
                        Q(case__family=OuterRef("case"))
                        & Q(task__pk=settings.DISTRIBUTION["INQUIRY_TASK"])
                        & Q(
                            status__in=[
                                WorkItem.STATUS_READY,
                                WorkItem.STATUS_COMPLETED,
                            ]
                        )
                        & Q(addressed_groups__overlap=pks)
                    )
                )
            )

        return queryset.filter(circulations__activations__service__pk=value)

    def filter_address_sz(self, queryset, name, value):
        address_form_fields = settings.APPLICATION.get("ADDRESS_FORM_FIELDS", [])
        return queryset.filter(
            fields__name__in=address_form_fields, fields__value__icontains=value
        )

    def filter_intent_sz(self, queryset, name, value):
        intent_form_fields = settings.APPLICATION.get("INTENT_FORM_FIELDS", [])
        return queryset.filter(
            fields__name__in=intent_form_fields, fields__value__icontains=value
        )

    def filter_construction_zone_location_sz(self, queryset, name, value):
        construction_zone_location_form_field = settings.APPLICATION.get(
            "CONSTRUCTION_ZONE_LOCATION_FORM_FIELD", None
        )
        return queryset.filter(
            fields__name=construction_zone_location_form_field,
            fields__value=value,
        )

    class Meta:
        model = models.Instance
        fields = (
            "creation_date",
            "submit_date_after_sz",
            "submit_date_before_sz",
            "form",
            "form_name_versioned",
            "identifier",
            "identifier_for_linking",
            "instance_state",
            "instance_group",
            "location",
            "previous_instance_state",
            "service",
            "user",
            "responsible_user",
            "responsible_service",
            "responsible_service_user",
            "address_sz",
            "intent_sz",
            "plot_sz",
            "builder_sz",
            "landowner_sz",
            "applicant_sz",
            "is_applicant",
            "form_name",
            "has_pending_billing_entry",
            "has_pending_sanction",
            "pending_sanctions_control_instance",
            "with_cantonal_participation",
            "keyword_search",
        )


class CalumaInstanceFilterSet(InstanceFilterSet):
    is_paper = CalumaYesNoFilter(question="is-paper")
    is_modification = CalumaYesNoFilter(
        question="projektaenderung", yes="ja", no="nein"
    )

    sanction_creator = NumberFilter(field_name="sanctions__service")
    sanction_control_instance = NumberFilter(field_name="sanctions__control_instance")
    caluma_keyword_search = CalumaInstanceKeywordSearchFilter()

    class Meta(InstanceFilterSet.Meta):
        fields = InstanceFilterSet.Meta.fields + (
            "is_paper",
            "is_modification",
            "caluma_keyword_search",
        )


class InstanceResponsibilityFilterSet(FilterSet):
    class Meta:
        model = models.InstanceResponsibility
        fields = ("user", "service", "instance")


class InstanceIssueFilterSet(FilterSet):
    state = CharMultiValueFilter()

    class Meta:
        model = models.Issue
        fields = ("instance", "user", "state")


class JournalEntryFilterSet(FilterSet):
    class Meta:
        model = models.JournalEntry
        fields = ("instance", "user")


class HistoryEntryFilterSet(FilterSet):
    class Meta:
        model = models.HistoryEntry
        fields = ("instance", "user", "service", "history_type")


class InstanceFormFieldFilterBackend(BaseFilterBackend):
    """
    Filter backend to filter any instance form field by its values.

    Query param format: `fields[name]=value`
    Example: `fields[baugesuchnummer]=2`

    This class is needed as `DjangoFilterBackend` doesn't allow
    dynamic filter names.
    """

    # TODO: fields query name colides with sparse fields
    # of json api specification and needs to be renamed

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        for param in query_params.keys():
            fields_match = re.match(r"^fields\[(.*?)\]$", param)
            valuelist = query_params.getlist(param)
            if fields_match and valuelist:
                name = fields_match.group(1)
                queryset = queryset.filter(
                    fields__name=name, fields__value__in=valuelist
                )

        return queryset


class FormFilterSet(FilterSet):
    forms_all_versions = BooleanFilter(method="filter_forms_all_versions")

    def filter_forms_all_versions(self, queryset, name, value):
        return queryset.filter(family__pk=F("pk")) if not value else queryset

    class Meta:
        model = models.Form
        fields = ("name", "form_state")


class FormFieldFilterSet(FilterSet):
    instance = NumberMultiValueFilter()
    name = CharMultiValueFilter()
    egrid = JSONFieldMultiValueFilter(
        value_transform=lambda value: [[{"egrid": val}] for val in value],
        lookup_expr="contains",
        field_name="value",
    )
    instance_state = CharMultiValueFilter(field_name="instance__instance_state__name")
    instance_state_exclude = CharMultiValueFilter(
        field_name="instance__instance_state__name", exclude=True
    )

    class Meta:
        model = models.FormField
        fields = ("instance", "name", "egrid", "instance_state")


class IssueTemplateFilterSet(FilterSet):
    class Meta:
        model = models.IssueTemplate
        fields = ["user"]


class IssueTemplateSetFilterSet(FilterSet):
    class Meta:
        model = models.IssueTemplateSet
        fields = ["name"]


class FormFieldOrdering(OrderingFilter):
    ordering_param = "sort_form_field"
    ordering_fields = None

    def _get_instance_pk_filter_expr(self, view):
        instance_field_name = getattr(view, "instance_field")
        return (
            "pk"
            if not instance_field_name
            else f"{instance_field_name.replace('.', LOOKUP_SEP)}__pk"
        )

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a ?sort_form_field=... query parameter.

        Only one form_field can be ordered at a time,
        by appending a - infront the ordering will be inverted.
        """
        param = request.query_params.get(self.ordering_param)
        if param:
            return param.strip()

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        param = self.get_ordering(request, queryset, view)

        if param:
            ordering = "-field_val" if param.startswith("-") else "field_val"

            outer_ref = OuterRef(self._get_instance_pk_filter_expr(view))
            form_field = models.FormField.objects.filter(
                instance=outer_ref, name=param.lstrip("-")
            )
            queryset = queryset.annotate(
                field_val=Subquery(form_field.values("value")[:1])
            ).order_by(ordering)

        return queryset


class PublicCalumaInstanceFilterSet(FilterSet):
    instance = NumberFilter(field_name="instance__pk")
    municipality = NumberFilter(method="filter_municipality")
    form_type = CharFilter(method="filter_form_type")
    dossier_nr = CharFilter()
    exclude_instance = NumberFilter(field_name="instance__pk", exclude=True)

    def filter_municipality(self, queryset, name, value):
        municipality_question = settings.MASTER_DATA["CONFIG"]["municipality"][1]

        return queryset.filter(
            document__answers__question_id=municipality_question,
            document__answers__value=str(value),
        ).distinct()

    def filter_form_type(self, queryset, name, value):
        """Filter the form type. UR specific."""
        return queryset.filter(
            document__answers__question_id="form-type",
            document__answers__value=value,
        )

    class Meta:
        model = Case
        fields = ["instance"]
