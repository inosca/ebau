import datetime as dt
from functools import lru_cache

from caluma.caluma_form.models import Answer, DynamicOption
from caluma.caluma_workflow.models import Case as CalumaCase, WorkItem
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db.models import (
    Case,
    CharField,
    DateField,
    Exists,
    F,
    Func,
    IntegerField,
    Min,
    OuterRef,
    Q,
    Subquery,
    UUIDField,
    Value,
    When,
)
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import (
    Cast,
    Coalesce,
    Concat,
    NullIf,
    Replace,
    Trim,
)
from django.utils.translation import get_language
from django_filters.rest_framework import BaseInFilter, DateFilter as DFDateFilter
from rest_framework.filters import BaseFilterBackend

from camac.caluma.models import Inquiry
from camac.deadlines.models import InstanceDeadline
from camac.instance.export.filters import StringAggSubquery
from camac.instance.models import Instance, InstanceStateT
from camac.responsible.models import ResponsibleService
from camac.user.models import Service, ServiceT, User
from camac.work_items.models import WorkItemTemplate


@lru_cache
def get_inquiry_service_id():
    """Return service ID of the AfB service (kt_ag)."""
    return Service.objects.filter(slug="afb").values_list("pk", flat=True).first()


def split_query_param(request, param):
    """Split a comma-separated query parameter into a list of stripped values."""
    raw = request.query_params.get(param, "")
    return [v.strip() for v in raw.split(",") if v.strip()]


class SubmitDateFilter(DFDateFilter):
    """Filter instances by submit date stored in case.meta['submit-date']."""

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        qs = qs.annotate(
            _submit_date_cast=Cast(
                NullIf(
                    KeyTextTransform(
                        "submit-date", "case__meta", output_field=CharField()
                    ),
                    Value(""),
                ),
                output_field=DateField(),
            )
        )
        return qs.filter(**{f"_submit_date_cast__{self.lookup_expr}": value})


class FormFilter(BaseInFilter):
    """Filter instances by one or more form slugs (comma-separated)."""

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        return qs.filter(case__family__document__form_id__in=value)


class InstanceStateFilter(BaseInFilter):
    """Filter instances by one or more instance-state IDs (comma-separated)."""

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES:
            return qs

        return qs.filter(instance_state_id__in=value)


class DecisionFilter(BaseInFilter):
    """Filter instances by one or more decision answer values (comma-separated)."""

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


