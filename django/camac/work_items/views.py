from itertools import chain

from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models import (
    Case,
    Q,
    Value,
    When,
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.settings.modules.work_item_list_schema import WorkItemListConfig
from camac.user.models import Service, User
from camac.user.permissions import permission_aware
from camac.work_items.available_tasks import get_options
from camac.work_items.models import (
    WorkItemListFilterPreset,
    WorkItemListRow,
    WorkItemTemplate,
)
from camac.work_items.serializers import (
    WorkItemListFilterPresetSerializer,
    WorkItemListRowSerializer,
    WorkItemListTaskOptionSerializer,
    WorkItemTemplateSerializer,
)

from . import filters

list_settings: WorkItemListConfig = settings.WORK_ITEM_LIST


class WorkItemTemplateViewset(ReadOnlyModelViewSet):
    serializer_class = WorkItemTemplateSerializer
    queryset = WorkItemTemplate.objects
    filterset_class = filters.WorkItemTemplateFilterSet

    @permission_aware
    def get_queryset(self):
        service = self.request.group.service

        if not service:
            # Don't return anything for internal groups without services such as
            # admin and support
            return self.queryset.none()

        return self.queryset.for_service(service)

    def get_queryset_for_applicant(self):
        return self.queryset.none()


class WorkItemListFilterPresetViewset(ReadOnlyModelViewSet):
    serializer_class = WorkItemListFilterPresetSerializer
    queryset = WorkItemListFilterPreset.objects.prefetch_related(
        "tasks", "work_item_templates"
    )

    @permission_aware
    def get_queryset(self):
        service = self.request.group.service

        if not service:
            # Don't return anything for internal groups without services such as
            # admin and support
            return self.queryset.none()

        return self.queryset.filter(
            # Template for current service
            Q(services=service)
            # Template for current service group
            | Q(service_groups=service.service_group)
            # Global template
            | Q(services__isnull=True, service_groups__isnull=True)
        ).annotate(
            category=Case(
                When(
                    services=service,
                    then=Value(WorkItemListFilterPreset.PresetCategoryChoices.SERVICE),
                ),
                When(
                    service_groups=service.service_group,
                    then=Value(
                        WorkItemListFilterPreset.PresetCategoryChoices.SERVICE_GROUP
                    ),
                ),
                default=Value(WorkItemListFilterPreset.PresetCategoryChoices.STANDARD),
            ),
        )

    def get_queryset_for_applicant(self):
        return self.queryset.none()


class WorkItemListRowViewset(ReadOnlyModelViewSet):
    serializer_class = WorkItemListRowSerializer
    filterset_class = filters.WorkItemListRowFilterSet
    queryset = WorkItemListRow.objects
    filter_backends = [filters.NullsFirstOrderingFilter, DjangoFilterBackend]
    ordering_fields = ["deadline", "created_at", "target_deadline_date"]
    ordering_nulls_first = ["deadline"]
    ordering = ["deadline"]

    def get_queryset(self):
        return self.queryset.annotate_with_request_context(
            self.request.group.service_id,
            self.request.user.username,
        )

    def paginate_queryset(self, queryset):
        """Paginate the queryset.

        Since this endpoint could be quite a bottleneck for the DB, we enforce
        pagination and make sure to only prefetch the users and services for the
        current page instead of all work items.
        """

        if "page[size]" not in self.request.query_params:
            # Since this endpoint can trigger very expensive queries, we
            # specifically enforce the pagination
            raise ValidationError("Pagination is required")

        page = super().paginate_queryset(queryset)

        if page is None:  # pragma: no cover
            return page

        self._prefetch_related_users(page)
        self._prefetch_related_services(page)

        return page

    def _prefetch_related_users(self, page: list["WorkItemListRow"]):
        """Prefetch users for a page of work item list rows.

        This will prefetch the needed users (assigned_user, closed_by_user) for
        a given set of work item list rows. The output will be a dict using the
        username as key for easy access from the relation fields.
        """

        usernames = chain(*[[obj.assigned_user, obj.closed_by_user] for obj in page])
        users = User.objects.filter(username__in=usernames)

        setattr(
            self,
            "_prefetched_users",
            {user.username: user for user in users},
        )

    def _prefetch_related_services(self, page: list["WorkItemListRow"]):
        """Prefetch services for a page of work item list rows.

        This will prefetch the needed services (addressed_service) for a given
        set of work item list rows. The output will be a dict using the service
        ID as key for easy access from the relation fields.
        """
        service_ids = [obj.addressed_service for obj in page]
        services = Service.objects.filter(pk__in=service_ids).prefetch_related("trans")

        setattr(
            self,
            "_prefetched_services",
            {service.pk: service for service in services},
        )

    def has_base_permission(self, obj):
        return obj.addressed_service == self.request.group.service_id and obj.is_ready

    def has_object_assign_to_me_permission(self, obj):
        return (
            self.has_base_permission(obj)
            and obj.assigned_user != self.request.user.username
        )

    def has_object_toggle_read_permission(self, obj):
        return self.has_base_permission(obj)

    def has_object_quick_complete_permission(self, obj):
        return self.has_base_permission(obj) and obj.is_manually_completable

    @action(
        methods=["POST"],
        detail=True,
        url_path="assign-to-me",
        filterset_class=None,
    )
    @transaction.atomic
    def assign_to_me(self, request, pk):
        """Assign work item to current user.

        This is only allowed if the work item:
        - Is addressed to the current service
        - Has the status "READY"
        - Is not assigned to the current user already
        """

        obj = self.get_object()
        obj.assign_to_user(self.request.user)
        return Response(self.get_serializer(obj).data)

    @action(
        methods=["POST"],
        detail=True,
        url_path="toggle-read",
        filterset_class=None,
    )
    @transaction.atomic
    def toggle_read(self, request, pk):
        """Toggle read status of a work item.

        This is only allowed if the work item:
        - Is addressed to the current service
        - Has the status "READY"
        """

        obj = self.get_object()
        obj.toggle_read()
        return Response(self.get_serializer(obj).data)

    @action(
        methods=["POST"],
        detail=True,
        url_path="quick-complete",
        filterset_class=None,
    )
    @transaction.atomic
    def quick_complete(self, request, pk):
        """Complete work item.

        This is only allowed if the work item:
        - Is addressed to the current service
        - Has the status "READY"
        - Is related to a task marked as manually completable (meta property)
        """

        obj = self.get_object()
        complete_work_item(
            work_item=obj,
            user=request.caluma_info.context.user,
        )
        return Response(self.get_serializer(obj).data)


class WorkItemListTaskOptionsView(ListAPIView):
    serializer_class = WorkItemListTaskOptionSerializer

    def list(self, request, *args, **kwargs):
        """List all options for the task filter on the work item list.

        This can be a combination between configured tasks and manual work item
        templates.
        """

        work_items = WorkItem.objects.none()

        if settings.WORK_ITEM_LIST.available_tasks_include_count:
            # If the count of work items matching each task or template should
            # be included, we need to get all visible work items and filter them
            # with the same filters used for displaying the rows.
            #
            # Since we don't need any annotations for filtering, we use the
            # normal work item model instead of the work item list row proxy
            # model to simplify the query.

            work_items = filters.WorkItemListRowFilterSet(
                data=request.query_params,
                request=request,
                queryset=WorkItem.objects.filter(deadline__isnull=False),
            ).qs

        options = get_options(
            self.request.group,
            work_items,
            request.query_params.get("preset"),
        )

        serializer = self.get_serializer(options, many=True)

        return Response(serializer.data)
