from caluma.caluma_core.visibilities import filter_queryset_for
from caluma.caluma_form import (
    historical_schema as historical_form_schema,
    schema as form_schema,
)
from caluma.caluma_user.visibilities import Authenticated
from caluma.caluma_workflow import schema as workflow_schema
from django.db.models import F, Q

from camac.caluma.utils import CamacRequest
from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.utils import filters


def disallow_public_access(fn):
    def wrapper(self, node, queryset, info):
        if not info.context.user.is_authenticated:
            return queryset.none()

        return fn(self, node, queryset, info)

    return wrapper


class CustomVisibility(Authenticated, InstanceQuerysetMixin):
    """Custom visibility for Kanton Bern.

    To avoid multiple db lookups, the result is cached in the
    request object, and reused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    instance_field = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.user = None
        self.request = None

    @filter_queryset_for(form_schema.Question)
    @filter_queryset_for(form_schema.Form)
    @filter_queryset_for(form_schema.Option)
    @filter_queryset_for(form_schema.DynamicOption)
    def filter_queryset_public(self, node, queryset, info):
        # this is blueprint data which is uncritical and can be exposed publicly
        return queryset

    @filter_queryset_for(form_schema.Document)
    @filter_queryset_for(historical_form_schema.HistoricalDocument)
    def filter_queryset_for_document(self, node, queryset, info):
        instance_ids = self._all_visible_instances(info)

        return queryset.filter(
            # document is accessible through CAMAC ACLs
            Q(family__case__family__instance__pk__in=instance_ids)
            | Q(family__work_item__case__family__instance__pk__in=instance_ids)
            # OR dashboard documents
            | Q(form_id=DASHBOARD_FORM_SLUG)
            # OR unlinked table documents created by the requesting user
            | Q(
                family__case__instance__isnull=True,
                family=F("pk"),
                created_by_user=info.context.user.username,
            )
        )

    @filter_queryset_for(form_schema.Answer)
    @filter_queryset_for(historical_form_schema.HistoricalAnswer)
    def filter_queryset_for_answer(self, node, queryset, info):
        # return all answers, since answers can only be accessed via documents
        # which are already properly protected
        return queryset

    @filter_queryset_for(workflow_schema.Case)
    @disallow_public_access
    def filter_queryset_for_case(self, node, queryset, info):
        return queryset.filter(
            family__instance__pk__in=self._all_visible_instances(info)
        )

    @filter_queryset_for(workflow_schema.WorkItem)
    @disallow_public_access
    def filter_queryset_for_work_items(self, node, queryset, info):
        return queryset.filter(
            case__family__instance__pk__in=self._all_visible_instances(info)
        )

    def get_base_queryset(self):
        """Overridden from InstanceQuerysetMixin to avoid the super().get_queryset() call."""
        instance_state_expr = self._get_instance_filter_expr("instance_state")
        return Instance.objects.all().select_related(instance_state_expr)

    def _all_visible_instances(self, info):
        """Fetch visible camac instances and cache the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP` or use
        default group  to retrieve all Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:  # pragma: no cover
            return result

        self.request = CamacRequest(info).request

        filtered = CalumaInstanceFilterSet(
            data=filters(self.request),
            queryset=self.get_queryset(),
            request=self.request,
        )

        instance_ids = filtered.qs.values_list("pk", flat=True)

        setattr(info.context, "_visibility_instances_cache", instance_ids)
        return instance_ids