class FirstInquiryDateFilter(DFDateFilter):
    """Filter instances by the date of the first inquiry addressed to a service.

    Uses child_case.created_at of the earliest active inquiry addressed to the
    given service for each instance.
    """

    def __init__(self, *args, service_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_id = service_id

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES or self.service_id is None:
            return qs

        # Find instances where the earliest inquiry (by child_case creation)
        # addressed to the requesting service satisfies the date condition.
        matching_instance_pks = (
            Inquiry.objects.addressed_to(self.service_id)
            .only_active()
            .values("case__family__instance__pk")
            .annotate(
                first_inquiry_date=Min("child_case__created_at__date"),
            )
            .filter(**{f"first_inquiry_date__{self.lookup_expr}": value})
            .values_list("case__family__instance__pk", flat=True)
        )

        return qs.filter(pk__in=list(matching_instance_pks))


def _exclude_claim_inquiries(qs):
    """Exclude inquiries answered with status "claim" (Unterlagenergänzung)."""
    status_question = settings.DISTRIBUTION.get("QUESTIONS", {}).get("STATUS")
    claim_value = (
        settings.DISTRIBUTION.get("ANSWERS", {}).get("STATUS", {}).get("CLAIM")
    )
    if not status_question or not claim_value:
        return qs

    return qs.exclude(
        child_case__document__answers__question_id=status_question,
        child_case__document__answers__value=claim_value,
    )


class CompletingDateFilter(DFDateFilter):
    """Filter instances by the date of the last completed inquiry for a service.

    Uses closed_at of the latest completed/skipped inquiry addressed to the
    given service for each instance. Inquiries answered with status "claim"
    (Unterlagenergänzung) are excluded.
    """

    def __init__(self, *args, service_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_id = service_id

    def filter(self, qs, value, *args, **kwargs):
        if value in EMPTY_VALUES or self.service_id is None:
            return qs

        # Find instances where the earliest completed inquiry (by closed_at)
        # addressed to the requesting service satisfies the date condition.
        matching_instance_pks = (
            _exclude_claim_inquiries(
                Inquiry.objects.addressed_to(self.service_id).for_status(
                    WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED
                )
            )
            .filter(closed_at__isnull=False)
            .values("case__family__instance__pk")
            .annotate(
                completing_date=Min("closed_at__date"),
            )
            .filter(**{f"completing_date__{self.lookup_expr}": value})
            .values_list("case__family__instance__pk", flat=True)
        )

        return qs.filter(pk__in=list(matching_instance_pks))


class InvolvedFilter:
    """Filter instances where the service is involved (inquiry or responsible).

    Supports three states:
    - value="true": Filter for instances where service IS involved
    - value="false": Filter for instances where service IS NOT involved
    - value=None/empty: No filtering (return all instances)
    """

    def __init__(self, service_id=None):
        self.service_id = service_id

    def filter(self, qs, value):
        if not value or self.service_id is None:
            return qs

        has_inquiry = Exists(
            Inquiry.objects.addressed_to(self.service_id).filter(
                case__family__instance=OuterRef("pk")
            )
        )

        if value.lower() == "true":
            return qs.filter(has_inquiry)
        elif value.lower() == "false":
            return qs.exclude(has_inquiry)

        return qs


class _BaseFilterBackend(BaseFilterBackend):
    """Shared annotation and filtering logic for statistics export backends.

    Subclasses set the _*_ref class attributes to adapt annotation paths
    to their target queryset (Instance/WorkItem).
    """

    # Path configuration — overridden by concrete subclasses.
    _case_ref: str  # "case" | "case__family" - reference to top level case (family)
    _instance_ref: str  # "" | "case__family__instance"

    @property
    def _case_meta_path(self):
        return f"{self._case_ref}__meta"

    @property
    def _document_id_ref(self):
        return f"{self._case_ref}__document_id"

    @property
    def _instance_pk_ref(self):
        return f"{self._instance_ref}__pk" if self._instance_ref else "pk"

    @property
    def _instance_state_id_ref(self):
        return (
            f"{self._instance_ref}__instance_state_id"
            if self._instance_ref
            else "instance_state_id"
        )

    def annotate_dossier_number(self):
        return NullIf(
            Replace(
                KeyTextTransform(
                    "dossier-number",
                    self._case_meta_path,
                    output_field=CharField(),
                ),
                Value('"'),
                Value(""),
            ),
            Value("null"),
        )

    def annotate_type(self):
        return Subquery(
            CalumaCase.objects.filter(pk=OuterRef(f"{self._case_ref}_id")).values(
                f"document__form__name__{get_language()}"
            )[:1]
        )

    def annotate_plot_number(self):
        return StringAggSubquery(
            Answer.objects.filter(
                question_id="parzellennummer",
                document__family=OuterRef(self._document_id_ref),
                value__isnull=False,
            )
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
                ),
            )
            .values("string_value"),
            column_name="string_value",
            delimiter=", ",
        )

    def annotate_submit_date(self):
        return Cast(
            NullIf(
                KeyTextTransform(
                    "submit-date", self._case_meta_path, output_field=CharField()
                ),
                Value(""),
            ),
            output_field=DateField(),
        )

    def annotate_responsible_user(self, service_id):
        return Subquery(
            ResponsibleService.objects.filter(
                instance_id=OuterRef(self._instance_pk_ref),
                service_id=service_id,
            )
            .annotate(
                name=Trim(
                    Concat(
                        Trim(F("responsible_user__name")),
                        Value(" "),
                        Trim(F("responsible_user__surname")),
                    )
                ),
            )
            .values("name")[:1]
        )

    def annotate_municipality(self):
        return Subquery(
            DynamicOption.objects.filter(
                question_id="gemeinde",
                document_id=OuterRef(self._document_id_ref),
            )
            .order_by("-created_at")
            .values(f"label__{get_language()}")[:1]
        )

    def annotate_instance_status(self):
        return Subquery(
            InstanceStateT.objects.filter(
                instance_state_id=OuterRef(self._instance_state_id_ref),
                language=get_language(),
            ).values("name")[:1]
        )

    def annotate_first_inquiry_date(self, service_id):
        """Date when the first inquiry was sent to the requesting service."""
        return Subquery(
            Inquiry.objects.addressed_to(service_id)
            .only_active()
            .filter(case__family__instance=OuterRef(self._instance_pk_ref))
            .annotate(inquiry_date=Cast("child_case__created_at__date", DateField()))
            .order_by("inquiry_date")
            .values("inquiry_date")[:1],
            output_field=DateField(),
        )

    def annotate_completing_date(self, service_id):
        """Date when the first inquiry from the service was completed.

        Inquiries answered with status claim are ignored.
        """
        return Subquery(
            _exclude_claim_inquiries(
                Inquiry.objects.addressed_to(service_id).for_status(
                    WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED
                )
            )
            .filter(
                case__family__instance=OuterRef(self._instance_pk_ref),
                closed_at__isnull=False,
            )
            .annotate(completion_date=Cast("closed_at__date", DateField()))
            .order_by("completion_date")
            .values("completion_date")[:1],
            output_field=DateField(),
        )

    def annotate_processing_time(self, service_id):
        """Return the number of working days from deadline start to completion."""
        return Subquery(
            InstanceDeadline.objects.filter(
                instance=OuterRef(self._instance_pk_ref),
                service_id=service_id,
            ).values("process_deadline_days")[:1],
            output_field=IntegerField(),
        )

    def annotate_on_time(self, service_id):
        """Whether the deadline was met (1) or not (0).

        Compares process_deadline_date against target_deadline_date
        on the InstanceDeadline for the requesting service.  Returns
        None when either date is not yet set.
        """
        return Subquery(
            InstanceDeadline.objects.filter(
                instance=OuterRef(self._instance_pk_ref),
                service_id=service_id,
            )
            .annotate(
                is_on_time=Case(
                    When(
                        process_deadline_date__isnull=True,
                        then=Value(None),
                    ),
                    When(
                        target_deadline_date__isnull=True,
                        then=Value(None),
                    ),
                    When(
                        process_deadline_date__lte=F("target_deadline_date"),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
            .values("is_on_time")[:1],
            output_field=IntegerField(),
        )

    def _filter_instances(self, request, queryset):
        """Apply Instance-level filters and return allowed PKs.

        Applies every registered filter class sequentially, then puts
        the PKs into a list so the next step receives a
        ``WHERE pk IN (...)`` instead of a deeply-nested subquery.
        """
        current_service = request.group.service_id
        inquiry_service = get_inquiry_service_id()

        queryset = SubmitDateFilter(lookup_expr="gte").filter(
            queryset, request.query_params.get("submit_date_after")
        )
        queryset = SubmitDateFilter(lookup_expr="lte").filter(
            queryset, request.query_params.get("submit_date_before")
        )
        queryset = FormFilter().filter(queryset, split_query_param(request, "form"))
        queryset = InstanceStateFilter().filter(
            queryset, split_query_param(request, "instance_state")
        )
        queryset = DecisionFilter().filter(
            queryset, split_query_param(request, "decision")
        )
        queryset = FirstInquiryDateFilter(
            lookup_expr="gte", service_id=inquiry_service
        ).filter(queryset, request.query_params.get("first_inquiry_date_after"))
        queryset = FirstInquiryDateFilter(
            lookup_expr="lte", service_id=inquiry_service
        ).filter(queryset, request.query_params.get("first_inquiry_date_before"))
        queryset = CompletingDateFilter(
            lookup_expr="gte", service_id=inquiry_service
        ).filter(queryset, request.query_params.get("completing_date_after"))
        queryset = CompletingDateFilter(
            lookup_expr="lte", service_id=inquiry_service
        ).filter(queryset, request.query_params.get("completing_date_before"))
        queryset = InvolvedFilter(service_id=current_service).filter(
            queryset, request.query_params.get("involved")
        )

        # Exclude dossiers that still have any pending inquiry addressed to
        # the inquiry service, but only when filtering by completing date.
        completing_date_filter_active = any(
            request.query_params.get(param)
            for param in ("completing_date_after", "completing_date_before")
        )
        if completing_date_filter_active:
            pending_inquiries = (
                Inquiry.objects.addressed_to(inquiry_service)
                .only_pending()
                .filter(case__family__instance=OuterRef("pk"))
            )
            queryset = queryset.exclude(Exists(pending_inquiries))

        return list(queryset.order_by().values_list("pk", flat=True).distinct())

    def _dossier_annotations(
        self,
        service_id,
        inquiry_service_id,
        requested_columns=None,
    ):
        """Return the dict of dossier-level annotation kwargs."""

        available_annotations = {
            "dossier_number": lambda: self.annotate_dossier_number(),
            "form_name": lambda: self.annotate_type(),
            "parcels": lambda: self.annotate_plot_number(),
            "submit_date": lambda: self.annotate_submit_date(),
            "responsible_user": lambda: self.annotate_responsible_user(service_id),
            "municipality": lambda: self.annotate_municipality(),
            "instance_status": lambda: self.annotate_instance_status(),
            "first_inquiry_date": lambda: self.annotate_first_inquiry_date(
                inquiry_service_id
            ),
            "completing_date": lambda: self.annotate_completing_date(
                inquiry_service_id
            ),
            "processing_time": lambda: self.annotate_processing_time(service_id),
            "on_time": lambda: self.annotate_on_time(service_id),
        }

        columns = (
            requested_columns
            if requested_columns is not None
            else available_annotations.keys()
        )
        return {
            name: available_annotations[name]()
            for name in columns
            if name in available_annotations
        }


class InstanceFilterBackend(_BaseFilterBackend):
    """Export one row per Instance (dossier)."""

    _case_ref = "case"
    _instance_ref = ""

    def filter_queryset(self, request, queryset, requested_annotations):
        current_service = request.group.service_id
        inquiry_service = get_inquiry_service_id()
        requested_columns = requested_annotations

        allowed_pks = self._filter_instances(request, queryset)

        return (
            Instance.objects.filter(pk__in=allowed_pks)
            .select_related("case")
            .only(
                "pk",
                "instance_state_id",
                "case__meta",
                "case__family_id",
                "case__document_id",
            )
            .annotate(
                **self._dossier_annotations(
                    current_service,
                    inquiry_service,
                    requested_columns,
                )
            )
        )


class WorkItemFilterBackend(_BaseFilterBackend):
    """Export one row per completed inquiry WorkItem.

    Only completed and inquiry tasks work items are included.
    """

    _case_ref = "case__family"
    _instance_ref = "case__family__instance"

    def annotate_wi_assigned_user(self):
        """Resolve the first assigned username to a full name."""
        return Subquery(
            User.objects.filter(
                username=OuterRef("assigned_users__0"),
            )
            .annotate(
                full_name=Trim(
                    Concat(
                        Trim(F("name")),
                        Value(" "),
                        Trim(F("surname")),
                    )
                ),
            )
            .values("full_name")[:1]
        )

    def annotate_wi_addressed_group(self):
        """Resolve the first addressed group to a service name."""
        return Subquery(
            ServiceT.objects.filter(
                service_id=Cast(OuterRef("addressed_groups__0"), IntegerField()),
                language=get_language(),
            ).values("name")[:1]
        )

    def annotate_wi_processing_time(self):
        """Return the number of calendar days between created_at and closed_at."""

        class _DateDiffDays(Func):
            """PostgreSQL ``date - date`` returning an integer number of days."""

            template = "(%(expressions)s)"
            arg_joiner = " - "
            output_field = IntegerField()

        return _DateDiffDays(
            Cast("closed_at", output_field=DateField()),
            Cast("created_at", output_field=DateField()),
        ) + Value(1)

    def annotate_wi_on_time(self):
        """Whether the work item was closed before or on its deadline (1) or not (0).

        Returns None when closed_at is not set.
        Returns 1 when there is no deadline (no deadline = always on time).
        """
        return Case(
            When(closed_at__isnull=True, then=Value(None)),
            When(deadline__isnull=True, then=Value(1)),
            When(
                closed_at__date__lte=F("deadline__date"),
                then=Value(1),
            ),
            default=Value(0),
            output_field=IntegerField(),
        )

    def annotate_task_name(self):
        """Resolve the task name, preferring the manual template name."""
        return Coalesce(
            Subquery(
                WorkItemTemplate.objects.filter(
                    pk=Cast(
                        KeyTextTransform("template-id", OuterRef("meta")),
                        output_field=UUIDField(),
                    ),
                ).values("name")[:1]
            ),
            F(f"task__name__{get_language()}"),
            output_field=CharField(),
        )

    def _work_item_annotations(self, requested_columns=None):
        """Return the dict of work-item-level annotation kwargs."""
        available = {
            "task_name": lambda: self.annotate_task_name(),
            "wi_created_at": lambda: Cast("created_at__date", DateField()),
            "wi_deadline": lambda: Cast("deadline__date", DateField()),
            "wi_closed_at": lambda: Cast("closed_at__date", DateField()),
            "wi_assigned_user": lambda: self.annotate_wi_assigned_user(),
            "wi_addressed_group": lambda: self.annotate_wi_addressed_group(),
            "wi_status": lambda: F("status"),
            "wi_processing_time": lambda: self.annotate_wi_processing_time(),
            "wi_on_time": lambda: self.annotate_wi_on_time(),
        }

        columns = (
            requested_columns if requested_columns is not None else available.keys()
        )
        return {name: available[name]() for name in columns if name in available}

    def filter_queryset(self, request, queryset, requested_annotations):
        current_service = request.group.service_id
        requested_columns = requested_annotations

        task_slugs = split_query_param(request, "task")

        if task_slugs:
            # Filter by the requested tasks, matching either by task_id or by
            # meta.template-id (same logic as work-item-list v2).
            task_filter = Q(task_id__in=task_slugs) | Q(
                **{"meta__template-id__in": task_slugs}
            )
        else:
            # Default: only inquiry work items (original behaviour).
            inquiry_task = settings.DISTRIBUTION["INQUIRY_TASK"]
            task_filter = Q(task_id=inquiry_task)

        role = request.query_params.get("role", "active")
        service_id = str(current_service)

        if role == "control":
            role_filter = (
                Q(controlling_groups__contains=[service_id])
                & ~Q(addressed_groups__contains=[service_id])
                & ~Q(addressed_groups__contains=["applicant"])
            )
        else:
            role_filter = Q(addressed_groups__contains=[service_id])

        date_filters = Q()
        for param, lookup in [
            ("wi_created_at_after", "created_at__date__gte"),
            ("wi_created_at_before", "created_at__date__lte"),
            ("wi_closed_at_after", "closed_at__date__gte"),
            ("wi_closed_at_before", "closed_at__date__lte"),
        ]:
            raw = request.query_params.get(param)
            if raw:
                date_filters &= Q(**{lookup: dt.date.fromisoformat(raw)})

        return (
            WorkItem.objects.filter(
                task_filter,
                role_filter,
                date_filters,
                status=WorkItem.STATUS_COMPLETED,
            )
            .select_related("task", "case")
            .annotate(
                **self._dossier_annotations(
                    current_service, current_service, requested_columns
                ),
                **self._work_item_annotations(requested_columns),
            )
        )
