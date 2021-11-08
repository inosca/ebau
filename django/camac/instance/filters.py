import re

from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db.models import OuterRef, Subquery
from django.db.models.constants import LOOKUP_SEP
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from rest_framework.filters import BaseFilterBackend, OrderingFilter

from camac.filters import (
    CharMultiValueFilter,
    JSONFieldMultiValueFilter,
    NumberMultiValueFilter,
)

from ..core import models as core_models
from ..responsible import models as responsible_models
from . import models


class ResponsibleUserFilter(CharFilter):
    def filter(self, qs, value):
        if value.lower() == "nobody":
            return qs.filter(**{f"{self.field_name}__isnull": True})
        return super().filter(qs, value)


class ResponsibleInstanceUserFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        if value.lower() == "nobody":
            return qs.filter(
                responsible_services__service__isnull=True,
                responsible_services__responsible_user__isnull=True,
            )

        return qs.filter(
            responsible_services__service=self.parent.request.group.service,
            responsible_services__responsible_user=value,
        )


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
            qs = qs.exclude(
                # exclude all instances which have responsible services
                pk__in=responsible_models.ResponsibleService.objects.filter(
                    service=current_service
                ).values("instance")
            )
            return qs

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


class InstanceFilterSet(FilterSet):
    instance_id = NumberMultiValueFilter()
    service = NumberFilter(field_name="circulations__activations__service")
    creation_date_after = DateFilter(
        field_name="creation_date__date", lookup_expr="gte"
    )
    tags = CharMultiValueFilter(field_name="tags__name", lookup_expr="all")
    creation_date_before = DateFilter(
        field_name="creation_date__date", lookup_expr="lte"
    )
    instance_state = NumberMultiValueFilter()
    responsible_user = ResponsibleUserFilter(field_name="responsibilities__user")
    responsible_instance_user = ResponsibleInstanceUserFilter()
    responsible_service = ResponsibleServiceFilter()
    responsible_service_user = ResponsibleServiceUserFilter()
    circulation_state = CirculationStateFilter()
    is_applicant = BooleanFilter(
        field_name="involved_applicants__invitee", method="filter_is_applicant"
    )
    form_name = CharFilter(field_name="form__name")
    location = NumberMultiValueFilter()
    has_pending_billing_entry = BooleanFilter(method="filter_has_pending_billing_entry")
    has_pending_sanction = BooleanFilter(method="filter_has_pending_sanction")
    pending_sanctions_control_instance = NumberFilter(
        method="filter_pending_sanctions_control_instance"
    )

    def filter_is_applicant(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})

        return queryset.exclude(**{name: self.request.user})

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

    class Meta:
        model = models.Instance
        fields = (
            "creation_date",
            "form",
            "identifier",
            "instance_state",
            "instance_group",
            "location",
            "previous_instance_state",
            "service",
            "user",
            "responsible_user",
            "responsible_instance_user",
            "responsible_service",
            "responsible_service_user",
            "is_applicant",
            "form_name",
            "has_pending_billing_entry",
            "has_pending_sanction",
            "pending_sanctions_control_instance",
        )


class CalumaInstanceFilterSet(InstanceFilterSet):
    is_paper = BooleanFilter(method="filter_is_paper")

    sanction_creator = NumberFilter(field_name="sanctions__service")
    sanction_control_instance = NumberFilter(field_name="sanctions__control_instance")

    def filter_is_paper(self, queryset, name, value):
        _filter = {
            "case__document__answers__question_id": "is-paper",
            "case__document__answers__value": "is-paper-yes",
        }

        if value:
            return queryset.filter(**_filter)

        return queryset.exclude(**_filter)

    class Meta(InstanceFilterSet.Meta):
        fields = InstanceFilterSet.Meta.fields + ("is_paper",)


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
    class Meta:
        model = models.Form
        fields = ["name"]


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

    def filter_municipality(self, queryset, name, value):
        municipality_question = settings.APPLICATION["MASTER_DATA"]["municipality"][1]

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
