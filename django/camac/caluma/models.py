from itertools import chain
from typing import List, TypeAlias, TypeVar
from uuid import UUID

from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.db.models import Manager, OuterRef, Q, QuerySet

from camac.instance.models import Instance
from camac.user.models import Service

T = TypeVar("T", bound="InquiryQuerySet")
ServiceType: TypeAlias = Service | int | str | None | List["ServiceType"]


def to_groups(service: ServiceType) -> List[str]:
    """Convert a service argument to a list of strings acceptable for caluma group filters.

    The caluma group attributes (`addressed_groups` and `controlling_groups`)
    always contain a list of strings (`ArrayField`). In order to filter those
    attributes, our value must be the same.

    Turns a service, or list of services, into a list of group IDs. Services may
    be passed in as a service object, or an integer or string representing
    service IDs. `None` values will be filtered out.
    """

    if isinstance(service, list):
        service = list(chain(*[to_groups(s) for s in service]))
    elif isinstance(service, Service):
        service = [str(service.pk)]
    elif isinstance(service, int):
        service = [str(service)]
    else:
        service = [service]

    return [s for s in service if s is not None]


def build_array_filter(base: str, values: List[str]) -> Q:
    """Create a django filter for `ArrayField`s.

    This will either use the lookup `contains` (0 or 1 values) or `overlap` (1+
    values) to create a filter argument that can be used to filter array fields.

    In other words: The returned filter will match a record if at least one of
    the given values is in the lookup field.
    """

    lookup = "overlap" if len(values) > 1 else "contains"

    return Q(**{f"{base}__{lookup}": values})


class InquiryQuerySet(QuerySet["Inquiry"]):
    """Custom queryset for inquiries.

    This queryset provides lots of predefined filter methods that can help you
    query the inquiries you need.
    """

    def for_status(self: T, *status: List[str]) -> T:
        """Return inquiries that match the given status."""

        return self.filter(status__in=status)

    def only_pending(self: T) -> T:
        """Return only pending inquries (status READY)."""

        return self.for_status(WorkItem.STATUS_READY)

    def only_answered(self: T) -> T:
        """Return only answered inquries (status COMPLETED)."""

        return self.for_status(WorkItem.STATUS_COMPLETED)

    def only_drafts(self: T) -> T:
        """Return only draft inquries (status DRAFT)."""

        return self.for_status(WorkItem.STATUS_SUSPENDED)

    def only_skipped(self: T) -> T:
        """Return only skipped inquries (status SKIPPED)."""

        return self.for_status(WorkItem.STATUS_SKIPPED)

    def only_active(self: T) -> T:
        """Return only inquries are active (status not SUSPENDED or CANCELED)."""

        return self.exclude(
            status__in=[WorkItem.STATUS_SUSPENDED, WorkItem.STATUS_CANCELED]
        )

    def exclude_withdrawn(self: T) -> T:
        """Return only inquries that were not withdrawn (status not CANCELED)."""

        return self.exclude(status=WorkItem.STATUS_CANCELED)

    def for_root_case(self: T, case: Case | UUID | str | OuterRef | None) -> T:
        """Return all inquries for a given root case."""

        if isinstance(case, Case):
            case = case.pk

        return self.filter(case__family=case)

    def for_distribution_case(self: T, case: Case | UUID | str | OuterRef | None) -> T:
        """Return all inquries for a given distribution case."""

        if isinstance(case, Case):
            case = case.pk

        return self.filter(case=case)

    def for_instance(self: T, instance: Instance | int | OuterRef | None) -> T:
        """Return all inquries for a given instance."""

        if isinstance(instance, Instance):
            instance = instance.pk

        return self.filter(case__family__instance__pk=instance)

    def addressed_to(self: T, service: ServiceType) -> T:
        """Return all inquiries addressed to a given service or a list of services.

        If multiple services are passed, it will return inquiries that are
        addressed to any of those services.
        """

        return self.filter(build_array_filter("addressed_groups", to_groups(service)))

    def controlled_by(self: T, service: ServiceType) -> T:
        """Return all inquiries controlled by a given service or a list of services.

        If multiple services are passed, it will return inquiries that are
        controlled by any of those services.
        """

        return self.filter(build_array_filter("controlling_groups", to_groups(service)))


class InquiryManager(Manager["Inquiry"]):
    """Custom manager for inquiries.

    This manager makes sure only inquiries (work items of the task configured in
    `settings.DISTRIBUTION["INQUIRY_TASK"]`) are returned. This manager uses the
    `InquiryQuerySet` and shares it's predefined filter methods.
    """

    def get_queryset(self) -> InquiryQuerySet:
        """Return the base queryset.

        This base queryset will only work items of the correct task. If the
        distribution module is not configured, it will return an empty queryset
        in every case.
        """

        queryset = super().get_queryset()

        if not settings.DISTRIBUTION:  # pragma: no cover
            return queryset.none()

        return queryset.filter(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])


class Inquiry(WorkItem):
    """Proxy model for inquries.

    This proxy models provides a streamlined API for fetching inquiries in eBau.
    The model behind it is the Caluma `WorkItem` model. The only difference is,
    that the manager (`Inquiry.objects`) makes sure that only inquiries (work
    items of the task configured in `settings.DISTRIBUTION["INQUIRY_TASK"]`) are
    returned. Also, there are lots of predefined filter methods that can help
    you query the inquiries you need.
    """

    # **DISCLAIMER:** The typing here is intentionally incorrect since typing it
    # as `InquiryManager` would not include the custom methods on our queryset
    # to be listed as a possible option in our IDEs. Since this API is built to
    # use exactly those, we fake the typing to help devs find possible filter
    # methods.
    # TODO: If anyone should find a way to fix this, please do so. At the time
    # of writing this, around 2h were spent trying to solve this problem without
    # any success.
    objects: InquiryQuerySet = InquiryManager.from_queryset(InquiryQuerySet)()

    class Meta:
        proxy = True
