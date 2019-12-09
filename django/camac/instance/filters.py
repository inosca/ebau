import re

from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from rest_framework.filters import BaseFilterBackend

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
                responsibilities__service__isnull=True,
                responsibilities__user__isnull=True,
            )

        return qs.filter(
            responsibilities__service=self.parent.request.group.service,
            responsibilities__user=value,
        )


class ResponsibleServiceFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        active_services = core_models.InstanceService.objects.filter(
            active=1,
            **settings.APPLICATION.get("ACTIVE_SERVICE_FILTERS", {}),
            service=value,
        )
        qs = qs.filter(pk__in=active_services.values("instance_id"))
        return qs


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


class CirculationStateFilter(NumberFilter):
    def filter(self, qs, value, *args, **kwargs):
        if value:
            return qs.filter(
                circulations__activations__service=self.parent.request.group.service,
                circulations__activations__circulation_state__pk=int(value),
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

    def filter_is_applicant(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})

        return queryset.exclude(**{name: self.request.user})

    class Meta:
        model = models.Instance
        fields = (
            "creation_date",
            "form",
            "identifier",
            "instance_state",
            "location",
            "previous_instance_state",
            "service",
            "user",
            "responsible_user",
            "responsible_instance_user",
            "responsible_service",
            "responsible_service_user",
            "is_applicant",
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


class FormFieldFilterSet(FilterSet):

    instance = NumberMultiValueFilter()
    name = CharMultiValueFilter()
    egrid = JSONFieldMultiValueFilter(
        value_transform=lambda value: [[{"egrid": val}] for val in value],
        lookup_expr="contains",
        field_name="value",
    )
    instance_state = CharMultiValueFilter(field_name="instance__instance_state__name")

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
