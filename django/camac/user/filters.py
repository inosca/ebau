from functools import reduce

from caluma.caluma_form.models import Answer
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q, Subquery
from django.utils import timezone
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)

from camac.billing.views import BillingV2EntryViewset
from camac.constants import kt_uri as uri_constants
from camac.filters import CharMultiValueFilter, NumberMultiValueFilter
from camac.instance import utils as instance_utils
from camac.instance.models import Instance
from camac.instance.views import InstanceView
from camac.responsible.models import ResponsibleService

from . import models
from .permissions import get_permission_func, permission_aware
from .utils import get_service_suggestions


class LocationFilterSet(FilterSet):
    location_id = NumberMultiValueFilter()

    class Meta:
        model = models.Location
        fields = ("location_id", "name", "communal_federal_number")


class PublicServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()
    has_parent = BooleanFilter(
        field_name="service_parent", lookup_expr="isnull", exclude=True
    )
    available_in_distribution = BooleanFilter(method="_available_in_distribution")
    service_group_name = CharMultiValueFilter(field_name="service_group__name")
    suggestion_for_instance = NumberFilter(method="filter_suggestion_for_instance")
    exclude_own_service = BooleanFilter(method="filter_exclude_own_service")
    service_name = CharFilter(method="filter_service_name")
    available_in_distribution_for_instance = NumberFilter(
        method="filter_available_in_distribution_for_instance"
    )

    # ?provider_for=geometer;999111 (service id)
    provider_for = CharFilter(method="filter_provider_for")

    # ?provider_for_instance_municipality=geometer;1234 (instance id)
    provider_for_instance_municipality = CharFilter(
        method="filter_provider_for_instance_municipality"
    )

    has_billing_entries = BooleanFilter(method="_filter_has_billing_entries")

    def _get_public_services_base(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        group = self.request.group
        service_group_mapping = settings.APPLICATION.get(
            "SERVICE_GROUPS_FOR_DISTRIBUTION", {}
        )

        groups = service_group_mapping.get("groups", {})
        roles = service_group_mapping.get("roles", {})
        service_groups = groups.get(group.pk, []) or roles.get(group.role.name, [])
        filters = []
        for config in service_groups:
            if config["localized"]:
                filters.append(
                    Q(
                        Q(groups__locations__in=group.locations.all())
                        | Q(groups__locations__isnull=True),
                        service_group__pk=config["id"],
                    )
                )
            else:
                filters.append(Q(service_group__pk=config["id"]))

        return (
            queryset.filter(reduce(lambda a, b: a | b, filters)).distinct()
            if len(filters) > 0
            else queryset
        )

    @permission_aware
    def _available_in_distribution(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        return queryset.none()

    def _available_in_distribution_for_service(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        group = self.request.group.pk
        service_group_mapping = settings.APPLICATION.get(
            "SERVICE_GROUPS_FOR_DISTRIBUTION", {}
        )
        if group in service_group_mapping.get("groups", {}):
            return self._get_public_services_base(queryset, name, value)

        # Services can invite subservices
        service = self.request.group.service
        return queryset.filter(service_parent=service)

    def _available_in_distribution_for_municipality(self, queryset, name, value):
        queryset = self._get_public_services_base(queryset, name, value)

        if settings.APPLICATION_NAME == "kt_uri":
            queryset = queryset.filter(
                Q(
                    pk__in=[
                        uri_constants.KOOR_BG_SERVICE_ID,
                        uri_constants.KOOR_NP_SERVICE_ID,
                    ]
                )
                | ~Q(service_group__name="Koordinationsstellen")
            )

        return queryset

    def _available_in_distribution_for_coordination(self, queryset, name, value):
        return self._get_public_services_base(queryset, name, value)

    def filter_available_in_distribution_for_instance(self, queryset, name, value):
        config = settings.DISTRIBUTION.get("AVAILABLE_SERVICES_FOR_INQUIRY")

        if not config:  # pragma: no cover
            return queryset

        service = self.request.group.service
        service_group = service.service_group.name
        instance = Instance.objects.get(pk=value)

        if instance.responsible_service() == service:
            service_group = "authority"

        applied_config = config.get(service_group, config.get("default", []))

        filters = {
            "include": Q(service_parent=service),
            "exclude": Q(),
        }

        for config_part in applied_config:
            conditions = config_part.get("conditions", [])

            if len(conditions) and not all(
                (
                    getattr(self, f"_condition_{condition['name']}")(instance)
                    != condition.get("invert", False)
                    for condition in conditions
                )
            ):
                continue

            for filter_type in ["include", "exclude"]:
                for type, values in config_part.get(filter_type, []):
                    if type == "services":
                        filters[filter_type] |= Q(
                            service_parent__isnull=True,
                            slug__in=values,
                        )
                    elif type == "service_groups":
                        filters[filter_type] |= Q(
                            service_parent__isnull=True,
                            service_group__name__in=values,
                        )

        return queryset.filter(filters["include"]).exclude(filters["exclude"])

    def _condition_is_bab(self, instance):
        if not settings.BAB:  # pragma: no cover
            return False

        return instance.case.meta.get("is-bab", False)

    def _condition_is_appeal(self, instance):
        if not settings.APPEAL:  # pragma: no cover
            return False

        return instance.case.meta.get("is-appeal", False)

    def _condition_publication_is_done(self, instance):
        publication_work_items = WorkItem.objects.filter(
            **{
                "case": instance.case,
                "task_id__in": settings.PUBLICATION["FILL_TASKS"],
                "meta__is-published": True,
                "status": WorkItem.STATUS_COMPLETED,
            }
        )

        has_completed_publication = publication_work_items.filter(
            Exists(
                Answer.objects.filter(
                    document_id=OuterRef("document_id"),
                    question_id="publikation-ende",
                    date__lte=timezone.now(),
                )
            )
        ).exists()

        has_running_publication = publication_work_items.filter(
            Q(
                Exists(
                    Answer.objects.filter(
                        document_id=OuterRef("document_id"),
                        question_id="publikation-ende",
                        date__gte=timezone.now(),
                    )
                )
            )
            & Q(
                Exists(
                    Answer.objects.filter(
                        document_id=OuterRef("document_id"),
                        question_id="publikation-start",
                        date__lte=timezone.now(),
                    )
                )
            )
        ).exists()

        return not has_running_publication and has_completed_publication

    def filter_suggestion_for_instance(self, queryset, name, value):
        suggested_service_ids_or_slugs = get_service_suggestions(
            Instance.objects.get(pk=value)
        )

        if all(isinstance(item, str) for item in list(suggested_service_ids_or_slugs)):
            return queryset.filter(slug__in=suggested_service_ids_or_slugs)
        return queryset.filter(pk__in=suggested_service_ids_or_slugs)

    def filter_exclude_own_service(self, queryset, name, value):
        if value and self.request.group.service_id:
            return queryset.exclude(pk=self.request.group.service_id)

        return queryset

    def filter_service_name(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            return queryset.filter(trans__name__icontains=value).distinct()

        return queryset.filter(name__icontains=value).distinct()

    def filter_provider_for(self, queryset, name, value):
        function, receiver = value.split(";")

        return queryset.filter(
            pk__in=models.ServiceRelation.objects.filter(
                function=function, receiver=receiver
            ).values("provider")
        )

    def filter_provider_for_instance_municipality(self, queryset, name, value):
        function, receiver_instance = value.split(";")
        providers = instance_utils.get_municipality_provider_services(
            receiver_instance, function
        )

        return queryset.filter(pk__in=Subquery(providers.values("pk")))

    def _filter_has_billing_entries(self, queryset, name, value):
        if not value:
            return queryset

        view = BillingV2EntryViewset(request=self.request)
        qs = view.get_queryset().filter(group__service=OuterRef("pk")).only("pk")

        return queryset.filter(Exists(qs))

    class Meta:
        model = models.Service
        fields = (
            "service_group",
            "has_parent",
            "available_in_distribution",
            "available_in_distribution_for_instance",
            "service_group_name",
            "service_parent",
            "suggestion_for_instance",
            "exclude_own_service",
            "service_name",
            "provider_for",
        )


class ServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()
    service_group_id = NumberMultiValueFilter()

    class Meta:
        model = models.Service
        fields = ("service_id", "service_group_id", "service_parent")


class PublicUserFilterSet(FilterSet):
    id = NumberMultiValueFilter()
    username = CharMultiValueFilter()
    service = NumberMultiValueFilter(field_name="groups__service")
    disabled = BooleanFilter()

    class Meta:
        model = models.User
        fields = ("username", "service")


class UserFilterSet(FilterSet):
    id = NumberMultiValueFilter()
    username = CharMultiValueFilter()
    exclude_primary_role = CharFilter(
        field_name="user_groups", method="_exclude_primary_role"
    )
    responsible_for_instances = BooleanFilter(
        method="_filter_responsible_for_instances"
    )

    def _exclude_primary_role(self, queryset, name, value):
        user_groups = models.UserGroup.objects.filter(
            default_group=1, group__role__name=value
        )
        return queryset.exclude(user_groups__in=user_groups).distinct()

    def _filter_responsible_for_instances(self, queryset, name, value):
        responsible = ResponsibleService.objects.filter(
            service_id=self.request.group.service_id
        ).values("responsible_user")

        if value:
            return queryset.filter(pk__in=responsible)

        return queryset.exclude(pk__in=responsible)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "disabled",
            "exclude_primary_role",
            "responsible_for_instances",
        )


class AccessibleInstanceFilter(NumberFilter):
    """Return list of groups that have access to given instance.

    This is used to display a "list of groups with access" when users click on links
    in notifications and don't have access with the currently selected group.
    """

    def filter(self, qs, value):
        if not value:
            return qs

        groups = self.parent.request.user.groups.all()
        groups_with_access = list(groups)

        view = InstanceView(
            request=self.parent.request,
            queryset=Instance.objects.filter(pk=int(value)),
            action="default",
        )
        return qs.filter(
            pk__in=[g.pk for g in groups_with_access if self._has_permission(view, g)]
        )

    def _has_permission(self, view, group):
        permission_func = get_permission_func(view, "get_queryset", group)
        if permission_func:
            return permission_func(group).count() > 0
        return True


class ServiceOrSubserviceFilter(NumberFilter):
    def filter(self, queryset, value):
        if value in EMPTY_VALUES:
            return queryset

        return queryset.filter(
            Q(service_id=value) | Q(service__service_parent_id=value)
        )


class GroupFilterSet(FilterSet):
    accessible_instance = AccessibleInstanceFilter()
    service = NumberMultiValueFilter()
    service_group = NumberMultiValueFilter(field_name="service__service_group")
    role = NumberMultiValueFilter()
    service_or_subservice = ServiceOrSubserviceFilter()

    class Meta:
        model = models.Group
        fields = (
            "accessible_instance",
            "service",
            "service_group",
            "role",
            "service_or_subservice",
        )


class PublicGroupFilterSet(FilterSet):
    service_group = NumberMultiValueFilter(field_name="service__service_group")
    role = NumberMultiValueFilter()
    service = NumberMultiValueFilter()

    class Meta:
        model = models.Group
        fields = ("service_group", "role", "service", "group_id")


class UserGroupFilterSet(FilterSet):
    in_group = NumberMultiValueFilter(field_name="group")

    class Meta:
        model = models.UserGroup
        fields = ("in_group",)
