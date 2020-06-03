from caluma.caluma_core.visibilities import filter_queryset_for
from caluma.caluma_form import (
    historical_schema as historical_form_schema,
    schema as form_schema,
)
from caluma.caluma_user.visibilities import Authenticated
from django.db.models import F, Q

from camac.caluma.api import CamacRequest
from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.utils import filters


class CustomVisibility(Authenticated, InstanceQuerysetMixin):
    """Custom visibility for Kanton Bern.

    Note: This expects that each document has a meta property that stores the
    CAMAC instance identifier, named "camac-instance-id". Each node is
    filtered by indirectly looking for the value of said property.

    To avoid multiple db lookups, the result is cached in the
    request object, and reused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    instance_field = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.user = None

    @filter_queryset_for(form_schema.Document)
    def filter_queryset_for_document(self, node, queryset, info):
        instance_ids = self._all_visible_instances(info)

        return queryset.filter(
            # document is accessible through CAMAC ACLs
            Q(**{"family__meta__camac-instance-id__in": instance_ids})
            # OR dashboard documents
            | Q(form_id=DASHBOARD_FORM_SLUG)
            # OR unlinked table documents created by the requesting user
            | Q(
                **{
                    "meta__camac-instance-id__isnull": True,
                    "family": F("pk"),
                    "created_by_user": info.context.user.username,
                }
            )
        )

    @filter_queryset_for(historical_form_schema.HistoricalDocument)
    def filter_queryset_for_historicaldocument(
        self, node, queryset, info
    ):  # pragma: no cover
        # TODO remove this method and apply chained decorator to `filter_queryset_for_document`
        return self.filter_queryset_for_document(node, queryset, info)

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

        camac_request = CamacRequest(info)

        self.user = camac_request.request.user
        self.group = camac_request.request.group

        filtered = CalumaInstanceFilterSet(
            data=filters(camac_request.request),
            queryset=self.get_queryset(self.group),
            request=camac_request.request,
        )

        instance_ids = list(filtered.qs.values_list("pk", flat=True))

        setattr(info.context, "_visibility_instances_cache", instance_ids)
        return instance_ids
